app: Obsidian
-

tag(): user.find_and_replace
tag(): user.multiple_cursors
tag(): user.splits
tag(): user.tabs
tag(): user.command_search
tag(): user.navigation

left side: user.obsidian("editor:focus-left")
right side: user.obsidian("editor:focus-right")
top side: user.obsidian("editor:focus-top")
bottom side: user.obsidian("editor:focus-bottom")

# reading/source toggle
view toggle: user.obsidian("markdown:toggle-preview")
bar switch: user.obsidian("app:toggle-left-sidebar")
panel switch: user.obsidian("app:toggle-right-sidebar")
ribbon switch: user.obsidian("app:toggle-ribbon")

# window and settings
window reload | reload it: user.obsidian("app:reload")
show settings: user.obsidian("app:open-settings")

# note operations
file hunt: user.obsidian("switcher:open")
file hunt [<user.text>]:
    user.obsidian("switcher:open")
    sleep(50ms)
    insert(user.text or "")
file hunt (pace | paste):
    user.obsidian("switcher:open")
    sleep(50ms)
    edit.paste()
note new | file create: user.obsidian("file-explorer:new-file")
note new here | file create here: user.obsidian("file-explorer:new-file-in-current-tab")
note new right | file create right: user.obsidian("file-explorer:new-file-in-new-pane")
folder new | file create folder: user.obsidian("file-explorer:new-folder")
note delete | file delete: user.obsidian("app:delete-file")
note rename | file rename: user.obsidian("workspace:edit-file-title")
note move: user.obsidian("file-explorer:move-file")
note duplicate | file clone: user.obsidian("file-explorer:duplicate-file")
note reveal | file reveal: user.obsidian("file-explorer:reveal-active-file")
file open folder: user.obsidian("open-with-default-app:show")
file open default app: user.obsidian("open-with-default-app:open")
file export pdf: user.obsidian("workspace:export-pdf")
file copy path: user.obsidian("workspace:copy-path")
file copy full path: user.obsidian("workspace:copy-full-path")
file copy url: user.obsidian("workspace:copy-url")

# daily notes
daily open: user.obsidian("daily-notes")
daily previous: user.obsidian("daily-notes:goto-prev")
daily next: user.obsidian("daily-notes:goto-next")

# links and navigation
follow: user.obsidian("editor:follow-link")
link open: user.obsidian("editor:open-link-in-new-leaf")
link split: user.obsidian("editor:open-link-in-new-split")

tab pin: user.obsidian("workspace:toggle-pin")
close other tabs: user.obsidian("workspace:close-others")
close tabs group: user.obsidian("workspace:close-tab-group")

# outline and backlinks
outline open: user.obsidian("outline:open-for-current")
backlinks open: user.obsidian("backlink:open-backlinks")
bar files: user.obsidian("file-explorer:open")
bar backlinks: user.obsidian("backlink:open")
bar tags: user.obsidian("tag-pane:open")
bar graph: user.obsidian("graph:open")
bar local graph: user.obsidian("graph:open-local")

# find and replace helpers (phrase-capable)
search here [<user.text>]:
    user.obsidian("editor:open-search")
    sleep(50ms)
    insert(user.text or "")
search all [<user.text>]:
    user.obsidian("global-search:open")
    sleep(50ms)
    insert(user.text or "")
replace here [<user.text>]:
    user.obsidian("editor:open-search-replace")
    sleep(50ms)
    insert(user.text or "")

# formatting and lists
bold: user.obsidian("editor:toggle-bold")
italic: user.obsidian("editor:toggle-italics")
code: user.obsidian("editor:toggle-code")
blockquote: user.obsidian("editor:toggle-blockquote")
bullet: user.obsidian("editor:toggle-bullet-list")
list number: user.obsidian("editor:toggle-numbered-list")
checkbox: user.obsidian("editor:toggle-checklist-status")
line numbers: user.obsidian("editor:toggle-line-numbers")
readable length: user.obsidian("editor:toggle-readable-line-length")
spellcheck: user.obsidian("editor:toggle-spellcheck")

# folding and movement
fold all: user.obsidian("editor:fold-all")
unfold all: user.obsidian("editor:unfold-all")
fold more: user.obsidian("editor:fold-more")
fold less: user.obsidian("editor:fold-less")
fold toggle: user.obsidian("editor:toggle-fold")
fold properties toggle: user.obsidian("editor:toggle-fold-properties")
line move up: user.obsidian("editor:swap-line-up")
line move down: user.obsidian("editor:swap-line-down")

# display and theme
theme switch: user.obsidian("theme:switch")
theme toggle: user.obsidian("theme:toggle-light-dark")
