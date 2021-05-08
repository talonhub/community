import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from tests.utils import TalonTestCase
    from code import formatters

    class TestFormatters(TalonTestCase):
        """
        Tests the text formatters
        """

        def test_snake_case(self):
            result = formatters.Actions.formatted_text("hello world", "SNAKE_CASE")

            self.assertEqual(result, "hello_world")

        def setUp(self):
            from talon import actions

            actions.reset_actions()
            actions.register_test_action("user.add_phrase_to_history", lambda x: None)
