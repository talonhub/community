from talon import Context, actions

ctx = Context()

ctx.matches = r"""
tag: ultisnips
"""


@ctx.action_class("user")
class user_actions:
    def snippet_search(text: str):
        # XXX - to complete
        # actions.user.ide_command_palette()
        # actions.insert("Insert Snippet")
        actions.insert(text)

    def snippet_insert(text: str):
        """Inserts a snippet"""
        actions.user.vim_insert_mode(text)
        actions.key("tab")
