from talon import Context, actions, ui, Module, app
is_mac = app.platform == 'mac'

ctx = Context()
ctx.matches = r'''
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
'''
@ctx.action_class('win')
class win_actions:
    def filename(): 
        title = actions.win.title()
        #this doesn't seem to be necessary on VSCode for Mac
        #if title == "":
        #    title = ui.active_window().doc
    
        if is_mac:
            result = title.split(" — ")[0]
        else:
            result = title.split(" - ")[0]

        if "." in result:
            return result
    
        return ""

    def file_ext():
        return actions.win.filename().split(".")[-1]
