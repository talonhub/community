app: joplin
-

# Enable Talon community action implementations
tag(): user.tabs
tag(): user.line_commands
tag(): user.find_and_replace
tag(): user.command_search
tag(): user.navigation
tag(): user.splits
tag(): user.code_comment_line

# Joplin layout and panel toggles
bar switch: user.joplin("toggleSideBar")
notes switch: user.joplin("toggleNoteList")
layout reset: user.joplin("resetLayout")
menu bar switch: user.joplin("toggleMenuBar")
# Activates the mode for resizing and moving bars/panes
layout move toggle: user.joplin("toggleLayoutMoveMode")
# Switch between md viewer and rich text editor
view toggle: user.joplin("toggleEditors")
# Switch between markdown viewer editor and combined
layout toggle: user.joplin("toggleVisiblePanes")

# Focus navigation
side focus: user.joplin("focusElementSideBar")
notes focus: user.joplin("focusElementNoteList")
title focus: user.joplin("focusElementNoteTitle")
editor focus: user.joplin("focusElementNoteBody")
viewer focus: user.joplin("focusElementNoteViewer")
search focus: user.joplin("focusSearch")

# Note and file search
file hunt:
    # Open the command pallette then delete the : to make it a file search
    key("ctrl-shift-p")
    key("backspace")
    # For some strange reason, just this command doesn't work (no errors or feedback).
    user.joplin("gotoAnything")
file hunt [<user.text>]:
    key("ctrl-shift-p")
    key("backspace")
    sleep(50ms)
    insert(user.text or "")

# Note lifecycle and folder management
note next:
    user.joplin("focusElementNoteList")
    key("down")
    user.joplin("focusElementNoteBody")
note previous:
    user.joplin("focusElementNoteList")
    key("up")
    user.joplin("focusElementNoteBody")
note new: user.joplin("newNote")
todo new: user.joplin("newTodo")
folder new: user.joplin("newFolder")
sub folder new: user.joplin("newSubFolder")
note delete: user.joplin("deleteNote")
folder delete: user.joplin("deleteFolder")
trash empty: user.joplin("emptyTrash")
note duplicate: user.joplin("duplicateNote")
note move: user.joplin("moveToFolder")
note link: user.joplin("linkToNote")
note type switch: user.joplin("toggleNoteType")
sort lines: user.joplin("editor.sortSelectedLines")

# Markdown formatting and insertions
bold: user.joplin("textBold")
italic: user.joplin("textItalic")
code: user.joplin("textCode")
heading: user.joplin("textHeading")
rule insert: user.joplin("textHorizontalRule")
link insert: user.joplin("textLink")
bullet: user.joplin("textBulletedList")
number list: user.joplin("textNumberedList")
checkbox: user.joplin("textCheckbox")
time insert: user.joplin("insertDateTime")
file attach: user.joplin("attachFile")

# Document metadata and synchronization
synchronize: user.joplin("synchronize")
alarm set: user.joplin("editAlarm")
show properties: user.joplin("showNoteProperties")
show stats: user.joplin("showNoteContentProperties")
export pdf: user.joplin("exportPdf")
external edit: user.joplin("startExternalEditing")
backup create: user.joplin("CreateBackup")
tag open: user.joplin("openTag")
tag set: user.joplin("setTags")
tag rename: user.joplin("renameTag")
