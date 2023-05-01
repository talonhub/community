import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    import itertools

    from talon import actions

    import core.create_spoken_forms

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

        assert "hi dollar sign world" in result

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

    def test_properties():
        """
        Throw some random inputs at the function to make sure it behaves itself
        """

        def _example_generator():
            pieces = ["hi", "world", "$", ".cs", "1900"]
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
