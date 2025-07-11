import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests
    from core.snippets import snippets_parser
    from core.snippets.snippet_types import SnippetVariable

    def assert_body_with_final_stop_added_as_expected(body: str, expected: str):
        actual, _ = snippets_parser.add_final_stop_to_snippet_body(body, [])
        assert actual == expected

    def test_stop_at_end():
        body = "import $0"
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_final_stop_not_at_end():
        body = "[$1]($0)"
        expected = "[$1]($2)$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_without_final_stop():
        body = "[$1]($2)"
        expected = "[$1]($2)$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_empty_body_unchanged():
        body = ""
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_number_inside_braces():
        body = "if (${1}){\n\t${0}}"
        expected = "if (${1}){\n\t${2}}$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_final_stop_with_default_value():
        body = "import ${0:default_value}"
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_final_stop_with_value_inside_braces():
        body = "import ${0}"
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_biggest_value_having_default():
        body = "from ${1:module} import $0;"
        expected = "from ${1:module} import $2;$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_three_stops():
        body = "[$0 for $2 in $1]"
        expected = "[$3 for $2 in $1]$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_multiple_final_stops():
        body = "[$0 for $0 in $1 if $2]"
        expected = "[$3 for $3 in $1 if $2]$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_multiple_final_stops_with_default():
        body = "[${0:nums} for ${0:nums} in $1 if $2]"
        expected = "[${3:nums} for ${3:nums} in $1 if $2]$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_multiple_final_stops_with_number_in_braces():
        body = "[${0} for ${0} in $1 if $2]"
        expected = "[${3} for ${3} in $1 if $2]$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def test_duplicate_proceeding_stops():
        body = "[$1 for $1 in $0]"
        expected = "[$1 for $1 in $2]$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def assert_variables_match_expected(
        body: str,
        variables: list[SnippetVariable],
        expected_variables: list[SnippetVariable],
    ):
        _, actual = snippets_parser.add_final_stop_to_snippet_body(body, variables)
        assert actual == expected_variables

    def test_formatting_gets_moved():
        body = "def $0:\n\treturn $1"
        variables = [SnippetVariable("0", insertion_formatters=["snake"])]
        expected_variables = [SnippetVariable("1", insertion_formatters=["snake"])]
        assert_variables_match_expected(body, variables, expected_variables)

    def test_variables_unchanged_for_smaller_variable():
        body = "def $1:\n\treturn $0;"
        variables = [SnippetVariable("1", insertion_formatters=["snake"])]
        expected_variables = [SnippetVariable("1", insertion_formatters=["snake"])]
        assert_variables_match_expected(body, variables, expected_variables)

    def test_variables_unchanged_with_stop_at_end():
        body = "def $1:\n\treturn $0"
        variables = [SnippetVariable("1", insertion_formatters=["snake"])]
        expected_variables = [SnippetVariable("1", insertion_formatters=["snake"])]
        assert_variables_match_expected(body, variables, expected_variables)
