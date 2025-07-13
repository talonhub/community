from talon import Module, actions

mod = Module()

# Hotkey that is configured to activate Shortcat
SHORTCAT_HOTKEY = "cmd-shift-alt-]"
# Delay to wait for Shortcat to show the shortcuts
SHORTCUTS_DELAY = "500ms"


@mod.action_class
class Actions:
    def shortcat_hover(text: str):
        "Hover over a button using shortcat"
        actions.key(SHORTCAT_HOTKEY)
        actions.sleep(SHORTCUTS_DELAY)
        actions.insert(text)

    def shortcat_click(text: str, click_delay: str = "0ms"):
        "Click a button using shortcat"
        actions.user.shortcat_hover(text)
        actions.sleep(click_delay)
        actions.key("enter")
        actions.sleep("100ms")
        actions.mouse_click(0)

    def shortcat_double_click(text: str, click_delay: str = "0ms"):
        "Double click a button using shortcat"
        actions.user.shortcat_hover(text)
        actions.sleep(click_delay)
        actions.key("enter")
        actions.sleep("100ms")
        actions.mouse_click(0)
        actions.mouse_click(0)

    def shortcat_right(text: str, click_delay: str = "0ms"):
        "Right click a button using shortcat"
        actions.user.shortcat_hover(text)
        actions.sleep(click_delay)
        actions.key("ctrl-enter")
