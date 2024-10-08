tag: user.code_libraries_gui_showing
-
# The show functions for this have language specific names, e.g. toggle imports for Python
# but let's use a generic name for the close one. Having it behind this tag allows it to be closed
# even if your editor isn't visible.
import cell <number>: user.code_select_library(number - 1, "")
toggle libraries close: user.code_toggle_libraries()
