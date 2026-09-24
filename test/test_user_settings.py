from pathlib import Path

import talon

if hasattr(talon, "test_mode"):
    from core.user_settings import parse_snippet_dirs

    BASE_DIR = Path("/fake/user/dir")

    def test_parse_snippet_dirs_empty():
        assert parse_snippet_dirs(None, BASE_DIR) == []
        assert parse_snippet_dirs("", BASE_DIR) == []
        assert parse_snippet_dirs("   ", BASE_DIR) == []

    def test_parse_snippet_dirs_single_relative():
        expected = [(BASE_DIR / "snippets").resolve()]
        assert parse_snippet_dirs("snippets", BASE_DIR) == expected

    def test_parse_snippet_dirs_single_absolute():
        expected = [Path("/opt/snippets").resolve()]
        assert parse_snippet_dirs("/opt/snippets", BASE_DIR) == expected

    def test_parse_snippet_dirs_with_spaces():
        expected = [(BASE_DIR / "my custom snippets/python").resolve()]
        assert parse_snippet_dirs("my custom snippets/python", BASE_DIR) == expected

    def test_parse_snippet_dirs_multiple_paths():
        raw = " my_snippets | /var/snippets | custom snippets/lang "
        expected = [
            (BASE_DIR / "my_snippets").resolve(),
            Path("/var/snippets").resolve(),
            (BASE_DIR / "custom snippets/lang").resolve(),
        ]
        assert parse_snippet_dirs(raw, BASE_DIR) == expected
