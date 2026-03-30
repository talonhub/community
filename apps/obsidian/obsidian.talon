app: Obsidian
-
tag(): user.find_and_replace
tag(): user.multiple_cursors
tag(): user.splits
tag(): user.tabs
tag(): user.command_search

left side: user.obsidian('editor:focus-left')
right side: user.obsidian('editor:focus-right')

# reading/source toggle
view toggle: user.obsidian('markdown:toggle-preview')
bar switch: user.obsidian('app:toggle-left-sidebar')
panel switch: user.obsidian('app:toggle-right-sidebar')
ribbon switch: user.obsidian('app:toggle-ribbon')

# note operations
file hunt: user.obsidian('switcher:open')
note new | file create: user.obsidian('file-explorer:new-file')
note delete | file delete: user.obsidian('app:delete-file')
note rename | file rename: user.obsidian('workspace:edit-file-title')
note move: user.obsidian('file-explorer:move-file')
note duplicate | file clone: user.obsidian('file-explorer:duplicate-file')
note reveal | file reveal: user.obsidian('file-explorer:reveal-active-file')

# daily notes
note daily: user.obsidian('daily-notes')
note daily previous: user.obsidian('daily-notes:goto-prev')
note daily next: user.obsidian('daily-notes:goto-next')

# links and navigation
link follow | follow this: user.obsidian('editor:follow-link')
link open: user.obsidian('editor:open-link-in-new-leaf')
link split: user.obsidian('editor:open-link-in-new-split')

tab pin: user.obsidian('workspace:toggle-pin')

# outline and backlinks
outline open: user.obsidian('outline:open-for-current')
backlinks open: user.obsidian('backlink:open-backlinks')

# formatting and lists
bold toggle: user.obsidian('editor:toggle-bold')
italic toggle: user.obsidian('editor:toggle-italics')
code toggle: user.obsidian('editor:toggle-code')
blockquote toggle: user.obsidian('editor:toggle-blockquote')
list bullet toggle: user.obsidian('editor:toggle-bullet-list')
list number toggle: user.obsidian('editor:toggle-numbered-list')
checkbox toggle: user.obsidian('editor:toggle-checklist-status')

# headings
heading one: user.obsidian('editor:set-heading-1')
heading two: user.obsidian('editor:set-heading-2')
heading three: user.obsidian('editor:set-heading-3')
heading four: user.obsidian('editor:set-heading-4')
heading five: user.obsidian('editor:set-heading-5')
heading six: user.obsidian('editor:set-heading-6')
heading remove: user.obsidian('editor:set-heading-0')
