from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag("code_comment_line", desc="Tag for enabling generic line comment commands")


@mod.action_class
class Actions:
    def code_comment_line_prefix():
        """Inserts line comment prefix at current cursor location"""
        actions.user.insert_snippet_by_name("commentLine")
