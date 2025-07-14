from talon import Module, actions, settings

mod = Module()

mod.setting(
    "shortcat_hotkey",
    type=str,
    default="cmd-shift-space",
    desc="Hotkey that is configured to activate Shortcat",
)
mod.setting(
    "shortcat_click_delay",
    type=str,
    default="500ms",
    desc="Delay to wait for Shortcat to show the shortcuts before clicking",
)


@mod.action_class
class Actions:
    def shortcat_hover(text: str):
        "Hover over a button using shortcat"
        actions.key(settings.get("user.shortcat_hotkey"))
        actions.sleep(settings.get("user.shortcat_click_delay"))
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
