from talon import Context, actions
ctx = Context()
ctx.matches = r"""
os: windows
and app.exe: ONENOTE.EXE
"""

@ctx.action_class('edit')
class EditActions:
    def select_line(n: int=None):
        actions.key('ctrl-a')