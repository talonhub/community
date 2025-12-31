from talon import Module, Context, actions

mod = Module()

mod.apps.microsoft_word = r"""
os: windows
and app.name: Microsoft Word
os: windows
and app.exe: /^winword\.exe$/i
"""
# mod.apps.microsoft_word = r"""
# os: windows
# and app.name: Microsoft Edge
# os: windows
# and app.exe: /^msedge\.exe$/i
# win.title: /\.docx/
# win.title: /\.doc/
# """

ctx = Context()
ctx.matches = """
app: microsoft_word
"""

@ctx.action_class("user")
class UserActions:
    # user.pages
    def page_current():
        actions.key("ctrl-shift-n")
        page = actions.edit.selected_text()
        actions.key("tab:2 enter")
        return int(page)

    def page_next():
        actions.key("ctrl-pagedown")

    def page_previous():
        actions.key("ctrl-pageup")

    def page_jump(number: int):
        actions.key("ctrl-g")
        actions.insert(str(number))
        actions.key("enter")

    def page_final():
        actions.key("ctrl-end")

    # def page_rotate_right():
    #     actions.key("shift-ctrl-0")

    # def page_rotate_left():
    #     actions.key("shift-ctrl-1")
