from talon import Context, actions

# Context matching
ctx = Context()
ctx.matches = """
os: windows
app: adobe_acrobat_reader_dc
"""


# --- Implement actions ---
@ctx.action_class('app')
class AppActions:
    # app.tabs
    def tab_next(): actions.key('ctrl-tab')
    def tab_previous(): actions.key('ctrl-shift-tab')


@ctx.action_class('edit')
class EditActions:
    def zoom_in(): actions.key("ctrl-0")  # in german version
    def zoom_out(): actions.key("ctrl-1")  # in german version TODO: differentiate languages
    def zoom_reset(): actions.key("ctrl-2")


@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_current():
        actions.key("ctrl-shift-n")
        page = actions.edit.selected_text()
        actions.key("tab:2 enter")
        return int(page)
    def page_next(): actions.key("ctrl-pagedown")
    def page_previous(): actions.key("ctrl-pageup")
    def page_jump(number: int):
        actions.key("ctrl-shift-n")
        actions.insert(str(number))
        actions.key("enter")
    def page_final(): actions.key("end")
