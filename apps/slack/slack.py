from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
mod.setting(
    "slack_contact_delay",
    type=int,
    default=400,
    desc="Milliseconds to wait for Slack dialogs when messaging a contact",
)
apps = mod.apps
apps.slack = "app.name: Slack"
mod.apps.slack = r"""
os: windows
and app.name: Slack
os: windows
and app.exe: /^slack\.exe$/i
"""
apps.slack = """
os: mac
and app.bundle: com.tinyspeck.slackmacgap
"""
apps.slack = """
tag: browser
browser.host: app.slack.com
"""
ctx.matches = r"""
app: slack
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_down():
        actions.edit.line_end()
        actions.key("shift-enter")


@mod.action_class
class Actions:
    def slack_open_workspace(number: int):
        """Opens the specified Slack workspace"""

    def slack_show_channel_info():
        """Shows the current channel's information"""

    def slack_section_next():
        """Selects the next Slack section"""
        actions.key("f6")

    def slack_section_previous():
        """Selects the previous Slack section"""
        actions.key("shift-f6")

    def slack_open_direct_messages():
        """Opens direct messages in Slack"""

    def slack_open_threads():
        """Opens threads in Slack"""

    def slack_go_back():
        """Navigates back in Slack"""

    def slack_go_forward():
        """Navigates forward in Slack"""

    def slack_open_activity():
        """Opens Activity in Slack"""

    def slack_open_directory():
        """Opens Directory in Slack"""

    def slack_open_unread_messages():
        """Opens Unread Messages in Slack"""

    def slack_open_starred_items():
        """Opens Starred Items in Slack"""

    def slack_toggle_full_screen():
        """Toggles full screen mode in Slack"""

    def slack_add_reaction():
        """Adds a reaction to the current message in Slack"""

    def slack_insert_command():
        """Inserts a command in Slack"""

    def slack_insert_link():
        """Inserts a link in Slack"""

    def slack_insert_code():
        """Inserts a code block in Slack"""

    def slack_start_bulleted_list():
        """Starts a bulleted list in Slack"""

    def slack_start_numbered_list():
        """Starts a numbered list in Slack"""

    def slack_insert_quotation():
        """Inserts a quotation in Slack"""

    def slack_toggle_bold():
        """Toggles bold formatting in Slack"""

    def slack_toggle_italic():
        """Toggles italic formatting in Slack"""

    def slack_toggle_strikethrough():
        """Toggles strikethrough formatting in Slack"""

    def slack_create_snippet():
        """Opens the menu for creating a snippet in Slack"""

    def slack_huddle():
        """Starts a huddle in Slack"""

    def slack_open_keyboard_shortcuts():
        """Opens the keyboard shortcuts menu in Slack"""

    def slack_toggle_left_sidebar():
        """Toggles the visibility of the left sidebar in Slack"""

    def slack_toggle_right_sidebar():
        """Toggles the visibility of the right sidebar in Slack"""

    def slack_open_new_message():
        """Opens a new message in Slack"""

    def slack_message_contact(name: str):
        """Opens a direct message to the given person in Slack"""
        delay = f"{settings.get('user.slack_contact_delay')}ms"
        actions.key("escape")
        actions.user.slack_open_new_message()
        actions.sleep(delay)
        actions.edit.select_line()
        actions.insert(name)
        actions.sleep(delay)
        actions.key("enter")
        actions.sleep(delay)
        # Move focus from the recipient field to the message field
        actions.key("tab")

    def slack_search_messages_from(name: str):
        """Searches Slack for messages sent by the given person"""
        delay = f"{settings.get('user.slack_contact_delay')}ms"
        actions.key("escape")
        actions.user.messaging_open_search()
        actions.sleep(delay)
        # Replace the "in:#channel" filter that Slack prefills
        actions.edit.select_line()
        actions.insert(f"from:@{name}")
        actions.sleep(delay)
        actions.key("enter")
