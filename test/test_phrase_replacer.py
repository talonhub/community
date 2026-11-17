import talon

if hasattr(talon, "test_mode"):
    from core.vocabulary.vocabulary import PhraseReplacer

    replacer = PhraseReplacer()
    replacer.update(
        {
            "this": "foo",
            "that": "bar",
            "this is": "stopping early",
            "this is a test": "it worked!",
        }
    )

    def _assert_replacement_matches_expected(text, expected_replacement):
        assert replacer.replace_string(text) == expected_replacement

    def test_irrelevant_word_is_not_replaced():
        _assert_replacement_matches_expected("gnork", "gnork")

    def test_replacing_single_word_input():
        _assert_replacement_matches_expected("this", "foo")

    def test_replacing_multiple_words():
        _assert_replacement_matches_expected("this that this", "foo bar foo")

    def test_replacing_biggest_relevant_word_sequence():
        _assert_replacement_matches_expected("this is a test", "it worked!")

    def test_replacing_biggest_relevant_word_sequence_in_bigger_string():
        _assert_replacement_matches_expected(
            "well this is a test really", "well it worked! really"
        )

    def test_replacing_word_sequence():
        _assert_replacement_matches_expected(
            "try this is too", "try stopping early too"
        )

    def test_replacing_word_sequence_one_short_of_a_bigger_relevant_sequence():
        _assert_replacement_matches_expected(
            "this is a tricky one", "stopping early a tricky one"
        )
