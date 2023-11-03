altar: key(alt)
#mouse: user.mouse_toggle_control_mouse()

add signature:
	insert("--\nEduard Ansaldo Gine, PhD.\nResearch Fellow\nMetaorganism Immunity Section, Laboratory of Host Immunity and Microbiome\nNational Institute of Allergy and Infectious Diseases\nNational Institutes of Health\nBuilding 4, Room 241\n4 Memorial Drive\nBethesda, MD 20892")

kay: key(enter)

drill: key(delete) 

slapper: 

exit: app.window_close()


down: key(down)
up: key(up)
left: key(left)
right: key(right)
numb <number>: insert("{number}")

parens:
    insert("()")
    key(left)
spam: ", "
stack: ":"
 
nope: edit.undo()

restart talon: user.talon_relaunch()

right click: key(shift-f10)
  
work email: insert("eduard.ansaldogine@nih.gov")

personal email: insert("eduardansaldogine@gmail.com")

Berkeley email: insert("eduard.ansaldo@berkeley.edu")

(file | explore): key(super-e)
(windows): key(super)

dasher: insert(" - ")

over: skip()


^talon restart confirm$: user.talon_restart()
^talon quit confirm$: user.talon_quit()

spin:
    key(right)
    ", "
    user.insert_between("'", "'")

# Formatting
formatted <user.format_text>: user.dictation_insert_raw(format_text)
^format selection <user.formatters>$: user.formatters_reformat_selection(formatters)