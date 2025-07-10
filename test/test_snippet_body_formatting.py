import talon

if hasattr(talon, "test_mode"):
	# Only include this when we're running tests
	from core.snippets import snippets_parser

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