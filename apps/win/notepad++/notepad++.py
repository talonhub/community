from talon import Context, actions, ui, Module
ctx = Context()

ctx.matches = r'''
app: Notepad++ : a free (GNU) source code editor
app: notepad++.exe
'''
@ctx.action_class('win')
class win_actions:
    def filename(): 
        title = actions.win.title()
        result = title.split(" - ")[0]
        if "." in result:
            #print(result.split("\\")[-1])
            return result.split("\\")[-1]
        return ""

    def file_ext():
        return actions.win.filename().split(".")[-1]

@ctx.action_class('user')
class user_actions:
    def go_to_line(line: int):
        actions.key("ctrl-g")
        actions.insert(str(line))
        actions.key("enter")

    def tab_jump(number: int):
        if number < 10:
            actions.key("ctrl-keypad_{}".format(number))

    def tab_final():
        """Jumps to the final tab"""
        print("Notepad doesn't support this...")
        #actions.key("ctrl-numpad_0")