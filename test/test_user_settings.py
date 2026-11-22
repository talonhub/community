from pathlib import Path

import talon

if hasattr(talon, "test_mode"):
    from core.user_settings import parse_directories_setting

    BASE_DIR = Path("/fake/user/dir")

    def test_parse_directories_setting_empty():
        assert parse_directories_setting(None, BASE_DIR) == []
        assert parse_directories_setting("", BASE_DIR) == []
        assert parse_directories_setting("   ", BASE_DIR) == []

    def test_parse_directories_setting_single_relative():
        expected = [(BASE_DIR / "snippets").resolve()]
        assert parse_directories_setting("snippets", BASE_DIR) == expected

    def test_parse_directories_setting_single_absolute():
        expected = [Path("/opt/snippets").resolve()]
        assert parse_directories_setting("/opt/snippets", BASE_DIR) == expected

    def test_parse_directories_setting_with_spaces():
        expected = [(BASE_DIR / "my custom snippets/python").resolve()]
        assert (
            parse_directories_setting("my custom snippets/python", BASE_DIR) == expected
        )

    def test_parse_directories_setting_multiple_paths():
        raw = """
            my_snippets
             /var/snippets
             ~/custom snippets/lang
            """
        expected = [
            (BASE_DIR / "my_snippets").resolve(),
            Path("/var/snippets").resolve(),
            (Path.home() / "custom snippets/lang").resolve(),
        ]
        assert parse_directories_setting(raw, BASE_DIR) == expected
