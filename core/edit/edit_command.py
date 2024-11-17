from talon import Module, actions
from typing import Union

from .edit_command_actions import EditAction, run_action_callback
from .edit_command_modifiers import EditModifier, run_modifier_callback

# In some cases there already is a "compound" talon action for a given action and modifier
compound_actions = {
    # selection
    ("selection", "wordLeft"): actions.edit.extend_word_left,
    ("selection", "wordRight"): actions.edit.extend_word_right,
    ("selection", "left"): actions.edit.extend_left,
    ("selection", "right"): actions.edit.extend_right,
    ("selection", "word"): actions.edit.extend_word_right,
    # Go before
    ("goBefore", "line"): actions.edit.line_start,
    ("goBefore", "paragraph"): actions.edit.paragraph_start,
    ("goBefore", "document"): actions.edit.file_start,
    ("goBefore", "fileStart"): actions.edit.file_start,
    ("goBefore", "selection"): actions.edit.left,
    ("goBefore", "wordLeft"): actions.edit.word_left,
    ("goBefore", "word"): actions.edit.word_left,
    # Go after
    ("goAfter", "line"): actions.edit.line_end,
    ("goAfter", "paragraph"): actions.edit.paragraph_end,
    ("goAfter", "document"): actions.edit.file_end,
    ("goAfter", "fileEnd"): actions.edit.file_end,
    ("goAfter", "selection"): actions.edit.right,
    ("goAfter", "wordRight"): actions.edit.word_right,
    ("goAfter", "word"): actions.edit.word_right,
    # Delete
    ("delete", "word"): actions.edit.delete_word,
    ("deleteLeft", "word"): actions.edit.delete_word,
    ("delete", "line"): actions.edit.delete_line,
    ("delete", "paragraph"): actions.edit.delete_paragraph,
    ("delete", "document"): actions.edit.delete_all,
    ("delete", "selection"): actions.edit.delete,
    # Cut to clipboard
    ("cutToClipboard", "line"): actions.user.cut_line,
    ("cutToClipboard", "selection"): actions.edit.cut,
    # copy
    ("copyToClipboard", "selection"): actions.edit.copy,
}


mod = Module()


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifier: Union[EditModifier, str], count: int):
        """Perform edit command"""
        if type(modifier) is not str:
            
            key = (action.type, modifier.type)    
            print(f"{action.type} {modifier.type}")
            if key in compound_actions:
                print("Found compound action")
                for i in range(1, count + 1):
                    compound_actions[key]()
                return
          
            run_modifier_callback(modifier, count)
            run_action_callback(action)
        else:
            for i in range(1, count + 1):
                run_action_callback(action)
    
