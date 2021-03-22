os: windows
os: linux
-
action(edit.copy):
	key(ctrl-c)

action(edit.cut):
	key(ctrl-x)

action(edit.delete):
	key(backspace)

action(edit.delete_line):
	edit.select_line()
	edit.delete()

#action(edit.delete_paragraph):

#action(edit.delete_sentence):

action(edit.delete_word):
	edit.select_word()
	edit.delete()

action(edit.down):
	key(down)

#action(edit.extend_again):

#action(edit.extend_column):

action(edit.extend_down):
	key(shift-down)

action(edit.extend_file_end):
	key(shift-ctrl-end)

action(edit.extend_file_start):
	key(shift-ctrl-home)

action(edit.extend_left):
	key(shift-left)

#action(edit.extend_line):

action(edit.extend_line_down):
	key(shift-down)

action(edit.extend_line_end):
	key(shift-end)

action(edit.extend_line_start):
	key(shift-home)

action(edit.extend_line_up):
	key(shift-up)

action(edit.extend_page_down):
	key(shift-pagedown)

action(edit.extend_page_up):
	key(shift-pageup)

#action(edit.extend_paragraph_end):
#action(edit.extend_paragraph_next()):
#action(edit.extend_paragraph_previous()):
#action(edit.extend_paragraph_start()):

action(edit.extend_right):
	key(shift-right)

#action(edit.extend_sentence_end):
#action(edit.extend_sentence_next):
#action(edit.extend_sentence_previous):
#action(edit.extend_sentence_start):

action(edit.extend_up):
	key(shift-up)

action(edit.extend_word_left):
	key(ctrl-shift-left)

action(edit.extend_word_right):
	key(ctrl-shift-right)

action(edit.file_end):
	key(ctrl-end)

action(edit.file_start):
	key(ctrl-home)

action(edit.find):
	key(ctrl-f)
	actions.insert(text)

action(edit.find_next):
	key(f3)
#action(edit.find_previous):

action(edit.indent_less):
	key(home delete)

action(edit.indent_more):
	key(home tab)

#action(edit.jump_column(n: int)
#action(edit.jump_line(n: int)

action(edit.left):
	key(left)

action(edit.line_down):
	key(down home)

action(edit.line_end):
	key(end)

action(edit.line_insert_down):
	key(end enter)

action(edit.line_insert_up):
	key(home enter up)

action(edit.line_start):
	key(home)

action(edit.line_up):
	key(up home)

#action(edit.move_again):

action(edit.page_down):
	key(pagedown)

action(edit.page_up):
	key(pageup)

#action(edit.paragraph_end):
#action(edit.paragraph_next):
#action(edit.paragraph_previous):
#action(edit.paragraph_start):

action(edit.paste):
	key(ctrl-v)

#action(paste_match_style):

action(edit.print):
	key(ctrl-p)

action(edit.redo):
	key(ctrl-y)

action(edit.right):
	key(right)

action(edit.save):
	key(ctrl-s)

action(edit.save_all):
	key(ctrl-shift-s)

action(edit.select_all):
	key(ctrl-a)

action(edit.select_line):
	key(end shift-home)

#action(edit.select_lines(a: int, b: int)):

action(edit.select_none):
	key(right)

#action(edit.select_paragraph):
#action(edit.select_sentence):

action(edit.select_word):
	key(ctrl-left ctrl-shift-right)

#action(edit.selected_text): -> str
#action(edit.sentence_end):
#action(edit.sentence_next):
#action(edit.sentence_previous):
#action(edit.sentence_start):

action(edit.undo):
	key(ctrl-z)

action(edit.up):
	key(up)

action(edit.word_left):
	key(ctrl-left)

action(edit.word_right):
	key(ctrl-right)

action(edit.zoom_in):
	key(ctrl-+)

action(edit.zoom_out):
	key(ctrl--)

action(edit.zoom_reset):
	key(ctrl-0)
