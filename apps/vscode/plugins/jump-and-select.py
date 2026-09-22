from talon import Context, actions

ctx = Context()
ctx.matches = r"""
    app: vscode
    user.plugin_installed: arturodent.jump-and-select
"""


@ctx.action_class("user")
class UserActions:
    def jump_cursor_to_next_char(char: str):
        actions.user.vscode("jump-and-select.jumpForward")
        actions.key(char)

    def jump_cursor_to_prev_char(char: str):
        actions.user.vscode("jump-and-select.jumpBackward")
        actions.key(char)
