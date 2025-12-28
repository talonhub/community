import glob
import logging
import re
import sys
import time
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Literal, Optional

import numpy as np
from talon import Context, Module, actions, app, cron, fs, screen, settings, ui
from talon.canvas import Canvas, MouseEvent
from talon.skia.typeface import Fontstyle, Typeface
from talon.types import rect

from .timestamped_captures import TextRange, TimestampedText

try:
    from talon.experimental import ocr
except ImportError:
    ocr = None

# Adjust path to search adjacent package directories. Prefixed with dot to avoid
# Talon running them itself. Append to search path so that faster binary
# packages can be used instead if available.
subtree_dir = Path(__file__).parent / ".subtrees"
package_paths = [
    str(subtree_dir / "gaze-ocr"),
    str(subtree_dir / "screen-ocr"),
    str(subtree_dir / "rapidfuzz/src"),
]
saved_path = sys.path.copy()
try:
    sys.path.extend([path for path in package_paths if path not in sys.path])
    import gaze_ocr
    import screen_ocr  # dependency of gaze-ocr
    from gaze_ocr import talon_adapter
finally:
    # Restore the unmodified path.
    sys.path = saved_path.copy()

mod = Module()
ctx = Context()

mod.setting(
    "ocr_use_talon_backend",
    type=bool,
    default=True,
    desc="If true, use Talon backend, otherwise use default fast backend from screen_ocr.",
)
mod.setting(
    "ocr_connect_tracker",
    type=bool,
    default=True,
    desc="If true, automatically connect the eye tracker at startup.",
)
mod.setting(
    "ocr_logging_dir",
    type=str,
    default=None,
    desc="If specified, log OCR'ed images to this directory.",
)
mod.setting(
    "ocr_click_offset_right",
    type=int,
    default=0,
    desc="Adjust the X-coordinate when clicking around OCR text.",
)
mod.setting(
    "ocr_select_pause_seconds",
    type=float,
    default=0.5,
    desc="Adjust the pause between clicks when performing a selection.",
)
mod.setting(
    "ocr_use_window_at_api",
    type=bool,
    default=False,
    desc="Use ui.window_at() API for focusing windows (requires beta Talon). Falls back to accessibility API if disabled or unavailable.",
)
mod.setting(
    "ocr_debug_display_seconds",
    type=float,
    default=3,
    desc="Adjust how long debugging display is shown.",
)
mod.setting(
    "ocr_disambiguation_display_seconds",
    type=float,
    default=5,
    desc="Adjust how long disambiguation display is shown. Use 0 to remove timeout.",
)
mod.setting(
    "ocr_gaze_box_padding",
    type=int,
    default=100,
    desc="How much padding is applied to gaze bounding box when searching for text.",
)
mod.setting(
    "ocr_gaze_point_padding",
    type=int,
    default=200,
    desc="How much padding is applied to gaze point when taking screenshots for debug overlay commands.",
)
mod.setting(
    "ocr_light_background_debug_color",
    type=str,
    default="000000",
    desc="Debug color to use on a light background",
)
mod.setting(
    "ocr_dark_background_debug_color",
    type=str,
    default="FFFFFF",
    desc="Debug color to use on a dark background",
)
mod.setting(
    "ocr_behavior_when_no_eye_tracker",
    type=Literal["MAIN_SCREEN", "ACTIVE_WINDOW"],
    default="MAIN_SCREEN",
    desc="Region to OCR when no data from the eye tracker",
)

mod.tag(
    "gaze_ocr_disambiguation",
    desc="Tag for disambiguating between different onscreen matches.",
)
mod.list("ocr_actions", desc="Actions to perform on selected text.")
mod.list(
    "ocr_common_actions", desc="Common actions that can be used without 'seen'/'scene'."
)
mod.list("ocr_modifiers", desc="Modifiers to perform on selected text.")
mod.list("onscreen_ocr_text", desc="Selection list for onscreen text.")


def paste_link() -> None:
    actions.user.hyperlink()
    actions.sleep("100ms")
    actions.edit.paste()


def capitalize() -> None:
    text = actions.edit.selected_text()
    actions.insert(text[0].capitalize() + text[1:] if text else "")


def uncapitalize() -> None:
    text = actions.edit.selected_text()
    actions.insert(text[0].lower() + text[1:] if text else "")


_OCR_ACTIONS: dict[str, Callable[[], None]] = {
    "": lambda: None,
    "select": lambda: None,
    "copy": lambda: actions.edit.copy(),
    "cut": lambda: actions.edit.cut(),
    "paste": lambda: actions.edit.paste(),
    "paste_link": paste_link,
    "delete": lambda: actions.key("backspace"),
    "delete_with_whitespace": lambda: actions.key("backspace"),
    "capitalize": capitalize,
    "uncapitalize": uncapitalize,
    "lowercase": lambda: actions.insert(actions.edit.selected_text().lower()),
    "uppercase": lambda: actions.insert(actions.edit.selected_text().upper()),
    "bold": lambda: actions.user.bold(),
    "italic": lambda: actions.user.italic(),
    "strikethrough": lambda: actions.user.strikethrough(),
    "number_list": lambda: actions.user.number_list(),
    "bullet_list": lambda: actions.user.bullet_list(),
    "link": lambda: actions.user.hyperlink(),
}

_OCR_MODIFIERS: dict[str, Callable[[], None]] = {
    "": lambda: None,
    "selectAll": lambda: actions.edit.select_all(),
}


@ctx.dynamic_list("user.onscreen_ocr_text")
def onscreen_ocr_text(phrase) -> str | list[str] | dict[str, str]:
    global gaze_ocr_controller, punctuation_table
    reset_disambiguation()
    gaze_ocr_controller.read_nearby((phrase[0].start, phrase[-1].end))
    selection_list = gaze_ocr_controller.latest_screen_contents().as_string()
    # Split camel-casing.
    selection_list = re.sub(r"([a-z])([A-Z])", r"\1 \2", selection_list)
    # Make punctuation speakable.
    selection_list = selection_list.translate(punctuation_table)
    return selection_list


def add_homophones(
    homophones: dict[str, Sequence[str]], to_add: Iterable[Iterable[str]]
):
    for words in to_add:
        merged_words = set(words)
        for word in words:
            old_words = homophones.get(word.lower(), [])
            merged_words.update(old_words)
        merged_words = sorted(merged_words)
        for word in merged_words:
            homophones[word.lower()] = merged_words


digits = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
default_digits_map = {n: i for i, n in enumerate(digits)}

# Inline punctuation words in case people are using vanilla knausj, where these are not
# exposed. Listed in order of preference.
default_punctuation_words = {
    "back tick": "`",
    "grave": "`",
    "comma": ",",
    "period": ".",
    "full stop": ".",
    "semicolon": ";",
    "colon": ":",
    "forward slash": "/",
    "question mark": "?",
    "exclamation mark": "!",
    "exclamation point": "!",
    "asterisk": "*",
    "hash sign": "#",
    "number sign": "#",
    "percent sign": "%",
    "at sign": "@",
    "and sign": "&",
    "ampersand": "&",
    # Currencies
    "dollar sign": "$",
    "pound sign": "£",
    "hyphen": "-",
    "underscore": "_",
}


user_dir = Path(__file__).parents[1]
# Search user_dir to find homophones.csv
homophones_file = None
for path in glob.glob(str(user_dir / "**/homophones.csv"), recursive=True):
    homophones_file = path
    break
if homophones_file:
    logging.info(f"Found homophones file: {homophones_file}")
else:
    logging.warning("Could not find homophones.csv. Is knausj_talon installed?")


def get_knausj_homophones():
    phones = {}
    if not homophones_file:
        return phones
    with open(homophones_file) as f:
        for line in f:
            words = line.rstrip().split(",")
            merged_words = set(words)
            for word in words:
                old_words = phones.get(word.lower(), [])
                merged_words.update(old_words)
            merged_words = sorted(merged_words)
            for word in merged_words:
                phones[word.lower()] = merged_words
    return phones


def reload_backend(name, flags):
    # Initialize eye tracking and OCR.
    global tracker, ocr_reader, gaze_ocr_controller, punctuation_table
    tracker = talon_adapter.TalonEyeTracker()
    # Note: tracker is connected automatically in the constructor.
    if not settings.get("user.ocr_connect_tracker"):
        tracker.disconnect()
    homophones = get_knausj_homophones()
    # TODO: Get this through an action to support customization.
    add_homophones(
        homophones, [(str(num), spoken) for spoken, num in default_digits_map.items()]
    )
    # Attempt to use overridable action to get punctuation. This is available in
    # wolfmanstout_talon, but not yet in knausj_talon, so fallback if needed.
    try:
        punctuation_words = actions.user.get_punctuation_words()
    except KeyError:
        punctuation_words = default_punctuation_words
    add_homophones(
        homophones,
        [
            (punctuation, spoken.replace(" ", ""))
            for spoken, punctuation in punctuation_words.items()
        ],
    )
    # Add common OCR errors to homophones.
    add_homophones(
        homophones,
        [
            ("ok", "okay", "0k"),
            ("ally", "a11y"),
            ("AI", "Al"),
        ],
    )
    punctuation_table = str.maketrans(
        {
            punctuation: f" {spoken.replace(' ', '')} "
            for spoken, punctuation in reversed(default_punctuation_words.items())
            if len(punctuation) == 1
        }
    )
    setting_ocr_use_talon_backend = settings.get("user.ocr_use_talon_backend")
    if setting_ocr_use_talon_backend and ocr:
        ocr_reader = screen_ocr.Reader.create_reader(
            backend="talon",
            radius=settings.get("user.ocr_gaze_point_padding"),
            homophones=homophones,
        )
    else:
        if setting_ocr_use_talon_backend and not ocr:
            logging.info("Talon OCR not available, will rely on external support.")
        ocr_reader = screen_ocr.Reader.create_fast_reader(
            radius=settings.get("user.ocr_gaze_point_padding"),
            homophones=homophones,
        )
    gaze_ocr_controller = gaze_ocr.Controller(
        ocr_reader,
        tracker,
        mouse=talon_adapter.Mouse(),
        keyboard=talon_adapter.Keyboard(),
        app_actions=talon_adapter.AppActions(),
        save_data_directory=settings.get("user.ocr_logging_dir"),
        gaze_box_padding=settings.get("user.ocr_gaze_box_padding"),
        fallback_when_no_eye_tracker=gaze_ocr.EyeTrackerFallback[
            settings.get("user.ocr_behavior_when_no_eye_tracker").upper()
        ],
    )


def on_ready():
    reload_backend(None, None)
    if homophones_file:
        fs.watch(str(homophones_file), reload_backend)


app.register("ready", on_ready)


def has_light_background(screenshot):
    array = np.array(screenshot)
    # From https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert
    grayscale = 0.299 * array[:, :, 0] + 0.587 * array[:, :, 1] + 0.114 * array[:, :, 2]
    return np.mean(grayscale) > 128


def get_debug_color(has_light_background: bool):
    return (
        settings.get("user.ocr_light_background_debug_color")
        if has_light_background
        else settings.get("user.ocr_dark_background_debug_color")
    )


def calculate_optimal_text_size(
    paint, text: str, bbox_width: float, bbox_height: float
) -> float:
    """Calculate optimal font size to fit text within bounding box using Paint.measure_text().

    Uses scaling approach with existing Paint object to avoid Font creation overhead.
    Maximizes font size while ensuring text fits within both width and height constraints.

    Args:
        paint: Skia Paint object to use for measurements
        text: Text string to size
        bbox_width: Target bounding box width
        bbox_height: Target bounding box height

    Returns:
        Optimal font size as float
    """
    # Store original text size to restore later
    original_size = paint.textsize

    # Use a reasonable base size for measurement
    base_size = 16
    paint.textsize = base_size

    try:
        width, bounds = paint.measure_text(text)

        if width <= 0 or bounds.height <= 0:
            return bbox_height  # Fallback to using bbox height as font size

        # Calculate scaling factors with small safety margin (95% of available space)
        safety_factor = 0.95
        width_scale = (bbox_width * safety_factor) / width
        height_scale = (bbox_height * safety_factor) / bounds.height

        # Use the more restrictive constraint
        scale = min(width_scale, height_scale)
        optimal_size = base_size * scale

        # Ensure minimum readable size
        optimal_size = max(optimal_size, 8)

        return optimal_size

    finally:
        # Always restore original text size
        paint.textsize = original_size


disambiguation_canvas = None
debug_canvas = None
ambiguous_matches: Optional[Sequence[gaze_ocr.CursorLocation]] = None
disambiguation_generator = None


def reset_disambiguation():
    global \
        ambiguous_matches, \
        disambiguation_generator, \
        disambiguation_canvas, \
        debug_canvas
    ctx.tags = []
    ambiguous_matches = None
    disambiguation_generator = None
    hide_canvas = disambiguation_canvas or debug_canvas
    if disambiguation_canvas:
        disambiguation_canvas.close()
    disambiguation_canvas = None
    if debug_canvas:
        debug_canvas.close()
    debug_canvas = None
    if hide_canvas:
        # Ensure that the canvas doesn't interfere with subsequent screenshots.
        actions.sleep("10ms")


def show_disambiguation():
    global ambiguous_matches, disambiguation_canvas

    contents = gaze_ocr_controller.latest_screen_contents()

    def on_draw(c):
        assert ambiguous_matches
        debug_color = get_debug_color(has_light_background(contents.screenshot))
        nearest = gaze_ocr_controller.find_nearest_cursor_location(ambiguous_matches)
        used_locations = set()
        for i, match in enumerate(ambiguous_matches):
            if nearest == match:
                c.paint.typeface = Typeface.from_name(
                    "", Fontstyle.new(weight=700, width=5)
                )
            else:
                c.paint.typeface = ""
            c.paint.textsize = max(round(match.text_height * 2), 15)
            c.paint.style = c.paint.Style.FILL
            c.paint.color = debug_color
            location = (match.visual_coordinates[0], match.visual_coordinates[1])
            # TODO: Check for nearby used locations, not just identical.
            while location in used_locations:
                # Shift right.
                location = (location[0] + match.text_height, location[1])
            used_locations.add(location)
            c.draw_text(str(i + 1), *location)
        setting_ocr_disambiguation_display_seconds = settings.get(
            "user.ocr_disambiguation_display_seconds"
        )
        if setting_ocr_disambiguation_display_seconds and disambiguation_canvas:
            current_canvas = disambiguation_canvas

            def timeout_disambiguation():
                global disambiguation_canvas
                if disambiguation_canvas and disambiguation_canvas == current_canvas:
                    reset_disambiguation()

            cron.after(
                f"{setting_ocr_disambiguation_display_seconds}s",
                timeout_disambiguation,
            )

    ctx.tags = ["user.gaze_ocr_disambiguation"]
    if disambiguation_canvas:
        disambiguation_canvas.close()
    rect = screen_ocr.to_rect(contents.bounding_box)
    screen_rect = screen.main().rect
    # If rect is approximately equal to screen.main().rect, use Canvas.from_screen to
    # avoid Windows bug where the screen is blacked out.
    # https://github.com/wolfmanstout/talon-gaze-ocr/issues/47
    if (
        abs(rect.x - screen_rect.x) < 1
        and abs(rect.y - screen_rect.y) < 1
        and abs(rect.width - screen_rect.width) < 1
        and abs(rect.height - screen_rect.height) < 1
    ):
        disambiguation_canvas = Canvas.from_screen(screen.main())
    else:
        disambiguation_canvas = Canvas.from_rect(rect)
    disambiguation_canvas.register("draw", on_draw)
    disambiguation_canvas.freeze()


def begin_generator(generator):
    global ambiguous_matches, disambiguation_generator, disambiguation_canvas
    reset_disambiguation()
    try:
        ambiguous_matches = next(generator)
        disambiguation_generator = generator
        show_disambiguation()
    except StopIteration:
        # Execution completed without need for disambiguation.
        pass


def move_cursor_to_word_generator(text: TimestampedText, disambiguate: bool = True):
    result = yield from gaze_ocr_controller.move_cursor_to_words_generator(
        text.text,
        disambiguate=disambiguate,
        time_range=(text.start, text.end),
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
    )
    if not result:
        actions.user.show_ocr_overlay_for_query("text", f"{text.text}")
        raise RuntimeError(f'Unable to find: "{text}"')


def move_text_cursor_to_word_generator(
    text: TimestampedText,
    position: str,
    hold_shift: bool = False,
):
    result = yield from gaze_ocr_controller.move_text_cursor_to_words_generator(
        text.text,
        disambiguate=True,
        cursor_position=position,
        time_range=(text.start, text.end),
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
        hold_shift=hold_shift,
    )
    if not result:
        actions.user.show_ocr_overlay_for_query("text", f"{text.text}")
        raise RuntimeError(f'Unable to find: "{text}"')


def move_text_cursor_to_longest_prefix_generator(
    text: TimestampedText, position: str, hold_shift: bool = False
):
    (
        locations,
        prefix_length,
    ) = yield from gaze_ocr_controller.move_text_cursor_to_longest_prefix_generator(
        text.text,
        disambiguate=True,
        cursor_position=position,
        time_range=(text.start, text.end),
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
        hold_shift=hold_shift,
    )
    if not locations:
        actions.user.show_ocr_overlay_for_query("text", f"{text.text}")
        raise RuntimeError(f'Unable to find: "{text}"')
    return prefix_length


def move_text_cursor_to_longest_suffix_generator(
    text: TimestampedText, position: str, hold_shift: bool = False
):
    (
        locations,
        prefix_length,
    ) = yield from gaze_ocr_controller.move_text_cursor_to_longest_suffix_generator(
        text.text,
        disambiguate=True,
        cursor_position=position,
        time_range=(text.start, text.end),
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
        hold_shift=hold_shift,
    )
    if not locations:
        actions.user.show_ocr_overlay_for_query("text", f"{text.text}")
        raise RuntimeError(f'Unable to find: "{text}"')
    return prefix_length


def move_text_cursor_to_difference(text: TimestampedText):
    result = yield from gaze_ocr_controller.move_text_cursor_to_difference_generator(
        text.text,
        disambiguate=True,
        time_range=(text.start, text.end),
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
    )
    if not result:
        actions.user.show_ocr_overlay_for_query("text", f"{text.text}")
        raise RuntimeError(f'Unable to find: "{text}"')
    return result


def select_text_generator(
    start: TimestampedText,
    end: Optional[TimestampedText] = None,
    for_deletion: bool = False,
    after_start: bool = False,
    before_end: bool = False,
):
    start_text = start.text
    end_text = end.text if end else None
    result = yield from gaze_ocr_controller.select_text_generator(
        start_text,
        disambiguate=True,
        end_words=end_text,
        for_deletion=for_deletion,
        start_time_range=(start.start, start.end),
        end_time_range=(end.start, end.end) if end else None,
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
        after_start=after_start,
        before_end=before_end,
        select_pause_seconds=lambda: settings.get("user.ocr_select_pause_seconds"),
    )
    if not result:
        actions.user.show_ocr_overlay_for_query(
            "text", f"{start.text}...{end.text if end else None}"
        )
        raise RuntimeError(f'Unable to select "{start}" to "{end}"')


def select_matching_text_generator(text: TimestampedText):
    result = yield from gaze_ocr_controller.select_matching_text_generator(
        text.text,
        disambiguate=True,
        time_range=(text.start, text.end),
        click_offset_right=lambda: settings.get("user.ocr_click_offset_right"),
        select_pause_seconds=lambda: settings.get("user.ocr_select_pause_seconds"),
    )
    if not result:
        actions.user.show_ocr_overlay_for_query("text", f"{text.text}")
        raise RuntimeError(f'Unable to find: "{text}"')


def select_text_range_generator(
    text_range: TextRange,
    for_deletion: bool,
):
    if not text_range.start:
        assert text_range.end
        yield from move_text_cursor_to_word_generator(
            text_range.end,
            position="before" if text_range.before_end else "after",
            hold_shift=True,
        )
    else:
        yield from select_text_generator(
            text_range.start,
            text_range.end,
            for_deletion,
            after_start=text_range.after_start,
            before_end=text_range.before_end,
        )


def context_sensitive_insert(text: str):
    if settings.get("user.context_sensitive_dictation"):
        actions.user.dictation_insert(text)
    else:
        # Use the default insert because the dictation context is likely wrong.
        actions.insert(text)


@mod.action_class
class GazeOcrActions:
    def focus_at(x: int, y: int):
        """Focus the window at the given coordinates."""
        # Default implementation is a no-op Mac has a specific implementation that uses
        # either ui.window_at() or ui.element_at()
        # TODO: Implement for Windows/Linux once ui.window_at() is fixed on those
        # platforms Need to have at least one action for Talon to recognize this as
        # implemented
        actions.sleep("0ms")

    #
    # Actions related to the eye tracker.
    #

    def connect_ocr_eye_tracker():
        """Connects eye tracker to OCR."""
        tracker.connect()

    def disconnect_ocr_eye_tracker():
        """Disconnects eye tracker from OCR."""
        tracker.disconnect()

    #
    # Actions related to the UI.
    #

    def show_ocr_overlay(
        type: str, near: Optional[TimestampedText] = None, refresh: bool = True
    ):
        """Displays OCR debug overlay over primary screen, refreshing the OCR nearby
        where the user is looking by default.

        If the near parameter is provided, refreshes OCR nearby where the user is
        looking when they spoke the near parameter."""
        reset_disambiguation()
        if refresh:
            if near:
                gaze_ocr_controller.read_nearby((near.start, near.end))
            else:
                gaze_ocr_controller.read_nearby()
        actions.user.show_ocr_overlay_for_query(type, "", True)

    def show_ocr_overlay_for_query(
        type: str, query: str = "", persistent: bool = False
    ):
        """Display overlay over primary screen, displaying the query."""
        global debug_canvas
        if debug_canvas:
            debug_canvas.close()
            debug_canvas = None
        contents = gaze_ocr_controller.latest_screen_contents()

        contents_rect = screen_ocr.to_rect(contents.bounding_box)

        # Capture start time for synchronized fading
        start_time = time.perf_counter()

        def on_draw(c):
            light_bg = has_light_background(contents.screenshot)
            debug_color = get_debug_color(light_bg)

            if type == "text":
                # Text overlay needs opaque background with fading to be readable
                # Fade timing configuration
                fade_in_duration = 0.5  # seconds to fade in
                hold_duration = 0.5  # seconds to hold at full opacity
                fade_out_duration = 0.5  # seconds to fade out
                total_cycle_time = (
                    fade_in_duration + hold_duration + fade_out_duration
                )  # 1.5s total

                elapsed_time = time.perf_counter() - start_time
                cycle_time = elapsed_time % total_cycle_time

                # Calculate alpha (0.0 to 1.0) based on cycle position
                timeout = settings.get("user.ocr_debug_display_seconds")
                if not persistent and elapsed_time > timeout:
                    # Ensure the animation does not overrun.
                    alpha = 0.0
                elif cycle_time < fade_in_duration:
                    # Fade in: 0 to 1 over fade_in_duration
                    alpha = cycle_time / fade_in_duration
                elif cycle_time < fade_in_duration + hold_duration:
                    # Hold: stay at 1.0
                    alpha = 1.0
                else:
                    # Fade out: 1 to 0 over fade_out_duration
                    fade_start = fade_in_duration + hold_duration
                    alpha = 1.0 - ((cycle_time - fade_start) / fade_out_duration)

                # Clamp alpha to valid range
                alpha = max(0.0, min(1.0, alpha))

                bg_color = "FFFFFF" if light_bg else "000000"
                alpha_byte = int(alpha * 255)

                # Draw opaque background over the contents area with alpha
                c.paint.style = c.paint.Style.FILL
                c.paint.color = f"{bg_color}{alpha_byte:02X}"
                c.draw_rect(contents_rect)

                # Show bounding box with alpha
                c.paint.style = c.paint.Style.STROKE
                c.paint.color = f"{debug_color}{alpha_byte:02X}"
                c.draw_rect(contents_rect)

                # Draw text with alpha
                for line in contents.result.lines:
                    for word in line.words:
                        c.paint.typeface = ""
                        c.paint.textsize = calculate_optimal_text_size(
                            c.paint, word.text, word.width, word.height
                        )
                        c.paint.style = c.paint.Style.FILL
                        c.paint.color = f"{debug_color}{alpha_byte:02X}"
                        # Position baseline at ~80% down from top of OCR bounding box
                        c.draw_text(
                            word.text, word.left, word.top + (word.height * 0.8)
                        )

            elif type == "boxes":
                # Box outlines don't interfere with text, so no background or fading needed
                # Show bounding box
                c.paint.style = c.paint.Style.STROKE
                c.paint.color = debug_color
                c.draw_rect(contents_rect)

                # Draw word boxes
                for line in contents.result.lines:
                    for word in line.words:
                        c.paint.style = c.paint.Style.STROKE
                        c.paint.color = debug_color
                        c.draw_rect(
                            rect.Rect(
                                x=word.left,
                                y=word.top,
                                width=word.width,
                                height=word.height,
                            )
                        )

            else:
                raise RuntimeError(f"Type not recognized: {type}")
            if debug_canvas and not persistent:
                current_canvas = debug_canvas

                def timeout_debug_canvas():
                    global debug_canvas
                    if debug_canvas and debug_canvas == current_canvas:
                        debug_canvas.close()
                        debug_canvas = None

                cron.after(
                    f"{settings.get('user.ocr_debug_display_seconds')}s",
                    timeout_debug_canvas,
                )

        # Increased size slightly for canvas to ensure everything will be inside canvas
        canvas_rect = contents_rect.copy()
        center = canvas_rect.center
        canvas_rect.height += 100
        canvas_rect.width += 100
        canvas_rect.center = center

        debug_canvas = Canvas.from_rect(canvas_rect)
        debug_canvas.blocks_mouse = True
        debug_canvas.register("draw", on_draw)

        def on_mouse(e: MouseEvent):
            global debug_canvas
            if e.event == "mousedown" and debug_canvas:  # Any mouse button click
                debug_canvas.close()
                debug_canvas = None

        debug_canvas.register("mouse", on_mouse)

    def hide_ocr_overlay():
        """Hide any visible OCR overlay."""
        global debug_canvas
        if debug_canvas:
            debug_canvas.close()
            debug_canvas = None

    def choose_gaze_ocr_option(index: int):
        """Disambiguate with the provided index."""
        global ambiguous_matches, disambiguation_generator, disambiguation_canvas
        if (
            not ambiguous_matches
            or not disambiguation_generator
            or not disambiguation_canvas
        ):
            assert not ambiguous_matches
            assert not disambiguation_generator
            assert not disambiguation_canvas
            raise RuntimeError("Disambiguation not active")
        ctx.tags = []
        disambiguation_canvas.close()
        disambiguation_canvas = None
        # Give the canvas a moment to disappear so it doesn't interfere with subsequent screenshots.
        actions.sleep("10ms")
        match = ambiguous_matches[index - 1]
        try:
            ambiguous_matches = disambiguation_generator.send(match)
            show_disambiguation()
        except StopIteration:
            # Execution completed successfully.
            reset_disambiguation()

    def hide_gaze_ocr_options():
        """Hide the disambiguation UI."""
        reset_disambiguation()

    #
    # Actions operating on the gaze point.
    #

    def move_cursor_to_gaze_point(offset_right: int = 0, offset_down: int = 0):
        """Moves mouse cursor to gaze location."""
        tracker.move_to_gaze_point((offset_right, offset_down))

    #
    # Actions operating on a single point within onscreen text.
    #

    def move_cursor_to_word(text: TimestampedText):
        """Moves cursor to onscreen word."""
        begin_generator(move_cursor_to_word_generator(text))

    def move_text_cursor_to_word(
        text: TimestampedText,
        position: str,
    ):
        """Moves text cursor near onscreen word."""
        begin_generator(move_text_cursor_to_word_generator(text, position))

    def insert_adjacent_to_text(
        find_text: TimestampedText, position: str, insertion_text: str
    ):
        """Insert text adjacent to onscreen text."""

        def run():
            yield from move_text_cursor_to_word_generator(
                find_text,
                position,
            )
            context_sensitive_insert(insertion_text)

        begin_generator(run())

    def move_cursor_to_text_and_do(
        text: TimestampedText, action: Callable[[], None], disambiguate: bool = True
    ) -> None:
        """Moves cursor to onscreen word and performs an action."""

        def run():
            yield from move_cursor_to_word_generator(text, disambiguate)
            action()

        begin_generator(run())

    def click_text(text: TimestampedText):
        """Click on the provided on-screen text."""
        actions.user.move_cursor_to_text_and_do(text, lambda: actions.mouse_click())

    def click_text_without_disambiguation(text: TimestampedText):
        """Click on the provided on-screen text, choosing the best match if multiple are
        found."""
        actions.user.move_cursor_to_text_and_do(
            text, lambda: actions.mouse_click(), disambiguate=False
        )

    def double_click_text(text: TimestampedText):
        """Double-lick on the provided on-screen text."""

        def double_click() -> None:
            actions.mouse_click()
            actions.mouse_click()

        actions.user.move_cursor_to_text_and_do(text, double_click)

    def triple_click_text(text: TimestampedText):
        """Triple-click on the provided on-screen text."""

        def triple_click() -> None:
            actions.mouse_click()
            actions.mouse_click()
            actions.mouse_click()

        actions.user.move_cursor_to_text_and_do(text, triple_click)

    def right_click_text(text: TimestampedText):
        """Right-click on the provided on-screen text."""
        actions.user.move_cursor_to_text_and_do(text, lambda: actions.mouse_click(1))

    def middle_click_text(text: TimestampedText):
        """Middle-click on the provided on-screen text."""
        actions.user.move_cursor_to_text_and_do(text, lambda: actions.mouse_click(2))

    def modifier_click_text(modifier: str, text: TimestampedText):
        """Control-click on the provided on-screen text."""

        def click_with_modifier() -> None:
            actions.key(f"{modifier}:down")
            actions.mouse_click()
            actions.key(f"{modifier}:up")

        actions.user.move_cursor_to_text_and_do(text, click_with_modifier)

    def change_text_homophone(text: TimestampedText):
        """Switch the on-screen text to a different homophone."""

        def change_homophone() -> None:
            actions.mouse_click()
            actions.edit.select_word()
            actions.user.homophones_show_selection()

        actions.user.move_cursor_to_text_and_do(text, change_homophone)

    #
    # Actions operating on a selection of onscreen text.
    #

    def select_text_and_do(
        text_range: TextRange,
        for_deletion: bool,
        ocr_modifier: str,
        action: Callable[[], None],
    ) -> None:
        """Selects text and performs an action."""
        if ocr_modifier not in _OCR_MODIFIERS:
            raise ValueError(f"Modifier not supported: {ocr_modifier}")

        def run():
            yield from select_text_range_generator(text_range, for_deletion)
            _OCR_MODIFIERS[ocr_modifier]()
            action()

        begin_generator(run())

    def perform_ocr_action(
        ocr_action: str,
        ocr_modifier: str,
        text_range: TextRange,
    ) -> None:
        """Selects text and performs a known action by name."""
        if ocr_action not in _OCR_ACTIONS:
            raise ValueError(f"Action not supported: {ocr_action}")

        actions.user.select_text_and_do(
            text_range=text_range,
            for_deletion=(ocr_action in ("cut", "delete_with_whitespace")),
            ocr_modifier=ocr_modifier,
            action=_OCR_ACTIONS[ocr_action],
        )

    def replace_text(ocr_modifier: str, text_range: TextRange, replacement: str):
        """Replaces onscreen text."""
        actions.user.select_text_and_do(
            text_range=text_range,
            for_deletion=settings.get("user.context_sensitive_dictation"),
            ocr_modifier=ocr_modifier,
            action=lambda: context_sensitive_insert(replacement),
        )

    #
    # Actions providing natural text editing.
    #

    def append_text(text: TimestampedText):
        """Finds onscreen text that matches the beginning of the provided text and
        appends the rest to it."""

        def run():
            prefix_length = yield from move_text_cursor_to_longest_prefix_generator(
                text, "after"
            )
            insertion_text = text.text[prefix_length:]
            context_sensitive_insert(insertion_text)

        begin_generator(run())

    def prepend_text(text: TimestampedText):
        """Finds onscreen text that matches the end of the provided text and
        prepends the rest to it."""

        def run():
            suffix_length = yield from move_text_cursor_to_longest_suffix_generator(
                text, "before"
            )
            insertion_text = text.text[:-suffix_length]
            context_sensitive_insert(insertion_text)

        begin_generator(run())

    def insert_text_difference(text: TimestampedText):
        """Finds onscreen text that matches the start and/or end of the provided text
        and inserts the difference."""

        def run():
            start, end = yield from move_text_cursor_to_difference(text)
            insertion_text = text.text[start:end]
            context_sensitive_insert(insertion_text)

        begin_generator(run())

    def revise_text(text: TimestampedText):
        """Finds onscreen text that matches the beginning and end of the provided text
        and replaces it."""

        def run():
            yield from select_matching_text_generator(text)
            insertion_text = text.text
            context_sensitive_insert(insertion_text)

        begin_generator(run())

    def revise_text_starting_with(text: TimestampedText):
        """Finds onscreen text that matches the beginning of the provided text
        and replaces it until the caret."""

        def run():
            try:
                yield from move_text_cursor_to_longest_prefix_generator(
                    text, "before", hold_shift=True
                )
            except RuntimeError as e:
                # Keep going so the user doesn't lose the dictated text.
                print(e)
            insertion_text = text.text
            context_sensitive_insert(insertion_text)

        begin_generator(run())

    def revise_text_ending_with(text: TimestampedText):
        """Finds onscreen text that matches the end of the provided text and
        replaces it from the caret."""

        def run():
            try:
                yield from move_text_cursor_to_longest_suffix_generator(
                    text, "after", hold_shift=True
                )
            except RuntimeError as e:
                # Keep going so the user doesn't lose the dictated text.
                print(e)
            insertion_text = text.text
            context_sensitive_insert(insertion_text)

        begin_generator(run())


def focus_element_window(element) -> bool:
    """Focuses the window containing the accessibility element."""
    try:
        ax_window = element.AXWindow
    except AttributeError:
        # Assume the current element is the window.
        ax_window = element

    try:
        ax_app = ax_window.AXParent
    except AttributeError:
        return False

    if ax_app.AXRole != "AXApplication":
        return False

    # Raise the window to the top.
    try:
        ax_window.perform("AXRaise")
    except Exception:
        return False

    # Focus the application. Check if it is already focused first to avoid
    # unnecessary impact on window ordering.
    if not ax_app.AXFrontmost:
        ax_app.AXFrontmost = True
    return True


# Mac-specific implementation that focuses windows at coordinates
ctx_mac = Context()
ctx_mac.matches = "os: mac"


@ctx_mac.action_class("user")
class MacGazeOcrActions:
    def focus_at(x: int, y: int):
        """Focus the window at the given coordinates on Mac."""
        use_window_at = settings.get("user.ocr_use_window_at_api")
        if use_window_at:
            # Attempt to turn off HUD if talon_hud is installed.
            try:
                actions.user.hud_set_visibility(False, pause_seconds=0)
            except Exception:
                pass
            # Use window_at API (requires beta Talon)
            try:
                window = ui.window_at(x, y)
            except (RuntimeError, AttributeError):
                # No window at this position
                logging.debug(f"No window at position ({x}, {y}); skipping focus.")
                return
            finally:
                # Attempt to turn on HUD if talon_hud is installed.
                try:
                    actions.user.hud_set_visibility(True, pause_seconds=0)
                except Exception:
                    pass

            # Focus the window if not already active
            if ui.active_window() != window:
                if window.title == "Notification Center":
                    app.notify(
                        "Unable to focus window with notifications active. Please dismiss notifications."
                    )
                    return
                window.focus()
                start_time = time.perf_counter()
                while ui.active_window() != window:
                    if time.perf_counter() - start_time > 1:
                        logging.warning(
                            f"Can't focus window: {window.title}. Proceeding anyway."
                        )
                        break
                    actions.sleep(0.1)
        else:
            # Use element_at API (works on older Talon versions)
            try:
                element = ui.element_at(x, y)
            except RuntimeError:
                logging.debug(f"No element at position ({x}, {y}); skipping focus.")
                return

            if not focus_element_window(element):
                # This can happen when clicking on the desktop or menu bar.
                logging.debug(
                    f"Unable to focus window for element {element}; skipping focus."
                )
