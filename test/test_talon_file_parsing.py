import talon

if hasattr(talon, "test_mode"):
    from plugin.configuration_ui.talon_file_parsing import (
        SettingFileSettingInformation,
        SettingsParser,
    )

    class MockPath:
        def __init__(self, text):
            self.text = text

        def read_text(self):
            return self.text

    def _assert_parser_matches_expected(
        input_text, settings, duplicate_tags, duplicate_settings, tags
    ):
        path = MockPath(input_text)
        parser = SettingsParser(path)
        print(parser.settings)
        assert settings == parser.settings
        assert duplicate_tags == parser.duplicate_tags
        assert duplicate_settings == parser.duplicate_settings
        assert tags == parser.tags
        assert input_text.splitlines() == parser.lines

    def test_handles_no_duplicates():
        test_case = r'''settings():
    # Adjust the scale of the imgui
    imgui.scale = 1.3

    # Uncomment to set the speech timeout. This is the amount of time after you stop
    # speaking until Talon starts processing the spoken audio. Default is 0.3s.
  # speech.timeout = 0.3

    user.snippets_dir = """
    multiline string
    multiple lines"""

    # user.commented_multiline = """
    # multiline string
    # multiple lines
    # """

# tag(): user.unprefixed_numbers
tag(): user.pop_to_repeat
'''
        settings = {
            "imgui.scale": SettingFileSettingInformation(
                1.3, 2, 3, assignment_prefix="    "
            ),
            "user.snippets_dir": SettingFileSettingInformation(
                "multiline string\nmultiple lines",
                8,
                11,
                True,
                assignment_prefix="    ",
            ),
            "speech.timeout": SettingFileSettingInformation(
                0.3, 6, 7, is_activated=False, assignment_prefix="  # "
            ),
            "user.commented_multiline": SettingFileSettingInformation(
                "multiline string\nmultiple lines\n",
                12,
                16,
                is_activated=False,
                assignment_prefix="    # ",
            ),
        }
        tags = {
            "user.unprefixed_numbers": SettingFileSettingInformation(False, 17, 18),
            "user.pop_to_repeat": SettingFileSettingInformation(True, 18, 19),
        }
        _assert_parser_matches_expected(test_case, settings, set(), set(), tags)

    def test_handles_more_kinds_of_values():
        test_case = r"""settings()
    user.a="test"
    user.b=12
    user.c=false
    user.d=true
    user.e = '''
    a
    '''
"""
        prefix = " " * 4
        settings = {
            "user.a": SettingFileSettingInformation(
                "test", 1, 2, assignment_prefix=prefix
            ),
            "user.b": SettingFileSettingInformation(12, 2, 3, assignment_prefix=prefix),
            "user.c": SettingFileSettingInformation(
                False, 3, 4, assignment_prefix=prefix
            ),
            "user.d": SettingFileSettingInformation(
                True, 4, 5, assignment_prefix=prefix
            ),
            "user.e": SettingFileSettingInformation(
                "a\n", 5, 8, assignment_prefix=prefix
            ),
        }
        _assert_parser_matches_expected(test_case, settings, set(), set(), {})

    def test_handles_duplicate_tags():
        test_case = r"""tag(): user.a
tag(): user.a
tag(): user.b
#tag(): user.b
tag(): user.c
"""
        tags = {"user.c": SettingFileSettingInformation(True, 4, 5)}
        duplicate_tags = {"user.a", "user.b"}
        _assert_parser_matches_expected(test_case, {}, duplicate_tags, set(), tags)

    def test_handles_duplicate_settings():
        test_case = r"""settings():
    user.a = 6
    user.a = 7
    user.b = 5
    # user.b = 5
    user.c = 1
"""
        settings = {"user.c": SettingFileSettingInformation(1, 5, 6, assignment_prefix=" "*4)}
        duplicate_settings = {"user.a", "user.b"}
        _assert_parser_matches_expected(test_case, settings, set(), duplicate_settings, {})