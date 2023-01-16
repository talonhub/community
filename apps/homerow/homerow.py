from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()
mod.apps.homerow = """
os: mac
and app.bundle: com.dexterleng.Homerow
"""

mod.tag("homerow_search")



@mod.action_class
class Actions:
    def homerow_search(text: str):
        """Search in Homerow"""

        if (
            len(ctx.tags) > 0
            and (focused_element := ui.focused_element())
            and win_is_homerow_search_bar(focused_element.window)
        ):
            focused_element.AXValue = text.lower()
            return

        # TODO(nriley): Consider always using accessibility?
        actions.key("cmd-shift-space")
        actions.sleep("50ms")
        

    def homerow_pick(label: str, mouse_action: str):
        """pick in Homerow"""
        actions.insert(label.upper())
        if "left" == mouse_action:
            actions.key("enter")
        elif "right" == mouse_action:
            actions.key("shift-enter")
        elif "double" == mouse_action:
            actions.key("enter")
            actions.sleep("50ms")
            actions.key("enter")
        elif "command" == mouse_action:
            actions.key("cmd-enter")
    
        complete_homerow_search()


def complete_homerow_search():
    ctx.tags = []
    ui.unregister("element_focus", element_focus)


def element_focus(element):
    complete_homerow_search()


def win_is_homerow_search_bar(win):
    return (
        win.app.bundle == "com.dexterleng.Homerow" and win.title == "Homerow Search Bar"
    )


def win_open(win):
    if not win_is_homerow_search_bar(win):
        return
    if len(ctx.tags) == 0:
        ctx.tags = ["user.homerow_search"]
        ui.register("element_focus", element_focus)


if app.platform == "mac":
    app.register("ready", lambda: ui.register("win_open", win_open))
