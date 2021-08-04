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

    def test_strikethrough_text():
        result = formatters.Actions.formatted_text("hello world", "STRIKETHROUGH")
        assert result == "h̶e̶l̶l̶o̶ ̶w̶o̶r̶l̶d̶"

    # TODO activate test and fix assert once case preservation is built into strikethrough
    # def test_strikethrough_text_preserves_case():
    #     result = formatters.Actions.formatted_text("HELLO world", "STRIKETHROUGH")
    #     assert result == "h̶e̶l̶l̶o̶ ̶w̶o̶r̶l̶d̶"

    # Reformat selection should call unformat_text to clear the strikethrough before it applies NOOP
    def test_removing_strikethrough_from_text_with_unformatter():
        # Can't call the actual formatter action which unformats and then formats since that's coupled to the editor
        # So for now just test unformat
        result = formatters.unformat_text("h̶e̶l̶l̶o̶ ̶w̶o̶r̶l̶d̶")
        assert result == "hello world"