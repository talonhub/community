"""Library for manipulating on-screen text using gaze tracking and OCR.

Supports disambiguation using Python generators to stop and resume computation. The *_generator
functions return a generator which can be started with next(generator), which will return a list of
matches if disambiguation is needed. Resume computation with generator.send(match). When computation
completes, next() or send() will raise StopIteration with the .value set to the return value.
"""

import os.path
import time
from collections.abc import Callable, Generator, Sequence
from concurrent import futures
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional

from screen_ocr import Reader, ScreenContents, WordLocation


@dataclass
class CursorLocation:
    click_coordinates: tuple[int, int]
    visual_coordinates: tuple[int, int]
    # Move cursor to the right if True, left if False.
    move_cursor_right: bool
    move_distance: int
    move_past_whitespace_left: bool
    move_past_whitespace_right: bool
    text_height: int

    mouse: Any = field(repr=False, compare=False)
    keyboard: Any = field(repr=False, compare=False)
    app_actions: Any = field(repr=False, compare=False)

    def move_mouse_cursor(self):
        self.mouse.move(self.click_coordinates)

    def move_text_cursor(self):
        self.mouse.move(self.click_coordinates)
        self.mouse.click()
        # Needed to avoid selection issues on Mac.
        time.sleep(0.01)
        if self.move_distance:
            if self.move_cursor_right:
                self.keyboard.right(self.move_distance)
            else:
                self.keyboard.left(self.move_distance)
        if (
            self.move_past_whitespace_left
            and not self.keyboard.is_shift_down()
            and self.app_actions
        ):
            left_chars = self.app_actions.peek_left()
            # Check that there is actually a space adjacent (not a newline). Google docs
            # represents a newline as newline followed by space, so we handle that case as
            # well.
            if (
                len(left_chars) >= 2
                and left_chars[-1] == " "
                and left_chars[-2] != "\n"
            ):
                self.keyboard.left(1)
        if (
            self.move_past_whitespace_right
            and not self.keyboard.is_shift_down()
            and self.app_actions
        ):
            right_chars = self.app_actions.peek_right()
            if right_chars and right_chars[0] == " ":
                self.keyboard.right(1)


class EyeTrackerFallback(Enum):
    MAIN_SCREEN = auto()
    ACTIVE_WINDOW = auto()


class OcrCache:
    def __init__(
        self,
        ocr_reader: Reader,
        fallback_when_no_eye_tracker: EyeTrackerFallback = EyeTrackerFallback.MAIN_SCREEN,
    ):
        self.ocr_reader = ocr_reader
        self._last_time_range = None
        self._last_screen_contents = None
        self.fallback_when_no_eye_tracker = fallback_when_no_eye_tracker

    def read(
        self,
        time_range: tuple[float, float],
        bounding_box: Optional[tuple[int, int, int, int]],
    ):
        if (
            self._last_time_range
            and time_range[0] >= self._last_time_range[0]
            and time_range[1] <= self._last_time_range[1]
        ):
            # Assume that bounding box is a subset if the time range is a subset.
            # Don't update the cache, in case multiple subsets are requested.
            if bounding_box:
                return self._last_screen_contents.cropped(bounding_box)
            else:
                return self._last_screen_contents
        else:
            self._last_time_range = time_range
            if bounding_box:
                self._last_screen_contents = self.ocr_reader.read_screen(bounding_box)
            else:
                if (
                    self.fallback_when_no_eye_tracker
                    == EyeTrackerFallback.ACTIVE_WINDOW
                ):
                    self._last_screen_contents = self.ocr_reader.read_current_window()
                else:
                    self._last_screen_contents = self.ocr_reader.read_screen()
            return self._last_screen_contents


class Controller:
    """Mediates interaction with gaze tracking and OCR.

    Provide Mouse and Keyboard from gaze_ocr.dragonfly or gaze_ocr.talon. AppActions is optional.
    """

    WordLocationsPredicate = Callable[[Sequence[WordLocation]], bool]

    class SelectionPosition(Enum):
        NONE = auto()
        LEFT = auto()
        RIGHT = auto()

    def __init__(
        self,
        ocr_reader: Reader,
        eye_tracker,
        mouse,
        keyboard,
        app_actions=None,
        save_data_directory: Optional[str] = None,
        gaze_box_padding: int = 100,
        fallback_when_no_eye_tracker: EyeTrackerFallback = EyeTrackerFallback.MAIN_SCREEN,
    ):
        self.ocr_reader = ocr_reader
        self.eye_tracker = eye_tracker
        self.mouse = mouse
        self.keyboard = keyboard
        self.app_actions = app_actions
        self.save_data_directory = save_data_directory
        self.gaze_box_padding = gaze_box_padding
        self._change_radius = 10
        self._executor = futures.ThreadPoolExecutor(max_workers=1)
        self._future = None
        self._ocr_cache = OcrCache(
            ocr_reader, fallback_when_no_eye_tracker=fallback_when_no_eye_tracker
        )
        self.fallback_when_no_eye_tracker = fallback_when_no_eye_tracker

    def shutdown(self, wait=True):
        self._executor.shutdown(wait)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False

    def start_reading_nearby(self) -> None:
        """Start OCR nearby the gaze point in a background thread."""
        gaze_point = (
            self.eye_tracker.get_gaze_point()
            if self.eye_tracker and self.eye_tracker.is_connected
            else None
        )
        # Don't enqueue multiple requests.
        if self._future and not self._future.done():
            self._future.cancel()
        self._future = self._executor.submit(
            (lambda: self.ocr_reader.read_nearby(gaze_point))
            if gaze_point
            else (lambda: self.ocr_reader.read_screen())
        )

    def read_nearby(
        self,
        time_range: Optional[tuple[float, float]] = None,
    ) -> None:
        """Perform OCR nearby the gaze point in the current thread.

        Arguments:
        time_range: If specified, read within the bounds of gaze during that time.
        """
        self._future = futures.Future()
        if time_range and time_range[0] and time_range[1]:
            start_timestamp, end_timestamp = time_range
            # Pad the range to account for timestamp inaccuracy.
            gaze_bounds = (
                self.eye_tracker.get_gaze_bounds_during_time_range(
                    start_timestamp - 0.1, end_timestamp + 0.1
                )
                if self.eye_tracker and self.eye_tracker.is_connected
                else None
            )
            if not gaze_bounds:
                self._future.set_result(
                    self._ocr_cache.read((start_timestamp, end_timestamp), None)
                )
                return
            ocr_bounds = (
                gaze_bounds.left - self.gaze_box_padding,
                gaze_bounds.top - self.gaze_box_padding,
                gaze_bounds.right + self.gaze_box_padding,
                gaze_bounds.bottom + self.gaze_box_padding,
            )
            self._future.set_result(
                self._ocr_cache.read((start_timestamp, end_timestamp), ocr_bounds)
            )
        else:
            gaze_point = (
                self.eye_tracker.get_gaze_point()
                if self.eye_tracker and self.eye_tracker.is_connected
                else None
            )
            if gaze_point:
                self._future.set_result(self.ocr_reader.read_nearby(gaze_point))
            else:
                if (
                    self.fallback_when_no_eye_tracker
                    == EyeTrackerFallback.ACTIVE_WINDOW
                ):
                    self._future.set_result(self.ocr_reader.read_current_window())
                else:
                    self._future.set_result(self.ocr_reader.read_screen())

    def latest_screen_contents(self) -> ScreenContents:
        """Return the ScreenContents of the latest call to start_reading_nearby().

        Blocks until available.
        """
        if not self._future:
            raise RuntimeError(
                "Call start_reading_nearby() before latest_screen_contents()"
            )
        return self._future.result()

    def move_cursor_to_words(
        self,
        words: str,
        cursor_position: str = "middle",
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
    ) -> Optional[tuple[int, int]]:
        """Move the mouse cursor nearby the specified word or words.

        If successful, returns the new cursor coordinates.

        Arguments:
        words: The word or words to search for.
        cursor_position: "before", "middle", or "after" (relative to the matching word)
        time_range: If specified, read within the bounds of gaze during that time.
        click_offset_right: Adjust the X-coordinate when clicking.
        """
        return self._extract_result(
            self.move_cursor_to_words_generator(
                words,
                disambiguate=False,
                cursor_position=cursor_position,
                time_range=time_range,
                click_offset_right=click_offset_right,
            )
        )

    def move_cursor_to_words_generator(
        self,
        words: str,
        disambiguate: bool,
        cursor_position: str = "middle",
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
    ) -> Generator[Sequence[CursorLocation], CursorLocation, Optional[tuple[int, int]]]:
        """Same as move_cursor_to_words, except it supports disambiguation through a generator.
        See header comment for details.
        """
        if time_range:
            self.read_nearby(time_range)
        screen_contents = self.latest_screen_contents()
        matches = screen_contents.find_matching_words(words)
        self._write_data(screen_contents, words, matches)
        cursor_locations = []
        for locations in matches:
            if cursor_position == "before":
                coordinates = locations[0].start_coordinates
            elif cursor_position == "middle":
                coordinates = (
                    int((locations[0].left + locations[-1].right) / 2),
                    int((locations[0].top + locations[-1].bottom) / 2),
                )
            elif cursor_position == "after":
                coordinates = locations[-1].end_coordinates
            else:
                raise ValueError(cursor_position)
            click_coordinates = self._apply_click_offset(
                coordinates, click_offset_right
            )
            cursor_locations.append(
                CursorLocation(
                    click_coordinates=click_coordinates,
                    visual_coordinates=click_coordinates,
                    move_cursor_right=False,
                    move_distance=0,
                    move_past_whitespace_left=False,
                    move_past_whitespace_right=False,
                    text_height=locations[0].height,
                    mouse=self.mouse,
                    keyboard=self.keyboard,
                    app_actions=self.app_actions,
                )
            )
        location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=cursor_locations,
        )
        if not location:
            return None
        location.move_mouse_cursor()
        return location.click_coordinates

    move_cursor_to_word = move_cursor_to_words

    def move_text_cursor_to_words(
        self,
        words: str,
        cursor_position: str = "middle",
        filter_location_function: Optional[WordLocationsPredicate] = None,
        include_whitespace: bool = False,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
    ) -> Optional[CursorLocation]:
        """Move the text cursor nearby the specified word or phrase.

        If successful, returns list of screen_ocr.WordLocation of the matching words.

        Arguments:
        words: The word or phrase to search for.
        cursor_position: "before", "middle", or "after" (relative to the matching word).
        filter_location_function: Given a sequence of word locations, return whether to proceed with
                                    cursor movement.
        include_whitespace: Include whitespace adjacent to the words.
        time_range: If specified, read within the bounds of gaze during that time.
        click_offset_right: Adjust the X-coordinate when clicking.
        """
        return self._extract_result(
            self.move_text_cursor_to_words_generator(
                words,
                disambiguate=False,
                cursor_position=cursor_position,
                filter_location_function=filter_location_function,
                include_whitespace=include_whitespace,
                time_range=time_range,
                click_offset_right=click_offset_right,
            )
        )

    def move_text_cursor_to_words_generator(
        self,
        words: str,
        disambiguate: bool,
        cursor_position: str = "middle",
        filter_location_function: Optional[WordLocationsPredicate] = None,
        include_whitespace: bool = False,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        hold_shift: bool = False,
        selection_position: Optional[SelectionPosition] = None,
    ) -> Generator[Sequence[CursorLocation], CursorLocation, Optional[CursorLocation]]:
        """Same as move_text_cursor_to_words, except it supports disambiguation through a generator.
        See header comment for details.
        """
        if time_range:
            self.read_nearby(time_range)
        screen_contents = self.latest_screen_contents()
        matches = screen_contents.find_matching_words(words)
        if filter_location_function:
            matches = list(filter(filter_location_function, matches))
        self._write_data(screen_contents, words, matches)
        if not selection_position:
            # Guess the selection position.
            if not hold_shift:
                selection_position = self.SelectionPosition.NONE
            elif cursor_position == "before":
                selection_position = self.SelectionPosition.LEFT
            elif cursor_position == "after":
                selection_position = self.SelectionPosition.RIGHT
            else:
                selection_position = self.SelectionPosition.NONE
        locations = self._plan_cursor_locations(
            matches,
            cursor_position=cursor_position,
            include_whitespace=include_whitespace,
            click_offset_right=click_offset_right,
            selection_position=selection_position,
        )
        location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=locations,
        )
        if not location:
            return None
        if hold_shift:
            self.keyboard.shift_down()
        try:
            location.move_text_cursor()
        finally:
            if hold_shift:
                self.keyboard.shift_up()
        return location

    move_text_cursor_to_word = move_text_cursor_to_words

    def move_text_cursor_to_longest_prefix(
        self,
        words: str,
        cursor_position: str = "middle",
        filter_location_function: Optional[WordLocationsPredicate] = None,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        hold_shift: bool = False,
    ) -> tuple[Optional[CursorLocation], int]:
        """Moves the text cursor to the longest prefix of the provided words that
        matches onscreen text. See move_text_cursor_to_words for argument details."""
        return self._extract_result(
            self.move_text_cursor_to_longest_prefix_generator(
                words,
                disambiguate=False,
                cursor_position=cursor_position,
                filter_location_function=filter_location_function,
                time_range=time_range,
                click_offset_right=click_offset_right,
                hold_shift=hold_shift,
            )
        )

    def move_text_cursor_to_longest_prefix_generator(
        self,
        words: str,
        disambiguate: bool,
        cursor_position: str = "middle",
        filter_location_function: Optional[WordLocationsPredicate] = None,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        hold_shift: bool = False,
    ) -> Generator[
        Sequence[CursorLocation], CursorLocation, tuple[Optional[CursorLocation], int]
    ]:
        """Same as move_text_cursor_to_longest_prefix, except it supports
        disambiguation through a generator. See header comment for details."""
        if time_range:
            self.read_nearby(time_range)
        screen_contents = self.latest_screen_contents()
        matches, prefix_length = screen_contents.find_longest_matching_prefix(
            words, filter_location_function=filter_location_function
        )
        self._write_data(screen_contents, words, matches)
        # Guess the selection position.
        selection_position = (
            self.SelectionPosition.LEFT if hold_shift else self.SelectionPosition.NONE
        )
        locations = self._plan_cursor_locations(
            matches,
            cursor_position=cursor_position,
            include_whitespace=False,
            click_offset_right=click_offset_right,
            selection_position=selection_position,
        )
        location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=locations,
        )
        if not location:
            return None, 0
        if hold_shift:
            self.keyboard.shift_down()
        try:
            location.move_text_cursor()
        finally:
            if hold_shift:
                self.keyboard.shift_up()
        return location, prefix_length

    def move_text_cursor_to_longest_suffix(
        self,
        words: str,
        cursor_position: str = "middle",
        filter_location_function: Optional[WordLocationsPredicate] = None,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        hold_shift: bool = False,
    ) -> tuple[Optional[CursorLocation], int]:
        """Moves the text cursor to the longest suffix of the provided words that
        matches onscreen text. See move_text_cursor_to_words for argument details."""
        return self._extract_result(
            self.move_text_cursor_to_longest_suffix_generator(
                words,
                disambiguate=False,
                cursor_position=cursor_position,
                filter_location_function=filter_location_function,
                time_range=time_range,
                click_offset_right=click_offset_right,
                hold_shift=hold_shift,
            )
        )

    def move_text_cursor_to_longest_suffix_generator(
        self,
        words: str,
        disambiguate: bool,
        cursor_position: str = "middle",
        filter_location_function: Optional[WordLocationsPredicate] = None,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        hold_shift: bool = False,
    ) -> Generator[
        Sequence[CursorLocation], CursorLocation, tuple[Optional[CursorLocation], int]
    ]:
        """Same as move_text_cursor_to_longest_suffix, except it supports
        disambiguation through a generator. See header comment for details."""
        if time_range:
            self.read_nearby(time_range)
        screen_contents = self.latest_screen_contents()
        matches, suffix_length = screen_contents.find_longest_matching_suffix(
            words, filter_location_function=filter_location_function
        )
        self._write_data(screen_contents, words, matches)
        # Guess the selection position.
        selection_position = (
            self.SelectionPosition.RIGHT if hold_shift else self.SelectionPosition.NONE
        )
        locations = self._plan_cursor_locations(
            matches,
            cursor_position=cursor_position,
            include_whitespace=False,
            click_offset_right=click_offset_right,
            selection_position=selection_position,
        )
        location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=locations,
        )
        if not location:
            return None, 0
        if hold_shift:
            self.keyboard.shift_down()
        try:
            location.move_text_cursor()
        finally:
            if hold_shift:
                self.keyboard.shift_up()
        return location, suffix_length

    def move_text_cursor_to_difference_generator(
        self,
        words: str,
        disambiguate: bool,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
    ) -> Generator[Sequence[CursorLocation], CursorLocation, Optional[tuple[int, int]]]:
        """Finds onscreen text that matches the start and/or end of the provided words,
        and moves the text cursor to the start of where the words differ. Returns the
        start and end indices of the differing text in the provided words, if found."""
        if time_range:
            self.read_nearby(time_range)
        screen_contents = self.latest_screen_contents()
        prefix_matches, prefix_length = screen_contents.find_longest_matching_prefix(
            words
        )
        suffix_matches, suffix_length = screen_contents.find_longest_matching_suffix(
            words
        )
        matches = list(prefix_matches) + list(suffix_matches)
        self._write_data(screen_contents, words, matches)
        # Find any pairs of matches that are adjacent onscreen. Track whether there is
        # whitespace between the pairs.
        adjacent_prefix_matches = []
        whitespace_between_matches_list = []
        for prefix_match in prefix_matches:
            for suffix_match in suffix_matches:
                if prefix_match[-1].is_adjacent_left_of(
                    suffix_match[0], allow_whitespace=True
                ):
                    adjacent_prefix_matches.append(prefix_match)
                    whitespace_between_matches_list.append(
                        not prefix_match[-1].is_adjacent_left_of(
                            suffix_match[0], allow_whitespace=False
                        )
                    )

        if adjacent_prefix_matches:
            locations = self._plan_cursor_locations(
                adjacent_prefix_matches,
                cursor_position="after",
                include_whitespace=False,
                click_offset_right=click_offset_right,
                selection_position=self.SelectionPosition.NONE,
            )
        else:
            prefix_locations = self._plan_cursor_locations(
                prefix_matches,
                cursor_position="after",
                include_whitespace=False,
                click_offset_right=click_offset_right,
                selection_position=self.SelectionPosition.NONE,
            )
            suffix_locations = self._plan_cursor_locations(
                suffix_matches,
                cursor_position="before",
                include_whitespace=False,
                click_offset_right=click_offset_right,
                selection_position=self.SelectionPosition.NONE,
            )
            locations = list(prefix_locations) + list(suffix_locations)
        location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=locations,
        )
        if not location:
            return None
        location.move_text_cursor()
        if adjacent_prefix_matches:
            whitespace_between_matches = whitespace_between_matches_list[
                locations.index(location)
            ]
            if whitespace_between_matches and words[-suffix_length - 1] == " ":
                return (prefix_length, len(words) - suffix_length - 1)
            else:
                return (prefix_length, len(words) - suffix_length)
        elif location in prefix_locations:
            return (prefix_length, len(words))
        else:
            assert location in suffix_locations
            return (0, len(words) - suffix_length)

    def select_text(
        self,
        start_words: str,
        end_words: Optional[str] = None,
        for_deletion: bool = False,
        start_time_range: Optional[tuple[float, float]] = None,
        end_time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        after_start: bool = False,
        before_end: bool = False,
    ) -> Optional[CursorLocation]:
        """Select a range of onscreen text.

        If only start_words is provided, the full word or phrase is selected. If
        end_word is provided, a range from the start words to end words will be
        selected.

        Arguments:
        for_deletion: If True, select adjacent whitespace for clean deletion of
                      the selected text.
        start_time_range: If specified, search for start_words within the bounds of gaze during that time.
        end_time_range: If specified, search for end_words within the bounds of gaze during that time.
        click_offset_right: Adjust the X-coordinate when clicking.
        after_start: If true, begin selection after the start word.
        before_end: If true, end selection before the end word.
        """
        return self._extract_result(
            self.select_text_generator(
                start_words,
                disambiguate=False,
                end_words=end_words,
                for_deletion=for_deletion,
                start_time_range=start_time_range,
                end_time_range=end_time_range,
                click_offset_right=click_offset_right,
                after_start=after_start,
                before_end=before_end,
            )
        )

    def select_text_generator(
        self,
        start_words: str,
        disambiguate: bool,
        end_words: Optional[str] = None,
        for_deletion: bool = False,
        start_time_range: Optional[tuple[float, float]] = None,
        end_time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        after_start: bool = False,
        before_end: bool = False,
        select_pause_seconds: float = 0.01,
    ) -> Generator[Sequence[CursorLocation], CursorLocation, Optional[CursorLocation]]:
        """Same as select_text, except it supports disambiguation through a generator.
        See header comment for details.
        """
        if start_time_range:
            self.read_nearby(start_time_range)
        screen_contents = self.latest_screen_contents()
        start_matches = screen_contents.find_matching_words(start_words)
        self._write_data(screen_contents, start_words, start_matches)
        start_locations = self._plan_cursor_locations(
            start_matches,
            cursor_position="after" if after_start else "before",
            include_whitespace=for_deletion and not after_start,
            click_offset_right=click_offset_right,
            selection_position=self.SelectionPosition.LEFT,
        )
        start_location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=start_locations,
        )
        if not start_location:
            return None
        start_location.move_text_cursor()
        time.sleep(select_pause_seconds)
        if end_words:
            if end_time_range:
                self.read_nearby(end_time_range)
            else:
                self._read_nearby_if_gaze_moved()

            def filter_function(location):
                return self._is_valid_selection(
                    start_location.click_coordinates, location[-1].end_coordinates
                )

            return (
                yield from self.move_text_cursor_to_words_generator(
                    end_words,
                    disambiguate=disambiguate,
                    cursor_position="before" if before_end else "after",
                    filter_location_function=filter_function,
                    include_whitespace=False,
                    click_offset_right=click_offset_right,
                    hold_shift=True,
                    selection_position=self.SelectionPosition.RIGHT,
                )
            )
        else:
            # Select until the end of the start_words match.
            end_match = start_matches[start_locations.index(start_location)]
            end_location = self._plan_cursor_location(
                end_match,
                cursor_position="before" if before_end else "after",
                include_whitespace=False,
                click_offset_right=click_offset_right,
                selection_position=self.SelectionPosition.RIGHT,
            )
            self.keyboard.shift_down()
            try:
                end_location.move_text_cursor()
            finally:
                self.keyboard.shift_up()
            return end_location

    def select_matching_text(
        self,
        words: str,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
    ) -> Optional[tuple[int, int]]:
        """Selects onscreen text that matches the beginning and/or end of the provided
        text. Returns the start and end indices corresponding to the changed text, if
        found. See select_text for argument details."""
        return self._extract_result(
            self.select_matching_text_generator(
                words,
                disambiguate=False,
                time_range=time_range,
                click_offset_right=click_offset_right,
            )
        )

    def select_matching_text_generator(
        self,
        words: str,
        disambiguate: bool,
        time_range: Optional[tuple[float, float]] = None,
        click_offset_right: int = 0,
        select_pause_seconds: float = 0.01,
    ) -> Generator[Sequence[CursorLocation], CursorLocation, Optional[tuple[int, int]]]:
        """Same as select_matching_text, except it supports disambiguation through a
        generator. See header comment for details."""
        if time_range:
            self.read_nearby(time_range)
        screen_contents = self.latest_screen_contents()
        prefix_matches, prefix_length = screen_contents.find_longest_matching_prefix(
            words
        )
        before_prefix_locations = self._plan_cursor_locations(
            prefix_matches,
            cursor_position="before",
            include_whitespace=False,
            click_offset_right=click_offset_right,
            selection_position=self.SelectionPosition.LEFT,
        )
        before_prefix_location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=before_prefix_locations,
        )
        if before_prefix_location:
            before_prefix_location.move_text_cursor()
            time.sleep(select_pause_seconds)
        if not time_range:
            self._read_nearby_if_gaze_moved()
            screen_contents = self.latest_screen_contents()
        if before_prefix_location:

            def filter_function(location):
                return self._is_valid_selection(
                    before_prefix_location.click_coordinates,
                    location[-1].end_coordinates,
                )
        else:
            filter_function = None
        suffix_matches, suffix_length = screen_contents.find_longest_matching_suffix(
            words, filter_location_function=filter_function
        )
        after_suffix_locations = self._plan_cursor_locations(
            suffix_matches,
            cursor_position="after",
            include_whitespace=False,
            click_offset_right=click_offset_right,
            selection_position=self.SelectionPosition.RIGHT,
        )
        after_suffix_location = yield from self._choose_cursor_location(
            disambiguate=disambiguate,
            matches=after_suffix_locations,
        )
        if before_prefix_location and after_suffix_location:
            self.keyboard.shift_down()
            try:
                after_suffix_location.move_text_cursor()
            finally:
                self.keyboard.shift_up()
            return (prefix_length, len(words) - suffix_length)
        elif not before_prefix_location and not after_suffix_location:
            return None
        elif before_prefix_location:
            assert not after_suffix_location
            prefix_match = prefix_matches[
                before_prefix_locations.index(before_prefix_location)
            ]
            after_prefix_location = self._plan_cursor_location(
                prefix_match,
                cursor_position="after",
                include_whitespace=False,
                click_offset_right=click_offset_right,
                selection_position=self.SelectionPosition.RIGHT,
            )
            self.keyboard.shift_down()
            try:
                after_prefix_location.move_text_cursor()
            finally:
                self.keyboard.shift_up()
            return (0, prefix_length)
        else:
            assert after_suffix_location and not before_prefix_location
            suffix_match = suffix_matches[
                after_suffix_locations.index(after_suffix_location)
            ]
            before_suffix_location = self._plan_cursor_location(
                suffix_match,
                cursor_position="before",
                include_whitespace=False,
                click_offset_right=click_offset_right,
                selection_position=self.SelectionPosition.LEFT,
            )
            before_suffix_location.move_text_cursor()
            time.sleep(select_pause_seconds)
            self.keyboard.shift_down()
            try:
                after_suffix_location.move_text_cursor()
            finally:
                self.keyboard.shift_up()
            return (len(words) - suffix_length, len(words))

    def find_nearest_cursor_location(
        self, locations: Sequence[CursorLocation]
    ) -> Optional[CursorLocation]:
        """Returns the cursor location nearest to the current gaze point, if
        available."""
        if not locations:
            return None
        contents = self.latest_screen_contents()
        if not contents.screen_coordinates:
            # "Nearest" is undefined.
            return None
        distance_to_words = [
            (
                _distance_squared(
                    location.click_coordinates, contents.screen_coordinates
                ),
                location,
            )
            for location in locations
        ]
        return min(distance_to_words, key=lambda x: x[0])[1]

    def move_cursor_to_word_action(self):
        raise RuntimeError(
            "controller.move_cursor_to_word_action no longer supported. "
            "Use gaze_ocr.dragonfly.MoveCursorToWordAction instead."
        )

    def move_text_cursor_action(self, word, cursor_position="middle"):
        """Return a dragonfly action for moving the text cursor nearby a word."""
        raise RuntimeError(
            "controller.move_text_cursor_action no longer supported. "
            "Use gaze_ocr.dragonfly.MoveTextCursorAction instead."
        )

    def select_text_action(self, start_word, end_word=None, for_deletion=False):
        """Return a Dragonfly action for selecting text."""
        raise RuntimeError(
            "controller.select_text_action no longer supported. "
            "Use gaze_ocr.dragonfly.SelectTextAction instead."
        )

    def _read_nearby_if_gaze_moved(self):
        current_gaze = (
            self.eye_tracker.get_gaze_point()
            if self.eye_tracker and self.eye_tracker.is_connected
            else None
        )
        latest_screen_contents = self.latest_screen_contents()
        previous_gaze = latest_screen_contents.screen_coordinates
        threshold_squared = (
            _squared(latest_screen_contents.search_radius / 2.0)
            if latest_screen_contents.search_radius
            else 0.0
        )
        if (
            current_gaze
            and previous_gaze
            and _distance_squared(current_gaze, previous_gaze) > threshold_squared
        ):
            self.read_nearby()

    def _plan_cursor_locations(
        self,
        matches: Sequence[Sequence[WordLocation]],
        cursor_position: str,
        include_whitespace: bool,
        click_offset_right: int,
        selection_position: SelectionPosition,
    ) -> Sequence[CursorLocation]:
        return [
            self._plan_cursor_location(
                match,
                cursor_position=cursor_position,
                include_whitespace=include_whitespace,
                click_offset_right=click_offset_right,
                selection_position=selection_position,
            )
            for match in matches
        ]

    def _plan_cursor_location(
        self,
        locations: Sequence[WordLocation],
        cursor_position: str,
        include_whitespace: bool,
        click_offset_right: int,
        selection_position: SelectionPosition,
    ) -> CursorLocation:
        if cursor_position == "before":
            distance_from_left = locations[0].left_char_offset
            distance_from_right = locations[0].right_char_offset + len(
                locations[0].text
            )
            move_past_whitespace_left = include_whitespace and not distance_from_left
            move_past_whitespace_right = False
            return self._plan_cursor_movement(
                start_coordinates=locations[0].start_coordinates,
                end_coordinates=locations[0].end_coordinates,
                click_offset_right=click_offset_right,
                distance_from_left=distance_from_left,
                distance_from_right=distance_from_right,
                selection_position=selection_position,
                move_past_whitespace_left=move_past_whitespace_left,
                move_past_whitespace_right=move_past_whitespace_right,
                text_height=locations[0].height,
            )
        elif cursor_position == "middle":
            # Note: if it's helpful, we could change this to position the cursor
            # in the middle of the word.
            coordinates = self._apply_click_offset(
                (
                    int((locations[0].left + locations[-1].right) / 2),
                    int((locations[0].top + locations[-1].bottom) / 2),
                ),
                click_offset_right,
            )
            return CursorLocation(
                click_coordinates=coordinates,
                visual_coordinates=coordinates,
                move_cursor_right=False,
                move_distance=0,
                move_past_whitespace_left=False,
                move_past_whitespace_right=False,
                text_height=locations[0].height,
                mouse=self.mouse,
                keyboard=self.keyboard,
                app_actions=self.app_actions,
            )
        else:
            assert cursor_position == "after"
            distance_from_right = locations[-1].right_char_offset
            distance_from_left = locations[-1].left_char_offset + len(
                locations[-1].text
            )
            move_past_whitespace_left = False
            move_past_whitespace_right = include_whitespace and not distance_from_right
            return self._plan_cursor_movement(
                start_coordinates=locations[-1].start_coordinates,
                end_coordinates=locations[-1].end_coordinates,
                click_offset_right=click_offset_right,
                distance_from_left=distance_from_left,
                distance_from_right=distance_from_right,
                selection_position=selection_position,
                move_past_whitespace_left=move_past_whitespace_left,
                move_past_whitespace_right=move_past_whitespace_right,
                text_height=locations[0].height,
            )

    def _plan_cursor_movement(
        self,
        start_coordinates: tuple[int, int],
        end_coordinates: tuple[int, int],
        click_offset_right: int,
        distance_from_left: int,
        distance_from_right: int,
        selection_position: SelectionPosition,
        move_past_whitespace_left: bool,
        move_past_whitespace_right: bool,
        text_height: int,
    ) -> CursorLocation:
        estimated_char_width = (end_coordinates[0] - start_coordinates[0]) / float(
            distance_from_left + distance_from_right
        )
        visual_coordinates = (
            int(start_coordinates[0] + distance_from_left * estimated_char_width),
            int((start_coordinates[1] + end_coordinates[1]) / 2.0),
        )
        # Determine whether to start from the left or the right.
        if not distance_from_left:
            start_from_left = True
        elif not distance_from_right:
            start_from_left = False
        elif selection_position == self.SelectionPosition.RIGHT:
            # Mac selection can only be reliably expanded outward.
            start_from_left = True
        elif selection_position == self.SelectionPosition.LEFT:
            # Mac selection can only be reliably expanded outward.
            start_from_left = False
        elif distance_from_left <= distance_from_right:
            start_from_left = True
        else:
            start_from_left = False
        if start_from_left:
            coordinates = self._apply_click_offset(
                start_coordinates, click_offset_right
            )
            return CursorLocation(
                click_coordinates=coordinates,
                visual_coordinates=visual_coordinates,
                move_cursor_right=True,
                move_distance=distance_from_left,
                move_past_whitespace_left=move_past_whitespace_left,
                move_past_whitespace_right=move_past_whitespace_right,
                text_height=text_height,
                mouse=self.mouse,
                keyboard=self.keyboard,
                app_actions=self.app_actions,
            )
        else:
            # Start from the right.
            coordinates = self._apply_click_offset(end_coordinates, click_offset_right)
            return CursorLocation(
                click_coordinates=coordinates,
                visual_coordinates=visual_coordinates,
                move_cursor_right=False,
                move_distance=distance_from_right,
                move_past_whitespace_left=move_past_whitespace_left,
                move_past_whitespace_right=move_past_whitespace_right,
                text_height=text_height,
                mouse=self.mouse,
                keyboard=self.keyboard,
                app_actions=self.app_actions,
            )

    def _choose_cursor_location(
        self,
        disambiguate: bool,
        matches: Sequence[CursorLocation],
    ) -> Generator[Sequence[CursorLocation], CursorLocation, Optional[CursorLocation]]:
        if not matches:
            return None
        if len(matches) == 1:
            return matches[0]
        if disambiguate:
            return (yield matches)
        else:
            return self.find_nearest_cursor_location(matches)

    @staticmethod
    def _extract_result(generator):
        """Extracts final return value from generator, assuming no values are generated."""
        try:
            next(generator)
            raise AssertionError()
        except StopIteration as e:
            return e.value

    @staticmethod
    def _apply_click_offset(coordinates, offset_right):
        return (coordinates[0] + offset_right, coordinates[1])

    def _write_data(self, screen_contents, word, word_locations):
        if not self.save_data_directory:
            return
        if word_locations:
            result = "multiple" if len(word_locations) > 1 else "success"
        else:
            result = "failure"
        file_name_prefix = f"{result}_{time.time():.2f}"
        file_path_prefix = os.path.join(self.save_data_directory, file_name_prefix)
        if hasattr(screen_contents.screenshot, "save"):
            screen_contents.screenshot.save(file_path_prefix + ".png")
        else:
            screen_contents.screenshot.write_file(file_path_prefix + ".png")
        with open(file_path_prefix + ".txt", "w") as file:
            file.write(word)

    def _is_valid_selection(self, start_coordinates, end_coordinates):
        epsilon = 5  # pixels
        (start_x, start_y) = start_coordinates
        (end_x, end_y) = end_coordinates
        # Selection goes to previous line.
        if end_y - start_y < -epsilon:
            return False
        # Selection stays on same line.
        elif end_y - start_y < epsilon:
            return end_x > start_x
        # Selection moves to following line.
        else:
            return True


def _squared(x):
    return x * x


def _distance_squared(coordinate1, coordinate2):
    x_diff = coordinate1[0] - coordinate2[0]
    y_diff = coordinate1[1] - coordinate2[1]
    return _squared(x_diff) + _squared(y_diff)
