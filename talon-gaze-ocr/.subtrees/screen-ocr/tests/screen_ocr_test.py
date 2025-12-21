import screen_ocr
from screen_ocr import _base


def test_find_longest_matching_suffix():
    line = _base.OcrLine(
        words=[
            _base.OcrWord(text="a", left=0, top=0, width=10, height=10),
            _base.OcrWord(text="test.", left=0, top=0, width=10, height=10),
            _base.OcrWord(text="b", left=0, top=0, width=10, height=10),
        ]
    )
    ocr_result = _base.OcrResult(lines=[line])
    contents = screen_ocr.ScreenContents(
        screen_coordinates=None,
        bounding_box=(0, 0, 100, 100),
        screenshot=None,
        result=ocr_result,
        confidence_threshold=1,
        homophones={},
        search_radius=None,
    )
    locations, suffix_length = contents.find_longest_matching_suffix("test word.")
    assert locations == [
        [
            screen_ocr.WordLocation(
                text=".",
                left_char_offset=4,
                right_char_offset=0,
                left=0,
                top=0,
                width=10,
                height=10,
                ocr_word_index=1,
                ocr_line_index=0,
            )
        ]
    ]
    assert suffix_length == 1
    locations, suffix_length = contents.find_longest_matching_suffix(" word.")
    assert locations == [
        [
            screen_ocr.WordLocation(
                text=".",
                left_char_offset=4,
                right_char_offset=0,
                left=0,
                top=0,
                width=10,
                height=10,
                ocr_word_index=1,
                ocr_line_index=0,
            )
        ]
    ]
    assert suffix_length == 1


def test_generate_candidates_from_line():
    line = _base.OcrLine(
        words=[
            _base.OcrWord(text="snake_case:=", left=0, top=0, width=10, height=10),
            _base.OcrWord(text="[TestClass]", left=12, top=0, width=10, height=10),
            _base.OcrWord(text="camelCase", left=24, top=0, width=10, height=10),
            _base.OcrWord(text="ALLCAPS", left=36, top=0, width=10, height=10),
            _base.OcrWord(text="doesn't", left=48, top=0, width=10, height=10),
        ]
    )
    candidates = list(screen_ocr.ScreenContents._generate_candidates_from_line(line, 0))
    assert candidates == [
        screen_ocr.WordLocation(
            text="snake",
            left_char_offset=0,
            right_char_offset=7,
            left=0,
            top=0,
            width=10,
            height=10,
            ocr_word_index=0,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="_",
            left_char_offset=5,
            right_char_offset=6,
            left=0,
            top=0,
            width=10,
            height=10,
            ocr_word_index=0,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="case",
            left_char_offset=6,
            right_char_offset=2,
            left=0,
            top=0,
            width=10,
            height=10,
            ocr_word_index=0,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text=":",
            left_char_offset=10,
            right_char_offset=1,
            left=0,
            top=0,
            width=10,
            height=10,
            ocr_word_index=0,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="=",
            left_char_offset=11,
            right_char_offset=0,
            left=0,
            top=0,
            width=10,
            height=10,
            ocr_word_index=0,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="[",
            left_char_offset=0,
            right_char_offset=10,
            left=12,
            top=0,
            width=10,
            height=10,
            ocr_word_index=1,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="Test",
            left_char_offset=1,
            right_char_offset=6,
            left=12,
            top=0,
            width=10,
            height=10,
            ocr_word_index=1,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="Class",
            left_char_offset=5,
            right_char_offset=1,
            left=12,
            top=0,
            width=10,
            height=10,
            ocr_word_index=1,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="]",
            left_char_offset=10,
            right_char_offset=0,
            left=12,
            top=0,
            width=10,
            height=10,
            ocr_word_index=1,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="camel",
            left_char_offset=0,
            right_char_offset=4,
            left=24,
            top=0,
            width=10,
            height=10,
            ocr_word_index=2,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="Case",
            left_char_offset=5,
            right_char_offset=0,
            left=24,
            top=0,
            width=10,
            height=10,
            ocr_word_index=2,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="ALLCAPS",
            left_char_offset=0,
            right_char_offset=0,
            left=36,
            top=0,
            width=10,
            height=10,
            ocr_word_index=3,
            ocr_line_index=0,
        ),
        screen_ocr.WordLocation(
            text="doesn't",
            left_char_offset=0,
            right_char_offset=0,
            left=48,
            top=0,
            width=10,
            height=10,
            ocr_word_index=4,
            ocr_line_index=0,
        ),
    ]
