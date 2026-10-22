import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests
    from core.snippets.snippets_insert_raw_text import Stop, parse_snippet

    def escapes_backslashes_and_dollar_signs_properly():
        body = "\\\\\\$9$1\\\\\\\\$0\\\\"
        expected_body = "\\$9\\\\\\"
        expected_stops = [Stop("1", 0, 3, 0, 3), Stop("0", 0, 1, 0, 5)]
        assert (expected_body, expected_stops) == parse_snippet(body)
