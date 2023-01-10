from talon import clip, Module, actions

module = Module()
clipboard_sleep_setting = module.setting(
    'google_sheets_clipboard_delay',
    type = float,
    default = 0.2,
    desc = 'How long to pause when using the clipboard with google sheets commands. Try increasing this if those commands are not working.'
)

def wait_long_enough_to_let_clipboard_revert_properly():
    actions.sleep(clipboard_sleep_setting.get())

def get_selected_text_using_clipboard() -> str:
    with clip.revert():
        actions.edit.copy()
        wait_long_enough_to_let_clipboard_revert_properly()
        result = clip.text()
    return result
