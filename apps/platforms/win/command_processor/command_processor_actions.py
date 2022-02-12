from talon import Context, actions
ctx = Context()
ctx.matches = r"""
app: windows_command_processor
app: windows_terminal
and win.title: /Command Prompt/
"""
ctx.tags = ['user.file_manager', 'user.git', 'user.kubectl', 'terminal']

@ctx.action_class('user')
class UserActions:
    def file_manager_refresh_title():
        actions.insert('title Command Prompt: %CD%')
        actions.key('enter')
        #action(user.file_manager_go_back):
        #    key("alt-left")
        #action(user.file_manager_go_forward):
        #    key("alt-right")
    def file_manager_open_parent():
        actions.insert('cd ..')
        actions.key('enter')
        actions.user.file_manager_refresh_title()

@ctx.action_class('edit')
class EditActions:
    def delete_line(): actions.key('esc')
