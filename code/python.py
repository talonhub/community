from talon import Module, Context, actions, ui, imgui

mod = Module()
ctx = Context()

mod.list('python_functions')

python_functions_dict = {"print": "print",
                         "length": "len",
                         "string": "str",
                         "int": "int",
                         "enumerate": "enumerate",
                         "update": "update",
                         "split": "split",
                         "set": "set",
                         "list": "list",
                         "range": "range"}


@mod.capture
def python_functions(m) -> str:
    "Returns a comma separated string of functions"

@mod.capture
def print_function(m) -> str:
    "Returns one of the python functions in the list"

@mod.action_class
class Actions:
    def list_python_functions():
        """List all known functions"""
        gui.show()
        gui.freeze()

    def hide_python_functions():
        """Hides list of all known functions"""
        gui.hide()

@ctx.capture(rule='{self.python_functions}+')
def python_functions(m):
    return ','.join(m.python_functions_list)

@ctx.capture(rule='<self.python_functions>')
def print_function(m):
    return python_functions_dict[m.python_functions]

ctx.lists['self.python_functions'] = python_functions_dict.keys()

@imgui.open(software=False)
def gui(gui: imgui.GUI):
    gui.text("Python functions")
    gui.line()
    for item in python_functions_dict.items():
        gui.text(f"{item[0]}: {item[1]}")
