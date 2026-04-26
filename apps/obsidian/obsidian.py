import re
import subprocess

from talon import Context, Module, actions, settings

lang_ctx = Context()
lang_ctx.matches = r"""
app: obsidian
not tag: user.code_language_forced
"""


@lang_ctx.action_class("code")
class CodeActions:
    def language():
        return "markdown"


ctx = Context()
ctx.matches = r"""
app: obsidian
"""

mod = Module()
# Expand app detection similar to VSCode to support all OS variants
mod.apps.obsidian = """
os: linux
and app.name: Obsidian
"""
mod.apps.obsidian = """
os: mac
and app.bundle: md.obsidian
"""
mod.apps.obsidian = r"""
os: windows
and app.exe: /^obsidian\.exe$/i
os: windows
app.name: obsidian
"""

mac_ctx = Context()
mac_ctx.matches = r"""
os: mac
app: obsidian
"""

mod.setting(
    "obsidian_use_cli",
    type=bool,
    default=False,
    desc="""Whether to use the Obsidian CLI instead of palette to send Obsidian commands. Palette (false) will work out of the box but requires the language to be set to English and is slower. CLI (true) requires command line interface to be enabled in the Obsidian general options, and requires Obsidian to be on the PATH""",
)

obsidian_command_names = {
    "app:delete-file": "Delete current file",
    "app:go-back": "Navigate back",
    "app:go-forward": "Navigate forward",
    "app:open-another-vault": "Open vault...",
    "app:open-help": "Open help",
    "app:open-sandbox-vault": "Open sandbox vault",
    "app:open-settings": "Open settings",
    "app:open-vault": "Manage vaults",
    "app:reload": "Reload app without saving",
    "app:show-debug-info": "Show debug info",
    "app:show-release-notes": "Show release notes",
    "app:switch-vault": "Change vault...",
    "app:toggle-default-new-pane-mode": "Toggle default mode for new tabs",
    "app:toggle-left-sidebar": "Toggle left sidebar",
    "app:toggle-ribbon": "Toggle ribbon",
    "app:toggle-right-sidebar": "Toggle right sidebar",
    "backlink:open": "Backlinks: Show backlinks",
    "backlink:open-backlinks": "Backlinks: Open backlinks for the current note",
    "backlink:toggle-backlinks-in-document": "Backlinks: Toggle backlinks in document",
    "bases:add-item": "Bases: Add item",
    "bases:add-view": "Bases: Add view",
    "bases:change-view": "Bases: Change view",
    "bases:copy-table": "Bases: Copy table to clipboard",
    "bases:insert": "Bases: Insert new base",
    "bases:new-file": "Bases: Create new base",
    "bookmarks:bookmark-all-tabs": "Bookmarks: Bookmark all tabs...",
    "bookmarks:bookmark-current-heading": "Bookmarks: Bookmark heading under cursor...",
    "bookmarks:bookmark-current-search": "Bookmarks: Bookmark current search...",
    "bookmarks:bookmark-current-section": "Bookmarks: Bookmark block under cursor...",
    "bookmarks:bookmark-current-view": "Bookmarks: Bookmark...",
    "bookmarks:open": "Bookmarks: Show bookmarks",
    "bookmarks:unbookmark-current-view": "Bookmarks: Remove bookmark for the current file",
    "canvas:convert-to-file": "Canvas: Convert to file...",
    "canvas:export-as-image": "Canvas: Export as image",
    "canvas:jump-to-group": "Canvas: Jump to group",
    "canvas:new-file": "Canvas: Create new canvas",
    "command-palette:open": "Command palette: Open command palette",
    "daily-notes": "Daily notes: Open today's daily note",
    "daily-notes:goto-next": "Daily notes: Open next daily note",
    "daily-notes:goto-prev": "Daily notes: Open previous daily note",
    "dataview:dataview-drop-cache": "Dataview: Drop all cached file metadata",
    "dataview:dataview-force-refresh-views": "Dataview: Force refresh all views and blocks",
    "dataview:dataview-rebuild-current-view": "Dataview: Rebuild current view",
    "editor:add-cursor-above": "Add cursor above",
    "editor:add-cursor-below": "Add cursor below",
    "editor:attach-file": "Insert attachment",
    "editor:clear-formatting": "Clear formatting",
    "editor:context-menu": "Show context menu under cursor",
    "editor:cycle-list-checklist": "Cycle bullet/checkbox",
    "editor:delete-paragraph": "Delete paragraph",
    "editor:download-attachments": "Download attachments for current file",
    "editor:focus": "Focus on last note",
    "editor:focus-bottom": "Focus on tab group below",
    "editor:focus-left": "Focus on tab group to the left",
    "editor:focus-right": "Focus on tab group to the right",
    "editor:focus-top": "Focus on tab group above",
    "editor:fold-all": "Fold all headings and lists",
    "editor:fold-less": "Fold less",
    "editor:fold-more": "Fold more",
    "editor:follow-link": "Follow link under cursor",
    "editor:indent-list": "Indent list item",
    "editor:insert-callout": "Insert callout",
    "editor:insert-codeblock": "Insert code block",
    "editor:insert-embed": "Add embed",
    "editor:insert-footnote": "Insert footnote",
    "editor:insert-horizontal-rule": "Insert horizontal rule",
    "editor:insert-link": "Insert Markdown link",
    "editor:insert-mathblock": "Insert maths block",
    "editor:insert-table": "Insert table",
    "editor:insert-tag": "Add tag",
    "editor:insert-wikilink": "Add internal link",
    "editor:open-link-in-new-leaf": "Open link under cursor in new tab",
    "editor:open-link-in-new-split": "Open link under cursor to the right",
    "editor:open-link-in-new-window": "Open link under cursor in new window",
    "editor:open-search": "Search current file",
    "editor:open-search-replace": "Search & replace in current file",
    "editor:rename-heading": "Rename this heading...",
    "editor:save-file": "Save current file",
    "editor:set-heading": "Toggle heading",
    "editor:set-heading-0": "Remove heading",
    "editor:set-heading-1": "Set as heading 1",
    "editor:set-heading-2": "Set as heading 2",
    "editor:set-heading-3": "Set as heading 3",
    "editor:set-heading-4": "Set as heading 4",
    "editor:set-heading-5": "Set as heading 5",
    "editor:set-heading-6": "Set as heading 6",
    "editor:swap-line-down": "Move line down",
    "editor:swap-line-up": "Move line up",
    "editor:table-col-after": "Table: Add column after",
    "editor:table-col-align-center": "Table: Align centre",
    "editor:table-col-align-left": "Table: Align left",
    "editor:table-col-align-right": "Table: Align right",
    "editor:table-col-before": "Table: Add column before",
    "editor:table-col-copy": "Table: Duplicate column",
    "editor:table-col-delete": "Table: Delete column",
    "editor:table-col-left": "Table: Move column left",
    "editor:table-col-right": "Table: Move column right",
    "editor:table-row-after": "Table: Add row after",
    "editor:table-row-before": "Table: Add row before",
    "editor:table-row-copy": "Table: Duplicate row",
    "editor:table-row-delete": "Table: Delete row",
    "editor:table-row-down": "Table: Move row down",
    "editor:table-row-up": "Table: Move row up",
    "editor:toggle-blockquote": "Toggle blockquote",
    "editor:toggle-bold": "Toggle bold",
    "editor:toggle-bullet-list": "Toggle bullet list",
    "editor:toggle-checklist-status": "Toggle checkbox status",
    "editor:toggle-code": "Toggle code",
    "editor:toggle-comments": "Toggle comment",
    "editor:toggle-fold": "Toggle fold on the current line",
    "editor:toggle-fold-properties": "Toggle fold properties in current file",
    "editor:toggle-highlight": "Toggle highlight",
    "editor:toggle-inline-math": "Toggle inline maths",
    "editor:toggle-italics": "Toggle italic",
    "editor:toggle-line-numbers": "Toggle line numbers",
    "editor:toggle-numbered-list": "Toggle numbered list",
    "editor:toggle-readable-line-length": "Toggle readable line length",
    "editor:toggle-source": "Toggle Live Preview/Source mode",
    "editor:toggle-spellcheck": "Toggle spellcheck",
    "editor:toggle-strikethrough": "Toggle strikethrough",
    "editor:unfold-all": "Unfold all headings and lists",
    "editor:unindent-list": "Unindent list item",
    "file-explorer:duplicate-file": "Make a copy of the current file",
    "file-explorer:move-file": "Move current file to another folder",
    "file-explorer:new-file": "Create new note",
    "file-explorer:new-file-in-current-tab": "Create new note in current tab",
    "file-explorer:new-file-in-new-pane": "Create note to the right",
    "file-explorer:new-folder": "Files: Create new folder",
    "file-explorer:open": "Files: Show file explorer",
    "file-explorer:reveal-active-file": "Files: Reveal current file in navigation",
    "file-recovery:open": "File recovery: Open local history",
    "footnotes:open": "Footnotes view: Show footnotes",
    "global-search:open": "Search: Search in all files",
    "graph:animate": "Graph view: Start graph time-lapse animation",
    "graph:open": "Graph view: Open graph view",
    "graph:open-local": "Graph view: Open local graph",
    "insert-current-date": "Templates: Insert current date",
    "insert-current-time": "Templates: Insert current time",
    "insert-template": "Templates: Insert template",
    "markdown:add-alias": "Add alias",
    "markdown:add-metadata-property": "Add file property",
    "markdown:clear-metadata-properties": "Clear file properties",
    "markdown:toggle-preview": "Toggle reading view",
    "note-composer:extract-heading": "Note composer: Extract this heading...",
    "note-composer:merge-file": "Note composer: Merge current file with another file...",
    "note-composer:split-file": "Note composer: Extract current selection...",
    "open-with-default-app:open": "Open in default app",
    "open-with-default-app:show": "Show in system explorer",
    "outgoing-links:open": "Outgoing links: Show outgoing links",
    "outgoing-links:open-for-current": "Outgoing links: Open outgoing links for the current file",
    "outline:open": "Outline: Show outline",
    "outline:open-for-current": "Outline: Open outline of the current file",
    "switcher:open": "Quick switcher: Open quick switcher",
    "tag-pane:open": "Tags view: Show tags",
    "theme:switch": "Change theme...",
    "theme:toggle-light-dark": "Toggle light/dark mode",
    "window:reset-zoom": "Reset zoom",
    "window:toggle-always-on-top": "Toggle window always on top",
    "window:zoom-in": "Zoom in",
    "window:zoom-out": "Zoom out",
    "workspace:close": "Close current tab",
    "workspace:close-others": "Close all other tabs",
    "workspace:close-others-tab-group": "Close others in tab group",
    "workspace:close-tab-group": "Close this tab group",
    "workspace:close-window": "Close window",
    "workspace:copy-full-path": "Copy current file path from system root",
    "workspace:copy-path": "Copy current file path from vault folder",
    "workspace:copy-url": "Copy Obsidian URL for current file",
    "workspace:edit-file-title": "Rename file",
    "workspace:export-pdf": "Export to PDF...",
    "workspace:goto-last-tab": "Go to last tab",
    "workspace:goto-tab-1": "Go to tab #1",
    "workspace:goto-tab-2": "Go to tab #2",
    "workspace:goto-tab-3": "Go to tab #3",
    "workspace:goto-tab-4": "Go to tab #4",
    "workspace:goto-tab-5": "Go to tab #5",
    "workspace:goto-tab-6": "Go to tab #6",
    "workspace:goto-tab-7": "Go to tab #7",
    "workspace:goto-tab-8": "Go to tab #8",
    "workspace:move-to-new-window": "Move current tab to new window",
    "workspace:new-tab": "New tab",
    "workspace:new-window": "New window",
    "workspace:next-tab": "Go to next tab",
    "workspace:open-in-new-window": "Open current tab in new window",
    "workspace:previous-tab": "Go to previous tab",
    "workspace:show-trash": "Show trash",
    "workspace:split-horizontal": "Split down",
    "workspace:split-vertical": "Split right",
    "workspace:toggle-pin": "Toggle pin",
    "workspace:toggle-stacked-tabs": "Toggle stacked tabs",
    "workspace:undo-close-pane": "Undo close tab",
}


def obsidian_run_cli_command(command_id: str):
    try:
        result = subprocess.run(
            [
                "obsidian",
                "command",
                f"id={command_id}",
            ],
            timeout=1.0,
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        if result.stdout:
            parse_obsidian_errors(result.stdout, command_id)
    except OSError as e:
        actions.app.notify(
            f"""Error running Obsidian command via CLI. The obsidian command might not be on your PATH?
            Full error:
            {e}
            """
        )
        actions.app.notify(f"Falling back to palette command for {command_id}")
        obsidian_palette_command(command_id, fallback=True)
    except subprocess.CalledProcessError as e:
        # Note: As of at least obsidian version 1.12, the CLI never
        # emits a failure exit code, so this block won't trigger unless that changes.
        parse_obsidian_errors(e.output, command_id)


def parse_obsidian_errors(message, command_id):
    if "Command line interface is not enabled" in message:
        actions.app.notify(
            """Talon settings say to use the Obsidian CLI for Obsidian commands, but CLI interface control is disabled in Obsidian settings.
            Please turn it on in Settings > General > Advanced
            """
        )
        actions.app.notify(f"Falling back to palette command for {command_id}")
        obsidian_palette_command(command_id, fallback=True)
    elif re.match('Command "[^"]*"not found', message):
        actions.app.notify(
            f"Command '{command_id}' does not seem to be a valid Obsidian command."
        )


def command_uri_or_client_fallback(command_id: str):
    """If advanced-uri is supported, use it to invoke the command.
    Otherwise, fall back to the client"""

    if settings.get("user.obsidian_use_cli"):
        obsidian_run_cli_command(command_id)
    else:
        obsidian_palette_command(command_id)


def get_command_palette_name(command_id: str) -> str:
    try:
        return obsidian_command_names[command_id]
    except KeyError as ex:
        actions.app.notify(
            f"ERROR: Could not find Obsidian palette name for command_id {command_id}"
        )
        return ""


def obsidian_palette_command(command_id: str, fallback=False):
    if settings.get("user.obsidian_use_cli") and not fallback:
        obsidian_run_cli_command("command-palette:open")
    else:
        actions.user.command_palette_key()
    command = get_command_palette_name(command_id)
    if not command:
        return None
    actions.insert(command)
    actions.key("enter")


@mod.action_class
class Actions:
    def command_palette_key():
        """Show command palette"""
        actions.key("ctrl-p")


@mac_ctx.action_class("user")
class MacUserActions:
    def command_palette_key():
        actions.key("cmd-p")


@mod.action_class
class Actions:
    def obsidian(command_id: str):
        """Invoke an action by Obsidian command id"""
        command_uri_or_client_fallback(command_id)


@ctx.action_class("app")
class AppActions:
    # talon app actions
    def tab_open():
        actions.user.obsidian("workspace:new-tab")

    def tab_close():
        actions.user.obsidian("workspace:close")

    def tab_next():
        actions.user.obsidian("workspace:next-tab")

    def tab_previous():
        actions.user.obsidian("workspace:previous-tab")

    def tab_reopen():
        actions.user.obsidian("workspace:undo-close-pane")

    def window_close():
        actions.user.obsidian("workspace:close-window")


@ctx.action_class("user")
class UserActions:
    # command palette / command search
    def command_search(command: str = ""):
        actions.user.obsidian("command-palette:open")
        if command:
            actions.insert(command)

    def tab_jump(number: int):
        actions.user.obsidian(f"workspace:goto-tab-{number}")

    def tab_final():
        actions.user.obsidian("workspace:goto-last-tab")

    # splits support (basic)
    def split_window():
        actions.user.obsidian("workspace:split-vertical")

    def split_window_vertically():
        actions.user.obsidian("workspace:split-vertical")

    def split_window_horizontally():
        actions.user.obsidian("workspace:split-horizontal")

    def split_next():
        actions.user.obsidian("editor:focus-right")

    def split_last():
        actions.user.obsidian("editor:focus-left")

    def split_clear():
        actions.user.obsidian("workspace:close-tab-group")

    # multiple cursor support (limited)
    def multi_cursor_add_above():
        actions.user.obsidian("editor:add-cursor-above")

    def multi_cursor_add_below():
        actions.user.obsidian("editor:add-cursor-below")

    def multi_cursor_disable():
        actions.key("escape")

    # project-wide search
    def find_everywhere(text: str):
        actions.user.obsidian("global-search:open")
        if text:
            actions.insert(text)

    def replace(text: str):
        actions.user.obsidian("editor:open-search-replace")
        if text:
            actions.insert(text)

    # navigation
    def go_back():
        actions.user.obsidian("app:go-back")

    def go_forward():
        actions.user.obsidian("app:go-forward")


@ctx.action_class("edit")
class EditActions:
    # basic editor operations
    def save():
        actions.user.obsidian("editor:save-file")

    def find(text: str = None):
        actions.user.obsidian("editor:open-search")
        if text:
            actions.insert(text)

    def find_next():
        actions.key("escape")
        actions.edit.find()
        actions.key("enter")

    def find_previous():
        actions.key("escape")
        actions.edit.find()
        actions.key("shift-enter")

    def zoom_in():
        actions.user.obsidian("window:zoom-in")

    def zoom_out():
        actions.user.obsidian("window:zoom-out")

    def zoom_reset():
        actions.user.obsidian("window:reset-zoom")
