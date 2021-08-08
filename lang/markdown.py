from talon import Module, Context

mod = Module()
ctx = Context()
ctx.matches = r"""
mode: user.markdown
mode: command 
and code.language: markdown
"""

mod.list("markdown_code_block_language", desc="Languages for code blocks")
ctx.lists["user.markdown_code_block_language"] = {
    "typescript": "typescript",
    "python": "python",
    "code": "",
}