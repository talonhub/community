from talon import Context, Module, registry, actions

mod = Module()
ctx = Context()

@mod.action_class
class Actions:
    def rails_console():
        """runs rails console"""
    def rails_server():
        """runs rails server"""

@ctx.action_class('user')
class UserActions:
    def rails_console():
      actions.insert("rails c")
      actions.key("enter")

    def rails_server():
      actions.insert('rails s 2>&1 | tee ../arc.log')
      actions.key("enter")
