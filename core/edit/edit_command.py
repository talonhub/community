from talon import Module, actions

from .edit_command_actions import EditAction, get_action_callback
from .edit_command_modifiers import EditModifier, get_modifier_callback

# In some cases there already is a "compound" talon action for a given action and modifier
compound_actions = {
    # Select
    "select.word": actions.edit.select_word,
    "select.line": actions.edit.select_line,
    "select.paragraph": actions.edit.select_paragraph,
    "select.document": actions.edit.select_all,
    # Go before
    "goBefore.line": actions.edit.line_start,
    "goBefore.paragraph": actions.edit.paragraph_start,
    "goBefore.document": actions.edit.file_start,
    # Go after
    "goAfter.line": actions.edit.line_end,
    "goAfter.paragraph": actions.edit.paragraph_end,
    "goAfter.document": actions.edit.file_end,
    # Delete
    "delete.word": actions.edit.delete_word,
    "delete.line": actions.edit.delete_line,
    "delete.paragraph": actions.edit.delete_paragraph,
    "delete.document": actions.edit.delete_all,
}


mod = Module()


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifier: EditModifier):
        """Perform edit command"""

        # string joined of action and modifier
        key = f"{action}.{modifier}"

        try:
            if key in compound_actions:
                compound_actions[key]()
                return

            action_callback = get_action_callback(action)
            modifier_callback = get_modifier_callback(modifier)

            modifier_callback()
            action_callback()
        except ValueError as ex:
            actions.app.notify(str(ex))
            raise ex
