import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    import random
    import shlex
    from knausj_talon_pkg.core.system_command import split_command

    def test_handles_empty():
        assert split_command("") == ("ok", [])

    def test_handles_simple():
        cmd = "~/my-script.sh args"
        expected = (
            "ok",
            [
                ("~/my-script.sh", "simple"),
                ("args", "simple"),
            ]
        )
        assert split_command(cmd) == expected

    def test_handles_quotes_in_simple():
        cmd = "thi'n'g"
        expected = (
            "ok",
            [
                ("thing", "quoted"),
            ]
        )
        assert split_command(cmd) == expected

    def test_handles_single_quotes():
        cmd = "~/my-script.sh 'with single\"quotes'"
        expected = (
            "ok",
            [
                ("~/my-script.sh", "simple"),
                ("with single\"quotes", "quoted"),
            ]
        )
        assert split_command(cmd) == expected

    def test_handles_double_quotes():
        cmd = "~/my-script.sh \"with double'quotes\""
        expected = (
            "ok",
            [
                ("~/my-script.sh", "simple"),
                ("with double'quotes", "quoted"),
            ]
        )
        assert split_command(cmd) == expected

    def test_handles_escaped_quotes():
        cmd = "\"dou\\ble\\\"\" 'sin\\gle\\'"
        expected = (
            "ok",
            [
                # Double quotes can include escaped double
                # quotes, but singles can't
                ("dou\\ble\"", "quoted"),
                ("sin\\gle\\", "quoted"),
            ]
        )
        assert split_command(cmd) == expected

    def test_supports_windows_paths():
        cmd = "C:\\Windows\\Something 'C:\\Users'"
        expected = (
            "ok",
            [
                ("C:\\Windows\\Something", "simple"),
                ("C:\\Users", "quoted"),
            ]
        )
        assert split_command(cmd) == expected

    def test_handles_unclosed_quotes():
        cmd = "first \"second"
        expected = ("error", "Unclosed quote at character 7")
        assert split_command(cmd) == expected

    def test_handles_trailing_escape_char():
        cmd = "\\"
        expected = ("ok", [("\\", "simple")])
        assert split_command(cmd) == expected

    def test_does_not_crash():
        # Test we don't crash for any input
        tokens = ("a", "'", "\"", "\\", " ")

        # Set seed for stable test cases
        rand = random.Random(0)

        for _ in range(100):
            cmd = "".join(rand.choices(tokens, k=rand.randint(1, 10)))
            split_command(cmd)

    def test_matches_shlex():
        # Test we get the same result as shlex for a subset of cases

        # We do a different thing to shlex for the '\<non quote>' case to
        # better support Windows paths, so limit the tokens we use to generate
        # test cases to mutually compatible ones
        tokens = ("a", "'", "\"", "\\\"", "\\'", " ")

        # Set seed for stable test cases
        rand = random.Random(0)

        for _ in range(100):
            cmd = "".join(rand.choices(tokens, k=rand.randint(1, 10)))
            try:
                model = shlex.split(cmd)
            except ValueError:
                model = None
            success, result = split_command(cmd)

            # We can parse the same things as shlex
            assert (model is None) == (success == "error"), cmd

            # And when we parse successfully we get the same result as shlex
            if model is not None:
                raw = [m for m, _ in result]
                assert raw == model, cmd
