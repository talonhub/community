app: vscode
-
{self.simple_cursorless_action} <user.cursorless_arg>:
    user.cursorless_single_target_command(simple_cursorless_action, cursorless_arg)

drink <user.cursorless_arg>:
    user.cursorless_single_target_command("setSelection", cursorless_arg)
    user.new_line_above()

pour <user.cursorless_arg>:
    user.cursorless_single_target_command("setSelection", cursorless_arg)
    user.new_line_below()

wrap <user.cursorless_arg> with funk <user.code_functions>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "{code_functions}(", ")")

square wrap <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "[", "]")

round wrap <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "(", ")")

curly wrap <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "{", "}")

(diamond | angle) wrap <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "<", ">")

quad wrap <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "\"", "\"")

twin wrap <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "'", "'")

puff <user.cursorless_arg>:
    user.cursorless_single_target_command("wrap", cursorless_arg, "\n", "\n")

extract <user.cursorless_arg> as <user.text>:
    user.cursorless_single_target_command("extractVariable", cursorless_arg)
    sleep(250ms)
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))
    key(enter)

action(user.dental_click): user.vscode("cursorless.toggleDecorations")