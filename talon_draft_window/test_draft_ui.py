try:
    import talon.experimental.textarea
    running_in_talon = True
except ModuleNotFoundError:
    # Some shenanigans to stub out the Talon imports
    import imp, sys
    name = "talon.experimental.textarea"
    module = imp.new_module(name)
    sys.modules[name] = module
    exec(
        "\n".join([
            "TextArea = 1",
            "Span = 1",
            "DarkThemeLabels = 1",
            "LightThemeLabels = 1"
        ]),
        module.__dict__
    )
    running_in_talon = False

from unittest import TestCase
from functools import wraps

from .draft_ui import calculate_text_anchors


class CalculateAnchorsTest(TestCase):
    """
    Tests calculate_text_anchors
    """

    def test_finds_anchors(self):
        examples = [
            ("one-word", [("a", 0, 8, 8)]),
            ("two words", [("a", 0, 3, 4), ("b", 4, 9, 9)]),
            ("two\nwords", [("a", 0, 3, 4), ("b", 4, 9, 9)]),
        ]
        anchor_labels = ["a", "b"]
        for text, expected in examples:
            # Given an example

            # When we calculate the result and turn it into a list
            result = list(calculate_text_anchors(text, 0, anchor_labels=anchor_labels))

            # Then it matches what we expect
            self.assertEqual(result, expected, text)

    def test_positions_anchors_around_cursor(self):
        # In these examples the cursor is at the asterisk which is stripped by the test
        # code. Indicies after the asterisk have to take this into account.
        examples = [
            ("one*-word", [("a", 0, 8, 8)]),
            ("one-word*", [("a", 0, 8, 8)]),
            (
                "the three words*",
                [("a", 0, 3, 4), ("b", 4, 9, 10), ("c", 10, 15, 15)]
            ),
            (
                "*the three words",
                [("a", 0, 3, 4), ("b", 4, 9, 10), ("c", 10, 15, 15)]
            ),
            (
                "too many* words for the number of anchors",
                [("a", 0, 3, 4), ("b", 4, 8, 9), ("c", 9, 14, 15)]
            ),
            (
                "too many words fo*r the number of anchors",
                [("a", 9, 14, 15), ("b", 15, 18, 19), ("c", 19, 22, 23)]
            ),
        ]
        anchor_labels = ["a", "b", "c"]

        for text_with_cursor, expected in examples:
            # Given an example
            cursor_pos = text_with_cursor.index("*")
            text = text_with_cursor.replace("*", "")

            # When we calculate the result and turn it into a list
            result = list(calculate_text_anchors(
                text,
                cursor_pos,
                anchor_labels=anchor_labels
            ))

            # Then it matches what we expect
            self.assertEqual(result, expected, text)
