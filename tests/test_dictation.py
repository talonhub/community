import talon

PHRASE_EXAMPLES = ["", "foo", "foo bar", "lorem ipsum dolor sit amet"]

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from knausj_talon_pkg.code import dictation

    def test_format_phrase():
        for x in PHRASE_EXAMPLES:
            assert dictation.format_phrase([x]) == x
            assert dictation.format_phrase(x.split()) == x

    def test_capture_to_words():
        # if l is a list of strings, then (capture_to_words(l) == l) should hold.
        for s in PHRASE_EXAMPLES:
            for l in [[s], s.split(), list(s)]:
                assert dictation.capture_to_words(l) == l

    def test_spacing_and_capitalization():
        format = dictation.DictationFormat()
        format.state = None
        result = format.format("first")
        assert result == "first"
        result = format.format("second.")
        assert result == " second."
        result = format.format("third(")
        assert result == " Third("
        result = format.format("fourth")
        assert result == "fourth"

    def test_force_spacing_and_capitalization():
        format = dictation.DictationFormat()
        format.state = None
        format.force_capitalization = "cap"
        result = format.format("first")
        assert result == "First"
        format.force_no_space = True
        result = format.format("second.")
        assert result == "second."
        format.force_capitalization = "no cap"
        result = format.format("third(")
        assert result == " third("
        result = format.format("fourth")
        assert result == "fourth"
