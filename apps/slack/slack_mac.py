from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: slack
"""


@ctx.action_class("user")
class UserActions:
    def messaging_workspace_previous():
        actions.key("cmd-shift-[")

    def messaging_workspace_next():
        actions.key("cmd-shift-]")

    def messaging_open_channel_picker():
        actions.key("cmd-k")

    def messaging_channel_previous():
        actions.key("alt-up")

    def messaging_channel_next():
        actions.key("alt-down")

    def messaging_unread_previous():
        actions.key("alt-shift-up")

    def slack_open_starred_items():
        actions.key("cmd-shift-s")

    def messaging_unread_next():
        actions.key("alt-shift-down")

    def messaging_open_search():
        actions.key("cmd-f")

    def messaging_mark_workspace_read():
        actions.key("shift-esc")

    def messaging_mark_channel_read():
        actions.key("esc")

    # Files and Snippets
    def messaging_upload_file():
        actions.key("cmd-u")

    def slack_open_workspace(number: int):
        actions.key(f"cmd-{number}")

    def slack_show_channel_info():
        actions.key("cmd-shift-i")

    def slack_open_direct_messages():
        actions.key("cmd-shift-k")

    def slack_open_threads():
        actions.key("cmd-shift-t")

    def slack_go_back():
        actions.key("cmd-[")

    def slack_go_forward():
        actions.key("cmd-]")

    def slack_open_activity():
        actions.key("cmd-shift-m")

    def slack_open_directory():
        actions.key("cmd-shift-e")

    def slack_open_unread_messages():
        actions.key("cmd-shift-a")

    def slack_toggle_full_screen():
        actions.key('ctrl-cmd-f')
    
    def slack_add_reaction():
        actions.key('cmd-shift-\\')
        
    def slack_insert_command():
        actions.key('cmd-shift-c')

    def slack_insert_link():
        actions.key('cmd-shift-u')

    def slack_insert_code():
        actions.key('cmd-shift-alt-c')
       
    def slack_start_bulleted_list():
        actions.key('cmd-shift-8')

    def slack_start_numbered_list():
        actions.key('cmd-shift-7')

    def slack_insert_quotation():
        actions.key('cmd-shift->')

    def slack_toggle_bold():
        actions.key('cmd-b')

    def slack_toggle_italic():
        actions.key('cmd-i')

    def slack_toggle_strikethrough():
        actions.key('cmd-shift-x')

    def slack_create_snippet():
        actions.key('cmd-shift-enter')

    def slack_huddle():
        actions.key('cmd-shift-h')

    def slack_open_keyboard_shortcuts():
        """Opens the keyboard shortcuts menu in Slack"""
        actions.key('cmd-/')

    def slack_toggle_left_sidebar():
        """Toggles the visibility of the left sidebar in Slack"""
        actions.key('cmd-shift-d')

    def slack_toggle_right_sidebar():
        """Toggles the visibility of the right sidebar in Slack"""
        actions.key('cmd-.')