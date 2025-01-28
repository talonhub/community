from talon import Module, actions

from .edit_command_actions import EditAction, run_action_callback
from .edit_command_modifiers import EditModifier, run_modifier_callback

# In some cases there already is a "compound" talon action for a given action and modifier
compound_actions = {
    # Go before
    ("goBefore", "line"): actions.edit.line_start,
    ("goBefore", "paragraph"): actions.edit.paragraph_start,
    ("goBefore", "document"): actions.edit.file_start,
    ("goBefore", "fileStart"): actions.edit.file_start,
    # Go after
    ("goAfter", "line"): actions.edit.line_end,
    ("goAfter", "paragraph"): actions.edit.paragraph_end,
    ("goAfter", "document"): actions.edit.file_end,
    ("goAfter", "fileEnd"): actions.edit.file_end,
    # Delete
    ("delete", "word"): actions.edit.delete_word,
    ("delete", "line"): actions.edit.delete_line,
    ("delete", "paragraph"): actions.edit.delete_paragraph,
    # ("delete", "document"): actions.edit.delete_all, # Beta only
    # Cut to clipboard
    ("cutToClipboard", "line"): actions.user.cut_line,
}


mod = Module()


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifier: EditModifier):
        """Perform edit command"""
        key = (action.type, modifier.type)

        if key in compound_actions:
            compound_actions[key]()
            return

        run_modifier_callback(modifier)
        run_action_callback(action)
