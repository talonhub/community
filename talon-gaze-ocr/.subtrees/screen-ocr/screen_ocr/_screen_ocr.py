"""Library for processing screen contents using OCR."""

import os
import platform
import re
from collections import deque
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from itertools import islice
from typing import (
    Any,
    Optional,
    Union,
)

try:
    from rapidfuzz import fuzz
except ImportError:
    print("Attempting to fall back to pure python rapidfuzz")
    os.environ["RAPIDFUZZ_IMPLEMENTATION"] = "python"
    from rapidfuzz import fuzz

from . import _base

# Optional backends.
try:
    from . import _tesseract
except (ImportError, SyntaxError):
    _tesseract = None
try:
    from . import _easyocr
except ImportError:
    _easyocr = None
try:
    from . import _talon
except ImportError:
    _talon = None
try:
    from . import _winrt
except (ImportError, SyntaxError):
    _winrt = None


# Optional packages needed for certain backends.
try:
    from PIL import Image, ImageGrab, ImageOps
except ImportError:
    Image = ImageGrab = ImageOps = None
try:
    from talon import actions, screen, ui
    from talon.types.rect import Rect
except ImportError:
    ui = screen = Rect = actions = None

# Represented as [left, top, right, bottom] pixel coordinates
BoundingBox = tuple[int, int, int, int]

if Rect:

    def to_rect(bounding_box: BoundingBox) -> Rect:
        return Rect(
            x=bounding_box[0],
            y=bounding_box[1],
            width=bounding_box[2] - bounding_box[0],
            height=bounding_box[3] - bounding_box[1],
        )

    def to_bounding_box(rect_talon: Rect) -> BoundingBox:
        return (
            rect_talon.x,
            rect_talon.y,
            rect_talon.x + rect_talon.width,
            rect_talon.y + rect_talon.height,
        )


class Reader:
    """Reads on-screen text using OCR."""

    @classmethod
    def create_quality_reader(cls, **kwargs) -> "Reader":
        """Create reader optimized for quality.

        See constructor for full argument list.
        """
        if _winrt:
            return cls.create_reader(backend="winrt", **kwargs)
        else:
            return cls.create_reader(backend="tesseract", **kwargs)

    @classmethod
    def create_fast_reader(cls, **kwargs) -> "Reader":
        """Create reader optimized for speed.

        See constructor for full argument list.
        """
        if _winrt:
            return cls.create_reader(backend="winrt", **kwargs)
        else:
            defaults = {
                "threshold_function": "otsu",
                "correction_block_size": 41,
                "margin": 60,
            }
            return cls.create_reader(backend="tesseract", **dict(defaults, **kwargs))

    @classmethod
    def create_reader(
        cls,
        backend: Union[str, _base.OcrBackend],
        tesseract_data_path=None,
        tesseract_command=None,
        threshold_function="local_otsu",
        threshold_block_size=41,
        correction_block_size=31,
        convert_grayscale=True,
        shift_channels=True,
        debug_image_callback=None,
        language_tag=None,
        **kwargs,
    ) -> "Reader":
        """Create reader with specified backend."""
        if isinstance(backend, _base.OcrBackend):
            return cls(backend, **kwargs)
        if backend == "tesseract":
            if not _tesseract:
                raise ValueError(
                    "Tesseract backend unavailable. To install, run pip install screen-ocr[tesseract]."
                )
            backend = _tesseract.TesseractBackend(
                tesseract_data_path=tesseract_data_path,
                tesseract_command=tesseract_command,
                threshold_function=threshold_function,
                threshold_block_size=threshold_block_size,
                correction_block_size=correction_block_size,
                convert_grayscale=convert_grayscale,
                shift_channels=shift_channels,
                debug_image_callback=debug_image_callback,
            )
            defaults = {
                "resize_factor": 2,
                "margin": 50,
            }
            return cls(
                backend,
                debug_image_callback=debug_image_callback,
                **dict(defaults, **kwargs),
            )
        if backend == "easyocr":
            if not _easyocr:
                raise ValueError(
                    "EasyOCR backend unavailable. To install, run pip install screen-ocr[easyocr]."
                )
            backend = _easyocr.EasyOcrBackend()
            return cls(backend, debug_image_callback=debug_image_callback, **kwargs)
        if backend == "winrt":
            if not _winrt:
                raise ValueError(
                    "WinRT backend unavailable. To install, run pip install screen-ocr[winrt]."
                )
            try:
                backend = _winrt.WinRtBackend(language_tag)
            except ImportError as e:
                raise ValueError(
                    "WinRT backend unavailable. To install, run pip install screen-ocr[winrt]."
                ) from e
            return cls(
                backend,
                debug_image_callback=debug_image_callback,
                **dict({"resize_factor": 2}, **kwargs),
            )
        if backend == "talon":
            if not _talon:
                raise ValueError(
                    "Talon backend unavailable. Requires installing and running in Talon (see talonvoice.com)."
                )
            backend = _talon.TalonBackend()
            return cls(backend, debug_image_callback=debug_image_callback, **kwargs)
        raise RuntimeError(f"Unsupported backend: {backend}")

    def __init__(
        self,
        backend: _base.OcrBackend,
        margin: int = 0,
        resize_factor: int = 1,
        resize_method=None,  # Pillow resize method
        debug_image_callback: Optional[Callable[[str, Any], None]] = None,
        confidence_threshold: float = 0.75,
        radius: int = 200,  # screenshot "radius"
        search_radius: int = 125,
        homophones: Optional[Mapping[str, Iterable[str]]] = None,
    ):
        self._backend = backend
        self.margin = margin
        self.resize_factor = resize_factor
        if resize_method or resize_factor == 1:
            self.resize_method = resize_method
        else:
            assert Image
            self.resize_method = Image.Resampling.LANCZOS
        self.debug_image_callback = debug_image_callback
        self.confidence_threshold = confidence_threshold
        self.radius = radius
        self.search_radius = search_radius
        self.homophones = (
            ScreenContents._normalize_homophones(homophones)
            if homophones
            else default_homophones()
        )
        # On most platforms the HUD will not be present in the screenshot. It is
        # observed that on Windows, Windows 10 does not hide the HUD, despite the
        # Microsoft documentation suggesting otherwise. To work around this, we toggle
        # the HUD visibility on older Windows versions.
        self.needs_hud_toggle = False
        try:
            if actions and platform.system() == "Windows":
                win_ver = tuple(map(int, platform.version().split(".")))
                if win_ver < (10, 0, 22000):  # Initial Windows 11 release
                    self.needs_hud_toggle = True
        except Exception:
            print("Failed to check Windows version. Will not toggle HUD.")
            pass

    def read_nearby(
        self,
        screen_coordinates: tuple[int, int],
        search_radius: Optional[int] = None,
        crop_radius: Optional[int] = None,
    ):
        """Return ScreenContents nearby the provided coordinates."""
        search_radius = search_radius or self.search_radius
        crop_radius = crop_radius or self.radius
        bounding_box = (
            screen_coordinates[0] - crop_radius,
            screen_coordinates[1] - crop_radius,
            screen_coordinates[0] + crop_radius,
            screen_coordinates[1] + crop_radius,
        )
        screenshot, bounding_box = self._clean_screenshot(bounding_box)
        return self.read_image(
            screenshot,
            bounding_box=bounding_box,
            screen_coordinates=screen_coordinates,
            search_radius=search_radius,
        )

    def read_screen(self, bounding_box: Optional[BoundingBox] = None):
        """Return ScreenContents for the entire screen."""
        screenshot, bounding_box = self._clean_screenshot(bounding_box)
        return self.read_image(
            screenshot,
            bounding_box=bounding_box,
            screen_coordinates=None,
            search_radius=None,
        )

    def read_current_window(self):
        if not self._is_talon_backend():
            raise NotImplementedError
        assert ui
        win = ui.active_window()
        bounding_box = to_bounding_box(win.rect)
        screenshot, bounding_box = self._clean_screenshot(
            bounding_box, clamp_to_main_screen=False
        )
        return self.read_image(
            screenshot,
            bounding_box=bounding_box,
        )

    def read_image(
        self,
        image,
        bounding_box: Optional[BoundingBox] = None,
        screen_coordinates: Optional[tuple[int, int]] = None,
        search_radius: Optional[int] = None,
    ):
        """Return ScreenContents of the provided image."""
        bounding_box = bounding_box or (0, 0, image.width, image.height)
        search_radius = search_radius or self.search_radius
        preprocessed_image = self._preprocess(image)
        result = self._backend.run_ocr(preprocessed_image)
        result = self._adjust_result(result, bounding_box[0:2])
        return ScreenContents(
            screen_coordinates=screen_coordinates,
            bounding_box=bounding_box,
            screenshot=image,
            result=result,
            confidence_threshold=self.confidence_threshold,
            homophones=self.homophones,
            search_radius=search_radius,
        )

    # TODO: Refactor methods into backend instead of using this.
    def _is_talon_backend(self):
        return _talon and isinstance(self._backend, _talon.TalonBackend)

    def _clean_screenshot(
        self, bounding_box: Optional[BoundingBox], clamp_to_main_screen: bool = True
    ) -> tuple[Any, BoundingBox]:
        if not self.needs_hud_toggle:
            return self._screenshot(bounding_box, clamp_to_main_screen)
        # Attempt to turn off HUD if talon_hud is installed.
        try:
            actions.user.hud_set_visibility(False, pause_seconds=0.02)
        except Exception:
            pass
        try:
            return self._screenshot(bounding_box, clamp_to_main_screen)
        finally:
            # Attempt to turn on HUD if talon_hud is installed.
            try:
                actions.user.hud_set_visibility(True, pause_seconds=0.001)
            except Exception:
                pass

    def _screenshot(
        self, bounding_box: Optional[BoundingBox], clamp_to_main_screen: bool = True
    ) -> tuple[Any, BoundingBox]:
        if self._is_talon_backend():
            assert screen
            assert to_rect
            screen_box = screen.main().rect
            if bounding_box and clamp_to_main_screen:
                bounding_box = (
                    max(0, bounding_box[0]),
                    max(0, bounding_box[1]),
                    min(screen_box.width, bounding_box[2]),
                    min(screen_box.height, bounding_box[3]),
                )
            if not bounding_box:
                bounding_box = (0, 0, screen_box.width, screen_box.height)
            screenshot = screen.capture_rect(
                to_rect(bounding_box),
                retina=False,
            )
        else:
            # TODO Consider cropping within grab() for performance. Requires knowledge
            # of screen bounds.
            assert ImageGrab
            screenshot = ImageGrab.grab()
            if bounding_box:
                bounding_box = (
                    max(0, bounding_box[0]),
                    max(0, bounding_box[1]),
                    min(screenshot.width, bounding_box[2]),
                    min(screenshot.height, bounding_box[3]),
                )
            else:
                bounding_box = (0, 0, screenshot.width, screenshot.height)
            screenshot = screenshot.crop(bounding_box)
        return screenshot, bounding_box

    def _adjust_result(
        self, result: _base.OcrResult, offset: tuple[int, int]
    ) -> _base.OcrResult:
        lines = []
        for line in result.lines:
            words = []
            for word in line.words:
                left = (word.left - self.margin) / self.resize_factor + offset[0]
                top = (word.top - self.margin) / self.resize_factor + offset[1]
                width = word.width / self.resize_factor
                height = word.height / self.resize_factor
                words.append(_base.OcrWord(word.text, left, top, width, height))
            lines.append(_base.OcrLine(words))
        return _base.OcrResult(lines)

    def _preprocess(self, image):
        if self.resize_factor != 1:
            new_size = (
                image.size[0] * self.resize_factor,
                image.size[1] * self.resize_factor,
            )
            image = image.resize(new_size, self.resize_method)
        if self.debug_image_callback:
            self.debug_image_callback("debug_resized", image)
        if self.margin:
            assert ImageOps
            image = ImageOps.expand(image, self.margin, "white")
        if not self._is_talon_backend():
            # Ensure consistent performance measurements.
            image.load()
        return image


def default_homophones() -> Mapping[str, Iterable[str]]:
    homophone_list = [
        # 0k is not actually a homophone but is frequently produced by OCR.
        ("ok", "okay", "0k"),
        ("close", "clothes"),
        ("0", "zero"),
        ("1", "one"),
        ("2", "two", "too", "to"),
        ("3", "three"),
        ("4", "four", "for"),
        ("5", "five"),
        ("6", "six"),
        ("7", "seven"),
        ("8", "eight"),
        ("9", "nine"),
        (".", "period"),
    ]
    homophone_map = {}
    for homophone_set in homophone_list:
        for homophone in homophone_set:
            homophone_map[homophone] = homophone_set
    return homophone_map


@dataclass
class WordLocation:
    """Location of a word on-screen."""

    left: int
    top: int
    width: int
    height: int
    left_char_offset: int
    right_char_offset: int
    text: str
    ocr_word_index: int
    ocr_line_index: int

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @property
    def middle_x(self) -> int:
        return int(self.left + self.width / 2)

    @property
    def middle_y(self) -> int:
        return int(self.top + self.height / 2)

    @property
    def start_coordinates(self) -> tuple[int, int]:
        return (self.left, self.middle_y)

    @property
    def middle_coordinates(self) -> tuple[int, int]:
        return (self.middle_x, self.middle_y)

    @property
    def end_coordinates(self) -> tuple[int, int]:
        return (self.right, self.middle_y)

    def is_adjacent_left_of(
        self, other: "WordLocation", allow_whitespace: bool
    ) -> bool:
        """Return True if the other word is adjacent to this word. Only valid if both
        WordLocations are from the same ScreenContents."""
        if self.ocr_line_index != other.ocr_line_index:
            return False
        elif self.ocr_word_index == other.ocr_word_index:
            return self.left_char_offset + len(self.text) == other.left_char_offset
        elif allow_whitespace and self.ocr_word_index + 1 == other.ocr_word_index:
            return self.right_char_offset == 0 and other.left_char_offset == 0
        else:
            return False


class ScreenContents:
    """OCR'd contents of a portion of the screen."""

    WordLocationsPredicate = Callable[[Sequence[WordLocation]], bool]

    def __init__(
        self,
        screen_coordinates: Optional[tuple[int, int]],
        bounding_box: BoundingBox,
        screenshot,
        result: _base.OcrResult,
        confidence_threshold: float,
        homophones: Mapping[str, Iterable[str]],
        search_radius: Optional[int],
    ):
        self.screen_coordinates = screen_coordinates
        self.bounding_box = bounding_box
        self.screenshot = screenshot
        self.result = result
        self.confidence_threshold = confidence_threshold
        self.homophones = homophones
        if search_radius:
            self.search_radius = search_radius
            self._search_radius_squared = search_radius * search_radius
        else:
            self.search_radius = None

    def as_string(self) -> str:
        """Return the contents formatted as a string."""
        lines = []
        for line in self.result.lines:
            words = []
            for word in line.words:
                words.append(word.text)
            lines.append(" ".join(words) + "\n")
        return "".join(lines)

    def cropped(self, bounding_box: BoundingBox) -> "ScreenContents":
        """Return a new ScreenContents cropped to the provided bounding box."""
        left, top, right, bottom = bounding_box
        lines = []
        for line in self.result.lines:
            words = []
            for word in line.words:
                if (
                    word.left > right
                    or word.left + word.width < left
                    or word.top > bottom
                    or word.top + word.height < top
                ):
                    continue
                words.append(word)
            lines.append(_base.OcrLine(words))
        result = _base.OcrResult(lines)
        return ScreenContents(
            screen_coordinates=self.screen_coordinates,
            bounding_box=bounding_box,
            screenshot=self.screenshot,  # TODO crop screenshot
            result=result,
            confidence_threshold=self.confidence_threshold,
            homophones=self.homophones,
            search_radius=self.search_radius,
        )

    def find_nearest_word_coordinates(
        self, target_word: str, cursor_position: str
    ) -> Optional[tuple[int, int]]:
        """Return the coordinates of the nearest instance of the provided word.

        Uses fuzzy matching.

        Arguments:
        word: The word to search for.
        cursor_position: "before", "middle", or "after" (relative to the matching word)
        """
        if cursor_position not in ("before", "middle", "after"):
            raise ValueError("cursor_position must be either before, middle, or after")
        word_location = self.find_nearest_word(target_word)
        if not word_location:
            return None
        if cursor_position == "before":
            return word_location.start_coordinates
        elif cursor_position == "middle":
            return word_location.middle_coordinates
        elif cursor_position == "after":
            return word_location.end_coordinates

    def find_nearest_word(self, target_word: str) -> Optional[WordLocation]:
        """Return the location of the nearest instance of the provided word.

        Uses fuzzy matching.
        """
        result = self.find_nearest_words(target_word)
        return result[0] if (result and len(result) == 1) else None

    def find_nearest_words(
        self,
        target: str,
        filter_function: Optional[Callable[[Sequence[WordLocation]], bool]] = None,
    ) -> Optional[Sequence[WordLocation]]:
        """Return the locations of the nearest sequence of the provided words.

        Uses fuzzy matching.
        """
        sequences = self.find_matching_words(target)
        if filter_function:
            sequences = list(filter(filter_function, sequences))
        return self.find_nearest_words_within_matches(sequences)

    def find_nearest_words_within_matches(
        self, sequences: Sequence[Sequence[WordLocation]]
    ) -> Optional[Sequence[WordLocation]]:
        if not sequences:
            return None
        if not self.screen_coordinates:
            # "Nearest" is undefined.
            return None
        distance_to_words = [
            (
                self._distance_squared(
                    (words[0].left + words[-1].right) / 2.0,
                    (words[0].top + words[-1].bottom) / 2.0,
                    *self.screen_coordinates,
                ),
                words,
            )
            for words in sequences
        ]
        return min(distance_to_words, key=lambda x: x[0])[1]

    # Special-case "0k" which frequently shows up instead of the correct "OK".
    _SUBWORD_REGEX = re.compile(r"\b0[Kk]\b|[A-Z][A-Z]+|[A-Za-z'][a-z']*|\S")

    def find_matching_words(
        self, target: str, match_each_word: bool = False
    ) -> Sequence[Sequence[WordLocation]]:
        """Return the locations of all sequences of the provided words.

        Uses fuzzy matching.
        """
        if not target:
            raise ValueError("target is empty")
        target_words = [
            self._normalize(subword)
            for subword in re.findall(self._SUBWORD_REGEX, target)
        ]

        # First, find all matches tied for highest score.
        scored_words = [
            (
                self._score_words(
                    candidates, target_words, match_each_word=match_each_word
                ),
                candidates,
            )
            for candidates in self._generate_candidates(
                self.result,
                len(target_words),
                include_compound_words=not match_each_word,
            )
        ]
        # print("\n".join(map(str, scored_words)))
        scored_words = [words for words in scored_words if words[0]]
        if not scored_words:
            return []
        max_score = max(score for score, _ in scored_words)
        best_matches = [words for score, words in scored_words if score == max_score]
        if not self.search_radius or not self.screen_coordinates:
            return best_matches
        return [
            words
            for words in best_matches
            if self._distance_squared(
                (words[0].left + words[-1].right) / 2.0,
                (words[0].top + words[-1].bottom) / 2.0,
                *self.screen_coordinates,
            )
            <= self._search_radius_squared
        ]

    def find_longest_matching_prefix(
        self,
        target: str,
        filter_location_function: Optional[WordLocationsPredicate] = None,
    ) -> tuple[Sequence[Sequence[WordLocation]], int]:
        """Return a tuple of the locations of all longest matching prefixes of the
        provided words, and the length of the prefix.

        Uses fuzzy matching.
        """
        if not target:
            raise ValueError("target is empty")
        target_words_and_prefix_lengths = [
            (self._normalize(match.group()), match.end())
            for match in re.finditer(self._SUBWORD_REGEX, target)
        ]
        target_words, prefix_lengths = zip(
            *target_words_and_prefix_lengths, strict=True
        )

        last_word_sequences = []
        last_prefix_length = 0
        for prefix_num_words in range(1, len(target_words) + 1):
            target_prefix_words = target_words[:prefix_num_words]
            prefix_length = prefix_lengths[prefix_num_words - 1]
            word_sequences = self.find_matching_words(
                " ".join(target_prefix_words), match_each_word=True
            )
            if filter_location_function:
                word_sequences = list(filter(filter_location_function, word_sequences))
            if not word_sequences:
                break
            last_word_sequences = word_sequences
            last_prefix_length = prefix_length
        return last_word_sequences, last_prefix_length

    def find_longest_matching_suffix(
        self,
        target: str,
        filter_location_function: Optional[WordLocationsPredicate] = None,
    ) -> tuple[Sequence[Sequence[WordLocation]], int]:
        """Return a tuple of the locations of all longest matching suffixes of the
        provided words, and the length of the suffix.

        Uses fuzzy matching.
        """
        if not target:
            raise ValueError("target is empty")
        target_words_and_suffix_lengths = [
            (self._normalize(match.group()), len(target) - match.start())
            for match in re.finditer(self._SUBWORD_REGEX, target)
        ]
        target_words, suffix_lengths = zip(
            *target_words_and_suffix_lengths, strict=True
        )

        last_word_sequences = []
        last_suffix_length = 0
        for suffix_num_words in range(1, len(target_words) + 1):
            target_suffix_words = target_words[-suffix_num_words:]
            suffix_length = suffix_lengths[-suffix_num_words]
            word_sequences = self.find_matching_words(
                " ".join(target_suffix_words), match_each_word=True
            )
            if filter_location_function:
                word_sequences = list(filter(filter_location_function, word_sequences))
            if not word_sequences:
                break
            last_word_sequences = word_sequences
            last_suffix_length = suffix_length
        return last_word_sequences, last_suffix_length

    @staticmethod
    def _generate_candidates(
        result: _base.OcrResult, length: int, include_compound_words: bool
    ) -> Iterator[Sequence[WordLocation]]:
        for line_index, line in enumerate(result.lines):
            candidates = list(
                ScreenContents._generate_candidates_from_line(line, line_index)
            )
            if include_compound_words or length == 1:
                for candidate in candidates:
                    yield [candidate]
            if length > 1:
                yield from ScreenContents._sliding_window(candidates, length)

    @staticmethod
    def _generate_candidates_from_line(
        line: _base.OcrLine, line_index: int
    ) -> Iterator[WordLocation]:
        for word_index, word in enumerate(line.words):
            left_offset = 0
            for match in re.finditer(ScreenContents._SUBWORD_REGEX, word.text):
                subword = match.group()
                right_offset = len(word.text) - (left_offset + len(subword))
                yield WordLocation(
                    left=int(word.left),
                    top=int(word.top),
                    width=int(word.width),
                    height=int(word.height),
                    left_char_offset=left_offset,
                    right_char_offset=right_offset,
                    text=subword,
                    ocr_word_index=word_index,
                    ocr_line_index=line_index,
                )
                left_offset += len(subword)

    @staticmethod
    def _normalize(word: str) -> str:
        # Avoid any changes that affect word length.
        return word.lower().replace("\u2019", "'")

    @staticmethod
    def _normalize_homophones(
        old_homophones: Mapping[str, Iterable[str]],
    ) -> Mapping[str, Iterable[str]]:
        new_homophones = {}
        for k, v in old_homophones.items():
            new_homophones[ScreenContents._normalize(k)] = list(
                map(ScreenContents._normalize, v)
            )
        return new_homophones

    def _score_words(
        self,
        candidates: Sequence[WordLocation],
        normalized_targets: Sequence[str],
        match_each_word: bool,
    ) -> float:
        if len(candidates) == 1:
            # Handle the case where the target words are smashed together.
            score = self._score_word(candidates[0], "".join(normalized_targets))
            return score if score >= self.confidence_threshold else 0
        scores = list(map(self._score_word, candidates, normalized_targets))
        if match_each_word:
            score = min(scores)
        else:
            # Weighted average of scores based on word lengths.
            score = sum(
                score * len(word)
                for score, word in zip(scores, normalized_targets, strict=True)
            ) / sum(map(len, normalized_targets))
        return score if score >= self.confidence_threshold else 0

    def _score_word(self, candidate: WordLocation, normalized_target: str) -> float:
        candidate_text = self._normalize(candidate.text)
        homophones = self.homophones.get(normalized_target, (normalized_target,))
        best_ratio = max(
            fuzz.ratio(
                # Don't filter to full confidence threshold yet in case of multiple words.
                homophone,
                candidate_text,
                score_cutoff=self.confidence_threshold / 2 * 100,
            )
            for homophone in homophones
        )
        return best_ratio / 100.0

    @staticmethod
    def _distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
        x_dist = x1 - x2
        y_dist = y1 - y2
        return x_dist * x_dist + y_dist * y_dist

    @staticmethod
    # From https://docs.python.org/3/library/itertools.html
    def _sliding_window(iterable, n):
        # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
        it = iter(iterable)
        window = deque(islice(it, n), maxlen=n)
        if len(window) == n:
            yield tuple(window)
        for x in it:
            window.append(x)
            yield tuple(window)
