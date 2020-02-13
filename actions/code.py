from talon import Context, actions, ui, Module
import re

ctx = Context()
key = actions.key

extension_lang_map = {
"py"   : "python",
"cs"   : "csharp",
"cpp"  : "cplusplus",
"h"    : "cplusplus",
"talon": "talon",
}

regex_ext = re.compile("\.(\S*)\s")
 
@ctx.action_class('code')
class CodeActions:
    def language(): 
        m = regex_ext.search(ui.active_window().title)
        if m:
            extension = m.group(1)
            if extension in extension_lang_map:
                return extension_lang_map[extension]
            else:
                return extension
        return ""
