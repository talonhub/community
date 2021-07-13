from talon import Context, actions, ui, Module, app, clip

mod = Module()
# This is a huge hack! I am opening roamresearch in brave,  to be able to recognize it with talon
#  otherwise  roam opens in new window but in the same process  as the main chrome browser,  that would be fine
#  if  roam had a nice title that talon could recognize,  but this is not the case.
mod.apps.roam = "app.name: Brave-browser"
ctx = Context()
ctx.matches = r"""
app: roam
"""


# @ctx.action_class("edit")
# class edit_actions:
#     def page_down():
#         actions.key("shift-pagedown")

#     def find(text: str):
#         actions.key("ctrl-shift-f")
#         actions.insert(text)

#     def page_up():
#         # print(100 * "fsdafs\n")
#         actions.key("shift-pageup")

#     def paste():
#         actions.key("ctrl-shift-v")

#     def copy():
#         actions.key("ctrl-shift-c")


# @ctx.action_class("app")
# class user_actions:
#     def tab_next():
#         actions.key("ctrl-pagedown")

#     def tab_open():
#         actions.key("ctrl-shift-t")

#     def tab_close():
#         actions.key("ctrl-shift-w")

#     def tab_previous():
#         actions.key("ctrl-pageup")
