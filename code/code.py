from talon import Context, actions, ui, Module
import re
import os 
ctx = Context()
key = actions.key

extension_lang_map = {
"py"   : "python",
"cs"   : "csharp",
"cpp"  : "cplusplus",
"h"    : "cplusplus",
"talon": "talon",
}

# The [^\\\/] is specifically to avoid matching something like a .talon folder
# that would otherwise cause the .talon file action to load
regex_ext = re.compile("[^\\\/]\.(\S*)\s*")

@ctx.action_class('code')
class CodeActions:
    def language(): 
        title = ui.active_window().title
        #print(str(ui.active_app()))
        #workaround for VS Code on Mac. The title is "",
        #but the doc is correct.
        if title == "":
            title = ui.active_window().doc

        m = regex_ext.search(title)
        if m:
            extension = m.group(1)
            if extension in extension_lang_map:

                return extension_lang_map[extension]
            else:
                return extension
        return ""
