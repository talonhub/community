tag: user.code_libraries
-

state import:
    user.deprecate_command("2026-11-17", "state import", "snip import")
    user.code_import()

import <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    edit.line_insert_down()
