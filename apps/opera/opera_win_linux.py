from talon import Context, actions, app

ctx = Context()
ctx.matches = r"""
os: windows
os: linux
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

    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-{number}")

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
        actions.key("ctrl-pagedown")

    def tab_previous():
        actions.key("ctrl-pageup")


@ctx.action_class("browser")
class BrowserActions:
    def bookmarks_bar():
        raise NotImplementedError(
            "Opera doesn't have a default shortcut for this functionality but it can be configured"
        )

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

    def bookmarks():
        actions.key("ctrl-shift-b")

    def show_downloads():
        actions.key("ctrl-j")

    def show_extensions():
        actions.key("ctrl-shift-e")

    def focus_page():
        actions.key("f9")

    def reload_hard():
        actions.key("shift-5")
