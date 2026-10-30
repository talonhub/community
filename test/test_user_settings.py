import io
import warnings
from pathlib import Path

import pytest
import talon

if hasattr(talon, "test_mode"):
    # UPDATE THIS IMPORT if your module has a different name
    import core.user_settings  # Imported for monkeypatching module globals
    from core.user_settings import (
        append_to_csv,
        needs_final_newline,
        parse_directories_setting,
        read_csv_list,
        read_csv_rows,
        write_csv_default_rows,
        write_csv_defaults,
    )

    BASE_DIR = Path("/fake/user/dir")

    @pytest.fixture(autouse=True)
    def mock_warn_about_error(monkeypatch):
        """Automatically mock warn_about_error in all tests to use standard Python warnings with an explicit stack level."""

        def mock_warn(message: str):
            warnings.warn(message, UserWarning, stacklevel=2)

        monkeypatch.setattr(core.user_settings, "warn_about_error", mock_warn)

    # --- Existing Directory Tests ---

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

    # --- CSV Reading Tests ---

    def test_read_csv_list_normal():
        csv_data = """output,spoken
cat,kitty
dog,doggy
"""
        f = io.StringIO(csv_data)
        f.name = "test.csv"
        result = read_csv_list(f, headers=("output", "spoken"))
        assert result == {"kitty": "cat", "doggy": "dog"}

    def test_read_csv_list_spoken_first():
        csv_data = """spoken,output
kitty,cat
doggy,dog
"""
        f = io.StringIO(csv_data)
        f.name = "test.csv"
        result = read_csv_list(
            f, headers=("spoken", "output"), is_spoken_form_first=True
        )
        assert result == {"kitty": "cat", "doggy": "dog"}

    def test_read_csv_list_edge_cases():
        csv_data = "output,spoken\n\nsingle\nout, spk \na,b,c\n"
        f = io.StringIO(csv_data)
        f.name = "test.csv"
        result = read_csv_list(f, headers=("output", "spoken"))
        assert result == {"single": "single", "spk": "out", "b": "a"}

    def test_read_csv_rows_three_columns():
        csv_data = """col1,col2,col3
a,b,c
1,2,3
"""
        f = io.StringIO(csv_data)
        f.name = "test.csv"
        result = read_csv_rows(f, headers=("col1", "col2", "col3"))
        assert result == [["a", "b", "c"], ["1", "2", "3"]]

    def test_read_csv_rows_empty_or_header_only():
        f_empty = io.StringIO("")
        f_empty.name = "empty.csv"
        with pytest.warns(UserWarning, match="empty.csv is empty!"):
            assert read_csv_rows(f_empty, headers=("col1",)) == []

        f_header = io.StringIO("col1,col2,col3\n")
        f_header.name = "header.csv"
        with pytest.warns(UserWarning, match="header.csv has only the header!"):
            assert read_csv_rows(f_header, headers=("col1", "col2", "col3")) == []

    def test_read_csv_rows_malformed_headers():
        csv_data = """bad_col,col2,col3
a,b,c
"""
        f = io.StringIO(csv_data)
        f.name = "malformed.csv"
        with pytest.warns(UserWarning, match="Malformed headers"):
            result = read_csv_rows(f, headers=("col1", "col2", "col3"))

        assert result == [["a", "b", "c"]]

    # --- CSV Writing & File Operations Tests ---

    def test_write_csv_defaults(tmp_path):
        csv_path = tmp_path / "test.csv"
        defaults = {"kitty": "cat", "same": "same"}

        write_csv_defaults(
            csv_path,
            headers=("spoken", "output"),
            default=defaults,
            is_spoken_form_first=True,
        )
        assert csv_path.exists()
        content = csv_path.read_text(encoding="utf-8")
        assert "spoken,output\n" in content
        assert "kitty,cat\n" in content
        assert "same\n" in content

        write_csv_defaults(
            csv_path, headers=("spoken", "output"), default={"new": "val"}
        )
        content2 = csv_path.read_text(encoding="utf-8")
        assert "new" not in content2

    def test_write_csv_default_rows_three_columns(tmp_path):
        csv_path = tmp_path / "test_rows.csv"
        defaults = [["a", "b", "c"], ["1", "2", "3"]]

        write_csv_default_rows(
            csv_path, headers=("col1", "col2", "col3"), default=defaults
        )
        content = csv_path.read_text(encoding="utf-8")
        assert "col1,col2,col3\n" in content
        assert "a,b,c\n" in content
        assert "1,2,3\n" in content

    def test_needs_final_newline(tmp_path):
        f_has = tmp_path / "has_newline.txt"
        f_has.write_text("hello\n", encoding="utf-8")
        assert not needs_final_newline(f_has)

        f_missing = tmp_path / "no_newline.txt"
        f_missing.write_text("hello", encoding="utf-8")
        assert needs_final_newline(f_missing)

        f_empty = tmp_path / "empty.txt"
        f_empty.write_text("", encoding="utf-8")
        assert not needs_final_newline(f_empty)

    def test_append_to_csv(monkeypatch, tmp_path):
        monkeypatch.setattr(core.user_settings, "COMMUNITY_ROOT_DIR", tmp_path)

        filename = "append_test.csv"
        settings_dir = tmp_path / "settings"
        settings_dir.mkdir(exist_ok=True)
        csv_path = settings_dir / filename

        csv_path.write_text("output,spoken\ncat,kitty", encoding="utf-8")

        append_to_csv(filename, {"doggy": "dog", "same": "same"}, private=False)

        content = csv_path.read_text(encoding="utf-8")
        assert "cat,kitty\n" in content
        assert "dog,doggy\n" in content
        assert "same\n" in content
