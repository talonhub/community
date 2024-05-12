import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from talon import actions

    from core.text import formatters

    def setup_function():
        actions.reset_test_actions()
        actions.register_test_action("user", "add_phrase_to_history", lambda x: None)

    def test_snake_case():
        result = formatters.Actions.formatted_text("hello world", "SNAKE_CASE")

        assert result == "hello_world"

    def test_no_spaces():
        result = formatters.Actions.formatted_text("hello world", "NO_SPACES")

        assert result == "helloworld"

    def test_capitalize():
        result = formatters.Actions.formatted_text("hello world", "CAPITALIZE")

        assert result == "Hello world"

        result = formatters.Actions.formatted_text("hEllo wOrld", "CAPITALIZE")

        assert result == "HEllo wOrld"

    def test_capitalize_first_word():
        result = formatters.Actions.formatted_text(
            "hello world", "CAPITALIZE_FIRST_WORD"
        )

        assert result == "Hello world"

        result = formatters.Actions.formatted_text(
            "hEllo wOrld", "CAPITALIZE_FIRST_WORD"
        )

        assert result == "hEllo wOrld"

    def test_capitalize_all_words():
        result = formatters.Actions.formatted_text(
            "hello world", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "Hello World"

        result = formatters.Actions.formatted_text(
            "hEllo wOrld", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "hEllo wOrld"

        result = formatters.Actions.formatted_text(
            "Hello to the world", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "Hello to the World"

        result = formatters.Actions.formatted_text(
            "hello: the world", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "Hello: The World"

        result = formatters.Actions.formatted_text(
            "down and up", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "Down and Up"

        result = formatters.Actions.formatted_text(
            "down-and-up", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "Down-and-Up"

        result = formatters.Actions.formatted_text(
            "it's good they’re Bill’s friends", "CAPITALIZE_ALL_WORDS"
        )

        assert result == "It's Good They’re Bill’s Friends"

        result = formatters.Actions.formatted_text(
            '"how\'s it going?"', "CAPITALIZE_ALL_WORDS"
        )

        assert result == '"How\'s It Going?"'
