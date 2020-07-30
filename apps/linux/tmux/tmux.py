from talon import Context, actions, Module 
from time import sleep
ctx = Context()
mod = Module()

ctx.matches = r'''
tag: tmux
'''
@ctx.action_class('user')
class user_actions:
    def split_number(index: int):
        actions.key("ctrl-b")
        actions.key("q")
        sleep(0.5)
        actions.key("{}".format(index))
