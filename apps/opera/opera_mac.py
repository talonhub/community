from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: opera
"""


@ctx.action_class("user")
class UserActions:
    def tab_duplicate():
        actions.browser.focus_address()
        actions.sleep("180ms")
        possibly_edited_url = actions.edit.selected_text()
        actions.key("esc:2")
        actions.browser.focus_address()
        actions.sleep("180ms")
        url_address = actions.edit.selected_text()
        actions.user.paste(possibly_edited_url)
        actions.app.tab_open()
        actions.user.paste(url_address)
        actions.key("enter")

    def tab_final():
        raise NotImplementedError(
            "Opera doesn't have a default shortcut for this functionality but it can be configured"
        )

    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()


@ctx.action_class("app")
class AppActions:
    def tab_next():
        actions.key("cmd-alt-right")

    def tab_previous():
        actions.key("cmd-alt-left")


@ctx.action_class("browser")
class BrowserActions:
    def bookmark_tabs():
        raise NotImplementedError("Opera doesn't support this functionality")

    def go_home():
        raise NotImplementedError("Opera doesn't support this functionality")

    def go_back():
        actions.browser.focus_page()
        actions.next()

    def go_forward():
        actions.browser.focus_page()
        actions.next()

    def show_downloads():
        actions.key("cmd-j")

    def show_extensions():
        actions.key("cmd-shift-e")

    def show_history():
        actions.key("cmd-shift-h")

    def focus_page():
        actions.key("cmd-alt-l")

    def reload_hard():
        actions.key("shift-5")
