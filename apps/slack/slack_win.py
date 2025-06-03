from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: windows
os: linux
app: slack
"""


@ctx.action_class("user")
class UserActions:
    def messaging_workspace_previous():
        actions.key("ctrl-shift-tab")

    def messaging_workspace_next():
        actions.key("ctrl-tab")

    def messaging_open_channel_picker():
        actions.key("ctrl-k")

    def messaging_channel_previous():
        actions.key("alt-up")

    def messaging_channel_next():
        actions.key("alt-down")

    def messaging_unread_previous():
        actions.key("alt-shift-up")

    def messaging_unread_next():
        actions.key("alt-shift-down")

    # (go | undo | toggle) full: key(ctrl-cmd-f)
    def messaging_open_search():
        actions.key("ctrl-f")

    def messaging_mark_workspace_read():
        actions.key("shift-esc")

    def messaging_mark_channel_read():
        actions.key("esc")

    # Files and Snippets
    def messaging_upload_file():
        actions.key("ctrl-u")

    def slack_open_workspace(number: int):
        actions.key(f"ctrl-{number}")

    def slack_show_channel_info():
        actions.key("ctrl-shift-i")

    def slack_open_direct_messages():
        actions.key("ctrl-shift-k")

    def slack_open_threads():
        actions.key("ctrl-shift-t")

    def slack_go_back():
        actions.key('alt-left')

    def slack_go_forward():
        actions.key('alt-right')

    def slack_open_activity():
        actions.key("ctrl-shift-m")

    def slack_open_directory():
        actions.key("ctrl-shift-e")

    def slack_open_unread_messages():
        actions.key("ctrl-shift-a")

    def slack_toggle_full_screen():
        actions.key('ctrl-ctrl-f')
    
    def slack_add_reaction():
        actions.key('ctrl-shift-\\')
        
    def slack_insert_command():
        actions.key('ctrl-shift-c')

    def slack_insert_link():
        actions.key('ctrl-shift-u')

    def slack_insert_code():
        actions.insert("```")
       
    def slack_start_bulleted_list():
        actions.key('ctrl-shift-8')

    def slack_start_numbered_list():
        actions.key('ctrl-shift-7')

    def slack_insert_quotation():
        actions.key('ctrl-shift-9')

    def slack_toggle_bold():
        actions.key('ctrl-b')

    def slack_toggle_italic():
        actions.key('ctrl-i')

    def slack_toggle_strikethrough():
        actions.key('ctrl-shift-x')

    def slack_create_snippet():
        actions.key('ctrl-shift-enter')

    def slack_huddle():
        actions.key('ctrl-shift-h')

    def slack_open_keyboard_shortcuts():
        """Opens the keyboard shortcuts menu in Slack"""
        actions.key('ctrl-/')

    def slack_toggle_left_sidebar():
        """Toggles the visibility of the left sidebar in Slack"""
        actions.key('ctrl-shift-d')

    def slack_toggle_right_sidebar():
        """Toggles the visibility of the right sidebar in Slack"""
        actions.key('ctrl-.')