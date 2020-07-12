from talon import ctrl, ui, Module, Context, actions, clip, app

ctx = Context()
ctx.matches = r'''
app: Safari
'''
@ctx.action_class('user')
class user_actions:
    def tab_jump(number: int):
        if number < 9:
            actions.key("cmd-{}".format(number))

    def tab_final():
        actions.key("cmd-9")