import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests
    from core.snippets import snippets_parser

    DEFAULT_CONTEXT = snippets_parser.SnippetDocument("", -1, -1)

    def assert_body_with_final_stop_added_as_expected(body: str, expected: str):
        actual = snippets_parser.add_final_stop_to_snippet_body(body)
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

    def test_nonzero_final_stop():
        body = "test $1"
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_nonzero_final_stop_with_default():
        body = "test ${1:default}"
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_nonzero_final_stop_with_number_in_braces():
        body = "test ${2}"
        assert_body_with_final_stop_added_as_expected(body, body)

    def test_nonzero_at_end_with_zero_earlier():
        body = "test$0 $1"
        expected = "test$2 $1$0"
        assert_body_with_final_stop_added_as_expected(body, expected)

    def assert_snippet_body_matches_expected(body: str, expected: str):
        document = snippets_parser.SnippetDocument(
            "test.snippet", 1, 2 + body.count("\n")
        )
        document.body = body
        document.name = "test"
        snippet = snippets_parser.create_snippet(document, DEFAULT_CONTEXT)
        assert snippet.body == expected

    def test_escaping_space_at_start():
        body = "\\ "
        expected = " "
        assert_snippet_body_matches_expected(body, expected)

    def test_escaping_space_at_start_with_three_backslashes():
        body = "\\\\\\ "
        expected = "\\ "
        assert_snippet_body_matches_expected(body, expected)

    def test_escaping_four_backslashes():
        body = "\\\\ "
        expected = "\\ "
        assert_snippet_body_matches_expected(body, expected)

    def test_escaping_multiple_spaces():
        body = "\\ \\ a\\ b"
        expected = "  a b"
        assert_snippet_body_matches_expected(body, expected)

    def test_escaping_backslashes_in_the_middle():
        body = "	a\\\\ \\\\\\\\b \\\\ c"
        expected = "	a\\ \\\\b \\ c"
        assert_snippet_body_matches_expected(body, expected)

    def assert_snippet_literal_body_matches_expected(body: str, expected: str):
        text = f"name: snippetName\nphrase: phrase\n-\n{body}\n---"
        documents = snippets_parser.parse_file_content("file", text)
        snippet = snippets_parser.create_snippets(documents)[0]
        assert snippet.body == expected

    def test_escaping_space_at_the_end():
        text = "snippetBody\\ "
        expected = "snippetBody "
        assert_snippet_literal_body_matches_expected(text, expected)

    def test_escaping_three_backslashes_and_a_space_at_the_end():
        text = "snippetBody\\\\\\ "
        expected = "snippetBody\\ "
        assert_snippet_literal_body_matches_expected(text, expected)

    def test_escaping_two_backslashes_at_the_end():
        text = "snippetBody\\\\ "
        expected = "snippetBody\\"
        assert_snippet_literal_body_matches_expected(text, expected)

    def test_escaping_space_before_more_whitespace():
        text = "snippetBody\\   "
        expected = "snippetBody "
        assert_snippet_literal_body_matches_expected(text, expected)