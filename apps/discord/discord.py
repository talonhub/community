from talon import Context, Module

mod = Module()
apps = mod.apps
apps.discord = "app.name: Discord"
apps.discord = "app.name: Discord.exe"
apps.discord = """
tag: browser
browser.host: discord.com
"""

mod.list("discord_destination", desc="discord destination")

ctx = Context()
ctx.matches = r"""
app: discord
"""

ctx.lists["user.discord_destination"] = {
    "user": "@",
    "channel": "#",
    "voice": "!",
    "server": "*",
}


@mod.action_class
class discord_actions:
    def discord_mentions_last():
        """Go up to channel with unread mentions"""

    def discord_mentions_next():
        """Go down to channel with unread mentions"""

    def discord_oldest_unread():
        """Go to oldest unread message"""

    def discord_toggle_pins():
        """Toggle pins popout"""

    def discord_toggle_inbox():
        """Toggle inbox popout"""

    def discord_toggle_members():
        """Toggle channel member list"""

    def discord_emoji_picker():
        """Toggle emoji picker"""

    def discord_gif_picker():
        """Toggle gif picker"""

    def discord_mark_inbox_read():
        """Mark top inbox channel read"""

    def discord_mute():
        """Toggle mute"""

    def discord_deafen():
        """Toggle deafen"""

    def discord_answer_call():
        """Answer incoming call"""

    def discord_decline_call():
        """Decline incoming call"""

    def discord_quick_switcher(dest_type: str, dest_search: str):
        """Open up the quick switcher, optionally specifying a type of destination"""

    def discord_go_current_call():
        """Go to current call"""

    def discord_toggle_dms():
        """Toggle between dms and your most recent server"""
