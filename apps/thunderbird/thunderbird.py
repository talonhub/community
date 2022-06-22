from talon import Context, Module

# --- App definitions ---
# Main app TODO: mac context
mod = Module()
mod.apps.thunderbird = """
os: windows
and app.name: Thunderbird
os: windows
and app.exe: thunderbird.exe
"""
mod.apps.thunderbird = """
os: linux
and app.name: Thunderbird
"""

# Inbox tab TODO: also matches emails opened in new tab
mod.apps.thunderbird_inbox = """
app: thunderbird
title: /@/
"""

# Calendar tab (lightning)
months = [
    "January",  # English
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "Januar",  # German
    "Februar",
    "März",
    "Mai",
    "Juni",
    "Juli",
    "Oktober",
    "Dezember",
]
mod.apps.thunderbird_calendar = f"""
app: thunderbird
title: Calendar - Mozilla Thunderbird
title: Kalender - Mozilla Thunderbird
title: /({"|".join(map(lambda m: m + " ", months))})/
"""

# Tasks tab
mod.apps.thunderbird_tasks = """
app: thunderbird
title: Tasks - Mozilla Thunderbird
title: Aufgaben - Mozilla Thunderbird
"""

# Mail composer window
mod.apps.thunderbird_composer = """
app: thunderbird
title: /Write: /
title: /Verfassen: /
"""

# Address book popup window
mod.apps.thunderbird_contacts = """
app: thunderbird
title: Address Book
title: Adressbuch
"""

# Context matching
ctx = Context()
ctx.matches = r"""
app: thunderbird
"""


# --- Define actions ---
@mod.action_class
class UserActions:
    def thunderbird_mod(keys: str):
        """Press keys with modifier ctrl or cmd"""

    def thunderbird_calendar_view(number: int):
        """Select between calendar view tabs"""


# --- Implement actions ---
@ctx.action_class("app")
class AppActions:
    # app.tabs
    # not possible in thunderbird
    def tab_open():
        pass
