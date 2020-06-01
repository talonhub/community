from talon import Context, actions, ui, Module
import re
import os 
ctx = Context()
key = actions.key

extension_lang_map = {
    "py": "python",
    "cs": "csharp",
    "cpp": "cplusplus",
    "h": "cplusplus",
    "talon": "talon",
    "gdb": "gdb",
    "md": "markdown",
    "sh": "bash",
    "go": "go"
}

# The [^\\\/] is specifically to avoid matching something like a .talon folder
# that would otherwise cause the .talon file action to load
forced_language = False

@ctx.action_class('code')
class code_actions:
    def language(): 
        result = ""
        if not forced_language:
            file_extension = actions.win.file_ext()
            file_name = actions.win.filename()

            if file_extension != "":
                result = file_extension
            #it should always be the last split...
            elif file_name != "" and "." in file_name:
                result = file_name.split(".")[-1]

            if result in extension_lang_map:
                result = extension_lang_map[result]
        
        #print("code.language: " + result)
        return result

mod = Module()

#create a mode for each defined language
for __, lang in extension_lang_map.items():
    mod.mode(lang)

@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        global forced_language
        for __, lang in extension_lang_map.items():
            if lang != language:
                actions.mode.disable("user.{}".format(lang))
            else:
                actions.mode.enable("user.{}".format(lang))

        forced_language = True

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        global forced_language
        forced_language = False

        for __, lang in extension_lang_map.items():
            actions.mode.disable("user.{}".format(lang))


    