## (2021-03-09) This syntax is experimental and may change. See below for an explanation.
## If you are having issues with this module not working in vscode try adding the vscode setting "editor.emptySelectionClipboard": false
navigate [{user.arrow_key}] [{user.navigation_action}] [{user.navigation_target_name}] [{user.before_or_after}] [<user.ordinals>] <user.navigation_target>:
    ## If you use this command a lot, you may wish to have a shorter syntax that omits the navigate keyword. Note that you then at least have to say either a navigation_action or before_or_after:
    #({user.navigation_action} [{user.arrow_key}] [{user.navigation_target_name}] [{user.before_or_after}] | [{user.arrow_key}] {user.before_or_after}) [<user.ordinals>] <user.navigation_target>:
    user.navigation(navigation_action or "GO", arrow_key or "RIGHT", navigation_target_name or "DEFAULT", before_or_after or "DEFAULT", navigation_target, ordinals or 1)

# ===== Examples of use =====
#
#   navigate comma: moves after the next "," on the line.
#   navigate before five: moves before the next "5" on the line.
#   navigate left underscore: moves before the previous "_" on the line.
#   navigate left after second plex: moves after the second-previous "x" on the line.
#
# Besides characters, we can find phrases or move in predetermined units:
#
#   navigate phrase hello world: moves after the next "hello world" on the line.
#   navigate left third word: moves left over three words.
#   navigate before second big: moves before the second-next 'big' word (a chunk of anything except white space).
#   navigate left second small: moves left over two 'small' words (chunks of a camelCase name).
#
# We can search several lines (default 10) above or below the cursor:
#
#   navigate up phrase john: moves before the previous "john" (case-insensitive) on the preceding lines.
#   navigate down third period: moves after the third period on the following lines.
#
# Besides movement, we can cut, copy, select, clear (delete), or extend the current selection:
#
#   navigate cut after comma: cut the word following the next comma on the line.
#   navigate left copy third word: copy the third word to the left.
#   navigate extend third big: extend the selection three big words right.
#   navigate down clear phrase I think: delete the next occurrence of "I think" on the following lines.
#   navigate up select colon: select the closest colon on the preceeding lines.
#
# We can specify what gets selected before or after the given input:
#
#    navigate select parens after equals: Select the first "(" and everything until the first ")" after the "="
#    navigate left copy all before equals: Copy everything from the start of the line until the first "=" you encounter while moving left
#    navigate clear constant before semicolon: Delete the last word consisting of only uppercase characters or underscores before a ";"
#
# ===== Explanation of the grammar =====
#
# [{user.arrow_key}]: left, right, up, down (default: right)
#   Which direction to navigate in.
#   left/right work on the current line.
#   up/down work on the closest lines (default: 10) above or below.
#
# [{user.navigation_action}]: move, extend, select, clear, cut, copy (default: move)
#   What action to perform.
#
# [{user.navigation_target_name}]: word, small, big, parens, squares, braces, quotes, angles, all, method, constant (default: word)
#    The predetermined unit to select if before_or_after was specified.
#    Defaults to "word"
#
# [{user.before_or_after}]: before, after (default: special behavior)
#   For move/extend: where to leave the cursor, before or after the target.
#   Defaults to "after" for right/down and "before" for left/up.
#
#   For select/copy/cut: if absent, select/copy/cut the target iself. If
#   present, the navigation_target_name before/after the target.
#
# [<user.ordinals>]: an english ordinal, like "second" (default: first)
#   Which occurrence of the target to navigate to.
#
# <user.navigation_target>: one of the following:
#   - a character name, like "comma" or "five".
#   - "word" or "big" or "small"
#   - "phrase <some text to search for>"
#   Specifies the target to search for/navigate to.

# The functionality for all these commands is covered in the lines above, but these commands are kept here for convenience. Originally from word_selection.talon.
word neck [<number_small>]:
    user.navigation_by_name("SELECT", "RIGHT", "DEFAULT", "word", number_small or 1)
word pre [<number_small>]:
    user.navigation_by_name("SELECT", "LEFT", "DEFAULT", "word", number_small or 1)
small word neck [<number_small>]:
    user.navigation_by_name("SELECT", "RIGHT", "DEFAULT", "small", number_small or 1)
small word pre [<number_small>]:
    user.navigation_by_name("SELECT", "LEFT", "DEFAULT", "small", number_small or 1)
big word neck [<number_small>]:
    user.navigation_by_name("SELECT", "RIGHT", "DEFAULT", "big", number_small or 1)
big word pre [<number_small>]:
    user.navigation_by_name("SELECT", "LEFT", "DEFAULT", "big", number_small or 1)
