### Actions ###
## Clipboard ##
cut that: edit.cut()
copy that: edit.copy()
grab that:
    mouse_click()
    mouse_click()
    edit.copy()
drop that:
    mouse_click()
    mouse_click()
    edit.paste()

spark: edit.paste()
paste that: edit.paste()
(spark | paste) match: edit.paste_match_style()
(spark | paste) all: user.paste_all()
(spark | paste) line: user.paste_line()
(spark | paste) line start: user.paste_line_start()
(spark | paste) line end: user.paste_line_end()
(spark | paste) word: user.paste_word()

## Search ##
find that: edit.find()
find next: edit.find_next()
## Misc ##
rewind: edit.undo()
replay: edit.redo()
disk: edit.save()
disk as: edit.save_all()
file print: edit.print()
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
zoom reset: edit.zoom_reset()

### Edit ###
scratch: edit.delete()
line delete: edit.delete_line()
# word delete:
#     edit.delete_word()
whack: user.delete_word_left()
bump: user.delete_word_right()
move in: edit.indent_more()
move out: edit.indent_less()
slap: key(enter)
line up: edit.line_insert_up()
line down: edit.line_insert_down()
swap up: edit.line_swap_up()
swap down: edit.line_swap_down()

### Navigation ###
sauce: edit.up()
dunce: edit.down()
lease: edit.left()
ross: edit.right()
pinch: edit.page_up()
punch: edit.page_down()
struck out: edit.file_end()
strike out: edit.file_start()
role: edit.word_right()
lord: edit.word_left()
strike: edit.line_start()
struck: edit.line_end()

### Selection ###
take none: edit.select_none()
take all: edit.select_all()
take up: edit.extend_up()
take down: edit.extend_down()
take ross: edit.extend_right()
take lease: edit.extend_left()
take start: edit.extend_file_start()
take end: edit.extend_file_end()
take line: edit.select_line()
take strike: edit.extend_line_start()
take struck: edit.extend_line_end()
take word: edit.select_word()
take lord: edit.extend_word_left()
take role: edit.extend_word_right()

# Duplication
clone that: edit.selection_clone()
clone line: edit.line_clone()

# Insert new line
new line above: edit.line_insert_up()
new line below: edit.line_insert_down()

# Insert padding with optional symbols
(pad | padding): user.insert_between(" ", " ")
(pad | padding) <user.symbol_key>+:
    insert(" ")
    user.insert_many(symbol_key_list)
    insert(" ")

# Undo/redo
undo that: edit.undo()
redo that: edit.redo()

# Save
file save: edit.save()
file save all: edit.save_all()
