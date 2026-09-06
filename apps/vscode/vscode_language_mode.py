import re

from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: vscode
not tag: user.code_language_forced
win.title: /lang:\[\w*\]/
"""

# Looks for special string in window title.
# NOTE: This requires you to add a special setting to your VSCode settings.json
# See [our vscode docs](./README.md#language-detection) for details
LANGUAGE_RE = re.compile(r"lang:\[(\w+)\]")


@ctx.action_class("code")
class CodeActions:
    def language():
        title: str = actions.win.title()
        match = LANGUAGE_RE.search(title)
        if match is not None:
            return match.group(1)
        return ""
