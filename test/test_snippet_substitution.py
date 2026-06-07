import talon

if hasattr(talon, "test_mode"):  # Only include this when we're running tests
    import pytest

    from core.snippets.snippets_insert import compute_snippet_text_with_substitutions

    FUNCTION_DECLARATION_BODY = "def $1($2):\n\t$0"

    def assert_substituting_matches_expected(
        body: str, substitutions: dict[str, str], expected: str
    ):
        actual = compute_snippet_text_with_substitutions(body, substitutions)
        assert actual == expected

    def assert_substituting_raises_exception(body: str, substitutions: dict[str, str], name: str | None=None, expected_text: str | None=None):
        with pytest.raises(ValueError) as error_info:
            compute_snippet_text_with_substitutions(body, substitutions, name)
        if expected_text is not None:
            assert expected_text in str(error_info.value)

    def test_substitution_only():
        body = "$0"
        substitution = {"0": "test"}
        expected = "test"
        assert_substituting_matches_expected(body, substitution, expected)

    def test_substituting_first():
        substitution = {"1": "test"}
        expected = "def test($2):\n\t$0"
        assert_substituting_matches_expected(
            FUNCTION_DECLARATION_BODY, substitution, expected
        )

    def test_substituting_second():
        substitution = {"2": "test"}
        expected = "def $1(test):\n\t$0"
        assert_substituting_matches_expected(
            FUNCTION_DECLARATION_BODY, substitution, expected
        )

    def test_substituting_third():
        substitution = {"0": "test"}
        expected = "def $1($2):\n\ttest"
        assert_substituting_matches_expected(
            FUNCTION_DECLARATION_BODY, substitution, expected
        )

    def test_substituting_all():
        substitution = {"0": "third", "1": "first", "2": "second"}
        expected = "def first(second):\n\tthird"
        assert_substituting_matches_expected(
            FUNCTION_DECLARATION_BODY, substitution, expected
        )

    def test_error_message_contains_body():
        substitution = {"9": "test"}
        assert_substituting_raises_exception(
            FUNCTION_DECLARATION_BODY,
            substitution,
            expected_text=FUNCTION_DECLARATION_BODY
        )

    def test_error_message_contains_name():
        substitution = {"9": "test"}
        name="function declaration"
        assert_substituting_raises_exception(
            FUNCTION_DECLARATION_BODY,
            substitution,
            name=name,
            expected_text=name
        )