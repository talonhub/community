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
panes switch: user.joplin("toggleVisiblePanes")
view toggle: user.joplin("toggleEditors")
layout move toggle: user.joplin("toggleLayoutMoveMode")
layout reset: user.joplin("resetLayout")
menu bar switch: user.joplin("toggleMenuBar")

# Focus navigation
focus side: user.joplin("focusElementSideBar")
focus notes: user.joplin("focusElementNoteList")
focus title: user.joplin("focusElementNoteTitle")
focus editor: user.joplin("focusElementNoteBody")
focus viewer: user.joplin("focusElementNoteViewer")
focus search: user.joplin("focusSearch")

# Note and file search
file hunt: user.joplin("gotoAnything")
file hunt [<user.text>]:
    user.joplin("gotoAnything")
    sleep(50ms)
    insert(user.text or "")

# Note lifecycle and folder management
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
sync now: user.joplin("synchronize")
tag set: user.joplin("setTags")
alarm set: user.joplin("editAlarm")
show properties: user.joplin("showNoteProperties")
show stats: user.joplin("showNoteContentProperties")
export pdf: user.joplin("exportPdf")
external edit: user.joplin("startExternalEditing")
backup create: user.joplin("CreateBackup")
