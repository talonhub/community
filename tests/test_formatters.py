import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from talon import actions
    from knausj_talon_pkg.code import formatters

    def setup_function():
        actions.reset_actions()
        actions.register_test_action("user.add_phrase_to_history", lambda x: None)

    def test_snake_case():
        result = formatters.Actions.formatted_text("hello world", "SNAKE_CASE")

        assert result == "hello_world"

    def test_no_spaces():
        result = formatters.Actions.formatted_text("hello world", "NO_SPACES")

        assert result == "helloworld"
