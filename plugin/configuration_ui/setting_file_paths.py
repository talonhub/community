from pathlib import Path

SETTINGS_DOT_TALON_PATH = Path(__file__).parent.parent.parent / "settings.talon"
MODE_INDICATOR_PATH = (
    Path(__file__).parent.parent / "mode_indicator" / "mode_indicator.talon"
)
SUBTITLES_PATH = Path(__file__).parent.parent / "subtitles" / "subtitles.talon"
RELEVANT_PATHS = [SETTINGS_DOT_TALON_PATH, MODE_INDICATOR_PATH, SUBTITLES_PATH]
