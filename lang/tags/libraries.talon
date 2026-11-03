tag: user.code_libraries
-

state import: user.code_import()

import <user.code_libraries>:
    user.code_insert_library(code_libraries, edit.selected_text())
    edit.line_insert_down()
