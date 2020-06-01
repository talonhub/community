from talon import Context, actions, ui, Module

ctx_vscode = Context()

ctx_vscode.matches = r'''
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
'''
@ctx_vscode.action_class('win')
class win_actions:
    def filename(): 
        title = actions.win.title()
        result = title.split(" - ")[0]
        if "." in result:
            return result
        return ""

    def file_ext():
        return actions.win.filename().split(".")[-1]
