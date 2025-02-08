from talon import Module, actions, settings

from .edit_command_actions import EditAction, run_action_callback
from .edit_command_modifiers import EditModifier, run_modifier_callback

mod = Module()

# providing some settings for customizing the word and line selection delay
# talon can execute selections must faster than a human
# resulting in unexpected or inconsistent results in applications such as visual studio code
mod.setting(
    "edit_command_word_selection_delay",
    type=int,
    default=75,
    desc="Sleep required between word selections",
)

mod.setting(
    "edit_command_line_selection_delay",
    type=int,
    default=75,
    desc="Sleep required between line selections",
)


def before_line_up():
    actions.edit.up()
    actions.edit.line_start()


def after_line_up():
    actions.edit.up()
    actions.edit.line_end()


def before_line_down():
    actions.edit.down()
    actions.edit.line_start()


def after_line_down():
    actions.edit.down()
    actions.edit.line_end()


def select_lines(action, direction, count):
    if direction == "lineUp":
        selection_callback = actions.edit.extend_line_up
        extend_line_callback = actions.edit.extend_line_start
    else:
        selection_callback = actions.edit.extend_line_down
        extend_line_callback = actions.edit.extend_line_end

    selection_delay = f"{settings.get('user.edit_command_line_selection_delay')}ms"

    for i in range(1, count + 1):
        selection_callback()
        actions.sleep(selection_delay)

    # ensure we take the start/end of the line too!
    extend_line_callback()
    actions.sleep(selection_delay)
    run_action_callback(action)


def select_words(action, direction, count):
    if direction == "wordLeft":
        selection_callback = actions.edit.extend_word_left
    else:
        selection_callback = actions.edit.extend_word_right

    selection_delay = f"{settings.get('user.edit_command_word_selection_delay')}ms"
    for i in range(1, count + 1):
        selection_callback()
        actions.sleep(selection_delay)

    run_action_callback(action)


def word_movement_handler(action, direction, count):
    if direction == "wordLeft":
        movement_callback = actions.edit.word_left
    else:
        movement_callback = actions.edit.word_right

    selection_delay = f"{settings.get('user.edit_command_word_selection_delay')}ms"
    for i in range(1, count + 1):
        movement_callback()
        actions.sleep(selection_delay)


# in some cases, it is necessary to have some custom handling for timing reasons
custom_callbacks = {
    ("goAfter", "wordLeft"): word_movement_handler,
    ("goAfter", "wordRight"): word_movement_handler,
    ("goBefore", "wordLeft"): word_movement_handler,
    ("goBefore", "wordRight"): word_movement_handler,
    # delete
    ("delete", "word"): select_words,
    ("delete", "wordLeft"): select_words,
    ("delete", "wordRight"): select_words,
    ("delete", "lineUp"): select_lines,
    ("delete", "lineDown"): select_lines,
    # cut
    ("cutToClipboard", "word"): select_words,
    ("cutToClipboard", "wordLeft"): select_words,
    ("cutToClipboard", "wordRight"): select_words,
    ("cutToClipboard", "lineUp"): select_lines,
    ("cutToClipboard", "lineDown"): select_lines,
    # copy
    ("copyToClipboard", "word"): select_words,
    ("copyToClipboard", "wordLeft"): select_words,
    ("copyToClipboard", "wordRight"): select_words,
    ("copyToClipboard", "lineUp"): select_lines,
    ("copyToClipboard", "lineDown"): select_lines,
    # select
    ("select", "lineUp"): select_lines,
    ("select", "lineDown"): select_lines,
}

# In other cases there already is a "compound" talon action for a given action and modifier
compound_actions = {
    # select
    ("select", "wordLeft"): actions.edit.extend_word_left,
    ("select", "wordRight"): actions.edit.extend_word_right,
    ("select", "left"): actions.edit.extend_left,
    ("select", "right"): actions.edit.extend_right,
    ("select", "word"): actions.edit.extend_word_right,
    # Go before
    ("goBefore", "line"): actions.edit.line_start,
    ("goBefore", "lineUp"): before_line_up,
    ("goBefore", "lineDown"): before_line_down,
    ("goBefore", "paragraph"): actions.edit.paragraph_start,
    ("goBefore", "document"): actions.edit.file_start,
    ("goBefore", "fileStart"): actions.edit.file_start,
    ("goBefore", "selection"): actions.edit.left,
    ("goBefore", "wordLeft"): actions.edit.word_left,
    ("goBefore", "word"): actions.edit.word_left,
    # Go after
    ("goAfter", "line"): actions.edit.line_end,
    ("goAfter", "lineUp"): after_line_up,
    ("goAfter", "lineDown"): after_line_down,
    ("goAfter", "paragraph"): actions.edit.paragraph_end,
    ("goAfter", "document"): actions.edit.file_end,
    ("goAfter", "fileEnd"): actions.edit.file_end,
    ("goAfter", "selection"): actions.edit.right,
    ("goAfter", "wordRight"): actions.edit.word_right,
    ("goAfter", "wordLeft"): actions.edit.word_left,
    ("goAfter", "word"): actions.edit.word_right,
    # Delete
    ("delete", "left"): actions.edit.delete,
    ("delete", "right"): actions.user.delete_right,
    ("delete", "line"): actions.edit.delete_line,
    ("delete", "paragraph"): actions.edit.delete_paragraph,
    # ("delete", "document"): actions.edit.delete_all, # Beta only
    ("delete", "document"): actions.user.delete_all,
    ("delete", "selection"): actions.edit.delete,
    # Cut to clipboard
    ("cutToClipboard", "line"): actions.user.cut_line,
    ("cutToClipboard", "selection"): actions.edit.cut,
    # copy
    ("copyToClipboard", "selection"): actions.edit.copy,
}


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifier: EditModifier):
        """Perform edit command"""
        key = (action.type, modifier.type)
        count = modifier.count

        if key in custom_callbacks:
            custom_callbacks[key](action, modifier.type, count)
            return

        elif key in compound_actions:
            for i in range(1, count + 1):
                compound_actions[key]()
            return

        run_modifier_callback(modifier)
        run_action_callback(action)
