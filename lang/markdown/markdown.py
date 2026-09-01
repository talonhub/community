from typing import Optional

from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: markdown
"""

mod.list("markdown_code_block_language", desc="Languages for code blocks")
ctx.lists["user.markdown_code_block_language"] = {
    "typescript": "typescript",
    "python": "python",
    "code": "",
    "ruby": "ruby",
    "shell": "shell",
    "bash": "bash",
    "json": "json",
    "are": "r",
    "markdown": "markdown",
}


@mod.action_class
class Actions:
    def markdown_insert_link(url: str, description: Optional[str] = None):
        """Inserts a markdown link filling in the url and optionally filling in the description"""
        substitutions = {"0": url}
        if description is not None:
            substitutions["1"] = description
        actions.user.insert_snippet_by_name("link", substitutions)

    def markdown_wrap_selection_with_link(url: str):
        """Wraps the selection with a markdown link for the specified url"""
        description = actions.edit.selected_text()
        actions.user.markdown_insert_link(url, description)

    def markdown_insert_table_header(num_columns: int):
        """Creates a table header with the given number of columns"""
        if num_columns <= 0:
            return
        # build a snippet
        # add the places to put the column names
        snippet_body_parts = ["|"]
        for i in range(num_columns):
            snippet_body_parts.append(f" ${i + 1} |")
        # add the dashed lines
        snippet_body_parts.append("\n|")
        for i in range(num_columns):
            snippet_body_parts.append("---|")
        # put it all together
        snippet_body = "".join(snippet_body_parts)
        # directly insert the snippet body.
        # Because the number of placeholders varies, we could not do this in a .snippet file.
        actions.user.insert_snippet(snippet_body)
