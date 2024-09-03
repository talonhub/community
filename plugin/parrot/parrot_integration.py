from copy import copy
from dataclasses import dataclass
from typing import Callable, Optional, Sequence
import json
import logging
import time

from talon import Module, resource, events
from talon.debug import log_exception
from talon.experimental.parrot import ParrotSystem, ParrotDelegate, ParrotFrame
from talon_init import TALON_HOME

PARROT_HOME = TALON_HOME / 'user' / 'community' / 'plugin' / 'parrot'
pattern_path = str(PARROT_HOME / 'patterns.json')
model_path = str(PARROT_HOME / 'model.pkl')

## START PARROT CLASSES ##
class PatternMatcher:
    def detect_all(self, frame: ParrotFrame, detection_functions: list[Callable]) -> bool:
        """Matcher for all detection functions"""
        for detect_function in detection_functions:
            if detect_function(self, frame) == False:
                return False
        return True

@dataclass
class NoiseTimestamps:
    last_detected_at:  float = 0.0
    duration_start:    float = 0.0
    detection_after:   float = 0.0
    graceperiod_until: float = 0.0
    throttled_at:      float = 0.0
    throttled_until:   float = 0.0

MatchPatternCallable = Callable[['NoisePattern', ParrotFrame, float], bool]

class NoisePattern(PatternMatcher):
    """Class containing all the thresholds and timestamps for a noise"""
    name: str
    # match_pattern: MatchPatternCallable # mypy bug
    duration: float
    throttles: dict[str, float]
    lowest_power_thresholds: list[float]
    labels: frozenset[str]

    # This graceperiod is purely used to dampen the effects of a noises probability getting more unstable over time with the current model
    graceperiod_length: float
    detection_after:    float
    timestamps: NoiseTimestamps

    def __init__(self, name: str, labels: list[str], match_pattern: MatchPatternCallable, lowest_power_thresholds: list[float], throttles: dict[str, float], detection_after: float, graceperiod_length: float):
        self.name = name
        self.match_pattern = match_pattern
        self.lowest_power_thresholds = lowest_power_thresholds
        self.detection_after = detection_after
        self.graceperiod_length = graceperiod_length
        self.throttles = throttles
        self.duration = 0
        self.labels = frozenset(labels)
        self.timestamps = NoiseTimestamps()

    def is_active(self, time) -> bool:
        """Check if a current noise is active"""
        return self.timestamps.throttled_until < time

    def detect(self, frame: ParrotFrame) -> bool:
        """Matches the pattern against the last N raw frames of the model classifier"""
        grace_detected = False
        detected = False
        if self.is_active(frame.ts):
            if self.match_pattern(self, frame, self.timestamps.graceperiod_until):
                self.timestamps.duration_start = self.timestamps.duration_start if self.timestamps.duration_start > 0 else frame.ts
                grace_detected = True

                # If there is a duration threshold, wait to activate until the duration has passed before marking the pattern as detected
                if (self.timestamps.duration_start + self.detection_after) <= frame.ts:
                    detected = True
                    self.timestamps.last_detected_at = frame.ts
                    self.timestamps.graceperiod_until = frame.ts + self.graceperiod_length
                    self.duration = frame.ts - self.timestamps.duration_start

        # Reset graceperiod if the detection did not match
        if grace_detected == False:
            self.timestamps.graceperiod_until = 0
            self.duration = 0

        # Reset the duration if the graceperiod has ended
        if self.timestamps.duration_start > 0 and detected == False and grace_detected == False and self.timestamps.graceperiod_until < (frame.ts + self.graceperiod_length):
            self.timestamps.duration_start = 0
            self.duration = 0

        return detected

    def reset_timestamps(self):
        """Reset all the activation timeouts"""
        self.timestamps.graceperiod_until = 0
        self.timestamps.duration_start = 0
        self.duration = 0

    def throttle(self, throttle_until: float, throttle_at: float):
        """Throttle the detection of this pattern until the timestamp is passed if the throttle is higher than the highest current throttle"""
        if throttle_until > self.timestamps.throttled_until:
            self.timestamps.throttled_at = throttle_at
            self.timestamps.throttled_until = throttle_until
            self.timestamps.graceperiod_until = 0

    def get_throttles(self) -> dict[str, float]:
        """Returns a dict of all the patterns to throttle after this pattern has been detected"""
        return self.throttles

    def get_current_lowest_power_threshold(self, time: float) -> float:
        """Retrieve the lowest power threshold to aid in determining when to skip forward passes"""
        return self.lowest_power_thresholds[1] if time < self.timestamps.graceperiod_until else self.lowest_power_thresholds[0]

class PatternBuilder:
    """Class that builds and validates the patterns to make sure they have the right syntax"""
    possible_thresholds = frozenset(['>power', '>f0', '>f1', '>f2', '>probability', '>ratio', '<power', '<f0', '<f1', '<f2', '<probability', '<ratio'])
    possible_keys = frozenset(['sounds', 'detect_after', 'threshold', 'graceperiod', 'grace_threshold', 'throttle'])

    def build(self, name: str, pattern: dict) -> Optional[NoisePattern]:
        """Builds a valid pattern or skips it in case the pattern is invalid"""
        for key in pattern:
            if key not in self.possible_keys:
                logging.warning(f"[parrot] unknown key {repr(key)}")

        if 'sounds' not in pattern or len(pattern['sounds']) == 0:
            logging.error(f"[parrot] skipping noise {repr(name)}: No sounds defined.")
            return None

        for key in pattern['threshold']:
            if key not in self.possible_thresholds:
                logging.warning(f"[parrot] unknown threshold key: {repr(key)}")
        detection_calls = self.generate_matching_functions(pattern['threshold'], pattern['sounds'])

        if 'grace_threshold' in pattern:
            for key in pattern['grace_threshold']:
                if key not in self.possible_thresholds:
                    logging.warning("[parrot] unknown grace threshold key: {repr(key)}")
            graceperiod_detection_calls = self.generate_matching_functions(pattern['grace_threshold'], pattern['sounds'])
        else:
            graceperiod_detection_calls = copy(detection_calls)

        # Calculate the lowest power thresholds - These are used for optimisation purposes
        # By default set the threshold at 20 to prevent continuous recognition on silence
        lowest_power_thresholds: list[float] = [20, 0]
        if '>power' in pattern['threshold']:
            lowest_power_thresholds[0] = pattern['threshold']['>power']
        if 'grace_threshold' in pattern and '>power' in pattern['grace_threshold']:
            lowest_power_thresholds[1] = pattern['grace_threshold']['>power']

        grace_period = pattern['graceperiod'] if 'graceperiod' in pattern else 0
        detection_after = pattern['detect_after'] if 'detect_after' in pattern else 0

        def match_pattern(self, frame: ParrotFrame, graceperiod_until: float):
            return self.detect_all(frame, graceperiod_detection_calls) if frame.ts < graceperiod_until else self.detect_all(frame, detection_calls)

        throttles = {}
        if 'throttle' in pattern:
            if name not in pattern['throttle']:
                pattern['throttle'][name] = 0
            throttles = pattern['throttle']

        return NoisePattern(name, pattern['sounds'], match_pattern, lowest_power_thresholds, throttles, detection_after, grace_period)

    def generate_matching_functions(self, thresholds, sounds):
        """Generate noise matching functions"""
        detection_calls = []

        if '>probability' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['>probability'], sounds=sounds: sum( frame.classes[sound] for sound in sounds) >= threshold )
        if '>power' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['>power']: frame.power >= threshold )
        if '>ratio' in thresholds and len(sounds) > 1:
            detection_calls.append( lambda self, frame, threshold=thresholds['>ratio'], sounds=sounds: ( frame.classes[sounds[0]] / frame.classes[sounds[1]] >= threshold ) )
        if '>f0' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['>f0']: frame.f0 >= threshold )
        if '>f1' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['>f1']: frame.f1 >= threshold )
        if '>f2' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['>f2']: frame.f2 >= threshold )

        # Lower than matches
        if '<probability' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['<probability'], sounds=sounds: sum( frame.classes[sound] for sound in sounds) < threshold )
        if '<power' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['<power']: frame.power < threshold )
        if '<ratio' in thresholds and len(sounds) > 1:
            detection_calls.append( lambda self, frame, threshold=thresholds['<ratio'], sounds=sounds: ( frame.classes[sounds[0]] / frame.classes[sounds[1]] < threshold ) )
        if '<f0' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['<f0']: frame.f0 < threshold )
        if '<f1' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['<f1']: frame.f1 < threshold )
        if '<f2' in thresholds:
            detection_calls.append( lambda self, frame, threshold=thresholds['<f2']: frame.f2 < threshold )

        return detection_calls

# END PARROT CLASSES #

class Delegate(ParrotDelegate):
    raw_patterns: list[NoisePattern]
    patterns: dict[str, NoisePattern]
    debug: bool
    last_frame_was_forwardpass: bool
    classes: Optional[set[str]]

    def __init__(self, *, debug: bool=False):
        self.debug = debug
        self.patterns = {}
        self.last_frame_was_forwardpass = False
        self.classes = None
        self.raw_patterns = []

    def apply_patterns(self) -> None:
        classes = self.classes
        patterns_to_validate = self.raw_patterns
        if classes is None:
            return
        # discard invalid patterns
        invalid_patterns: set[str] = set()
        patterns: dict[str, NoisePattern] = {}
        for pattern in patterns_to_validate:
            # NOTE: could make a note of the actual invalid labels, from the result of this set subtraction
            if len(pattern.labels - classes) > 0:
                invalid_patterns.add(pattern.name)
                events.write("parrot", f"invalid: {pattern.name}")
            else:
                patterns[pattern.name] = pattern
                events.write("parrot", f"added: {pattern.name}")
        self.patterns = patterns
        for name in invalid_patterns:
            logging.warning(f"[parrot] pattern {repr(name)} contains invalid labels and will not be used.")
        if invalid_patterns:
            class_names = ', '.join(classes)
            logging.warning(f"[parrot] use one of the following labels: {class_names}")

    def set_class_names(self, classes: set[str]) -> None:
        self.classes = classes
        self.apply_patterns()

    def set_patterns(self, json_patterns: dict) -> None:
        pattern_builder = PatternBuilder()
        patterns: list[NoisePattern] = []
        for key, config in json_patterns.items():
            pattern = pattern_builder.build(key, config)
            if pattern is not None:
                patterns.append(pattern)
        self.raw_patterns = patterns
        self.apply_patterns()

    def calculate_silence_threshold(self) -> float:
        """Calculate the power threshold needed before we need to do noise recognition given the currently active noises"""
        current_time = time.perf_counter()
        inactive_power_threshold = 10000000
        thresholds = []
        for pattern in self.patterns.values():
            if pattern.is_active(current_time):
                thresholds.append(pattern.get_current_lowest_power_threshold(current_time))

        # If the debug is on, drop the silence threshold to make it easier to view model output for debugging
        if self.debug:
            thresholds.append(10)

        # If no noises are active - skip all noise recognition and save some CPU
        if len(thresholds) == 0:
            return inactive_power_threshold
        else:
            return min(thresholds)

    def throttle_patterns(self, throttles_s: dict[str, float], current_time: float):
        """Throttles the given pattern names until the matching milliseconds are passed"""
        for pattern_name in throttles_s:
            pattern = self.patterns.get(pattern_name)
            if pattern is not None:
                pattern.throttle(current_time + throttles_s[pattern_name], current_time)

    def power_threshold(self, power: float) -> bool:
        silence_power_threshold = self.calculate_silence_threshold()

        # Reset all the duration timeouts if we are transitioning to silence
        should_forwardpass = power > silence_power_threshold
        if self.last_frame_was_forwardpass and not should_forwardpass:
            for pattern in self.patterns.values():
                pattern.reset_timestamps()

        self.last_frame_was_forwardpass = should_forwardpass
        return should_forwardpass

    def pattern_match(self, frame: ParrotFrame) -> set[str]:
        if self.debug:
            winner_label, winner_prob = next(iter(frame.classes.items()))
            events.write('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")

        active: set[str] = set()
        for pattern in self.patterns.values():
            if pattern.detect(frame):
                active.add(pattern.name)
                self.throttle_patterns(pattern.get_throttles(), frame.ts)

        return active

parrot_delegate = Delegate(debug=False)
system = ParrotSystem(model_path, parrot_delegate)

@resource.watch(pattern_path)
def on_pattern(f):
    try:
        parrot_delegate.set_patterns(json.load(f))
    except Exception:
        log_exception(f"[parrot] invalid pattern file: {pattern_path}")
