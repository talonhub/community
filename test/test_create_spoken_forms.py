import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    import itertools
    from collections.abc import Callable

    from talon import actions

    import core.abbreviate
    import core.user_settings

    # we need to replace the register_settings_csv decorator for unit tests.
    CallbackT = Callable[[dict[str, str]], None]
    DecoratorT = Callable[[CallbackT], CallbackT]

    def register_settings_csv_test(
        filename: str,
        headers: tuple[str, str],
        default: dict[str, str] = None,
        is_spoken_form_first: bool = False,
    ) -> DecoratorT:
        def decorator(fn: CallbackT) -> CallbackT:
            extensions = {
                "dot see sharp": ".cs",
            }
            abbreviations = {"source": "src", "whats app": "WhatsApp"}
            if filename == "abbreviations.csv":
                fn(abbreviations)
            elif filename == "file_extensions.csv":
                fn(extensions)

        return decorator

    # replace register_settings_csv before importing create_spoken_forms, so it registers our mock
    core.user_settings.register_customization_csv = register_settings_csv_test
    import core.create_spoken_forms
    from core.create_spoken_forms import create_spoken_form_years
    from core.vocabulary.vocabulary import PhraseReplacer

    def test_excludes_words():
        result = actions.user.create_spoken_forms("hi world", ["world"], 0, True)

        assert "world" not in result
        assert "hi world" in result

    def test_handles_empty_input():
        result = actions.user.create_spoken_forms("", None, 0, True)

        assert result == []

    def test_handles_minimum_term_length():
        result = actions.user.create_spoken_forms("hi world", None, 3, True)

        assert "hi" not in result
        assert "world" in result

    def test_handles_generate_subsequences():
        result = actions.user.create_spoken_forms("hi world", None, 0, False)

        assert "world" not in result
        assert "hi world" in result

    def test_expands_special_chars():
        result = actions.user.create_spoken_forms("hi $world", None, 0, True)

        assert "hi world" in result

    def test_expands_file_extensions():
        result = actions.user.create_spoken_forms("hi .cs", None, 0, True)

        assert "hi dot see sharp" in result

    def test_expands_abbreviations():

        result = actions.user.create_spoken_forms("src", None, 0, True)

        assert "source" in result
        assert "src" in result

        result = actions.user.create_spoken_forms("WhatsApp", None, 0, True)

        assert "whats app" in result

    def test_expand_upper_case():
        result = actions.user.create_spoken_forms("LICENSE", None, 0, True)

        assert "license" in result
        assert "L I C E N S E" in result

    def test_small_word_to_upper_case():
        result = actions.user.create_spoken_forms("vm", None, 0, True)

        assert "V M" in result

    def test_explode_packed_words():
        result = actions.user.create_spoken_forms("README", None, 0, True)

        assert "read me" in result

    def test_email():
        result = actions.user.create_spoken_forms("stupid@test.com", None, 0, True)
        assert "stupid at test dot com" in result

    def test_symbol_removal():
        result = actions.user.create_spoken_forms("$ this_is_a-'test'", None, 0, True)

        assert "this is a test" in result

    def test_and_symbol():
        result = actions.user.create_spoken_forms("movies & tv", None, 0, True)

        assert "movies tv" in result
        assert "movies and tv" in result

    def test_apostrophe_stripping():
        result = actions.user.create_spoken_forms("Sam's club", None, 0, True)

        assert "sams club" in result

    def test_properties():
        """
        Throw some random inputs at the function to make sure it behaves itself
        """

        def _example_generator():
            pieces = ["hi", "world", "dollar", ".cs", "1900"]
            params = list(
                itertools.product(
                    [None, ["world"], ["dot"]],  # Dot is from the expanded ".cs"
                    [0, 3],
                    [True, False],
                )
            )
            count = 0
            while True:
                for exclude, min_count, subseq in params:
                    for tokens in itertools.combinations(pieces, r=count):
                        yield (tokens, exclude, min_count, subseq)
                count += 1

        examples = itertools.islice(_example_generator(), 0, 100)
        for tokens, exclude, min_count, subseq in examples:
            source = " ".join(tokens)
            result = actions.user.create_spoken_forms(
                source, exclude, min_count, subseq
            )

            statement = (
                f'create_spoken_forms("{source}", {exclude}, {min_count}, {subseq})'
            )

            # No duplicates in result
            assert len(result) == len(set(result)), statement

            # No empty strings in result
            assert "" not in result, statement

            # Generates a form if we give it a non-empty input
            if len(tokens) > 0:
                assert len(result) >= 1, statement

            # Generated forms at least as numerous as input if subseq is True
            if subseq:
                assert len(result) >= len(tokens), statement

    def test_create_spoken_form_years():
        # ---------- create_spoken_form_years  (uncomment to run) ----------
        def test_year(year: str, expected: str):
            result = create_spoken_form_years(year)
            print(
                f"test_year: test string = {year}, result = {result}, expected = {expected}"
            )
            assert create_spoken_form_years(year) == expected

        print("************* test_year tests ******************")
        test_year("1100", "eleven hundred")
        test_year("1905", "nineteen five")
        test_year("1910", "nineteen ten")
        test_year("1925", "nineteen twenty five")
        test_year("2000", "two thousand")
        test_year("2005", "two thousand five")
        test_year("2020", "twenty twenty")
        test_year("2019", "twenty nineteen")
        test_year("2085", "twenty eighty five")
        test_year("2100", "twenty one hundred")
        test_year("2105", "twenty one five")
        test_year("9999", "ninety nine ninety nine")
        print("************* test_year tests done**************")

    def test_PhraseReplacer():
        rep = PhraseReplacer()
        rep.update(
            {
                "this": "foo",
                "that": "bar",
                "this is": "stopping early",
                "this is a test": "it worked!",
            }
        )
        assert rep.replace_string("gnork") == "gnork"
        assert rep.replace_string("this") == "foo"
        assert rep.replace_string("this that this") == "foo bar foo"
        assert rep.replace_string("this is a test") == "it worked!"
        assert (
            rep.replace_string("well this is a test really") == "well it worked! really"
        )
        assert rep.replace_string("try this is too") == "try stopping early too"
        assert (
            rep.replace_string("this is a tricky one") == "stopping early a tricky one"
        )
