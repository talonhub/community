from talon import Context, Module, actions, app

from ...core.command_client.command_client import run_command
from ...core.command_client.rpc_client.types import NoFileServerException

is_mac = app.platform == "mac"

mod = Module()

# Operating system matching declarations
mod.apps.joplin = """
os: linux
and app.name: Joplin
os: linux
and app.name: @joplinapp-desktop
"""
mod.apps.joplin = """
os: mac
and app.bundle: net.cozic.joplin-desktop
"""
mod.apps.joplin = r"""
os: windows
and app.exe: /^joplin\.exe$/i
os: windows
app.name: Joplin
"""

# Language mode configuration
lang_ctx = Context()
lang_ctx.matches = r"""
app: joplin
not tag: user.code_language_forced
"""


@lang_ctx.action_class("code")
class CodeActions:
    def language():
        return "markdown"

    def toggle_comment():
        actions.user.joplin("editor.toggleComment")


ctx = Context()
ctx.matches = r"""
app: joplin
"""

mac_ctx = Context()
mac_ctx.matches = r"""
os: mac
app: joplin
"""


# Command table populated via this DevTools extraction script; run via devtools console under help -> devtools
# (function extractJoplinCommandRegistry(){let CommandService;for(const modPath in require.cache){if(modPath.includes('CommandService')){const modExports=require.cache[modPath].exports;CommandService=modExports.default||modExports.CommandService||modExports;if(CommandService&&typeof CommandService.instance==='function'){break}}}if(!CommandService||!CommandService.instance){console.error("Extraction Failed: Unable to locate CommandService in require.cache.");return}const serviceInstance=CommandService.instance();const commandStore=serviceInstance.commands_;const commandMap={};for(const cmdName in commandStore){if(Object.prototype.hasOwnProperty.call(commandStore,cmdName)){let resolvedLabel="";try{resolvedLabel=serviceInstance.label(cmdName)}catch(err){const decl=commandStore[cmdName].declaration;if(decl&&typeof decl.label==='function'){try{resolvedLabel=decl.label()}catch(_){}}else if(decl&&typeof decl.label==='string'){resolvedLabel=decl.label}}commandMap[cmdName]=resolvedLabel?resolvedLabel.trim():cmdName}}const dictLines=["joplin_command_names = {"];const sortedIds=Object.keys(commandMap).sort();for(const id of sortedIds){dictLines.push(`    ${JSON.stringify(id)}: ${JSON.stringify(commandMap[id])},`)}dictLines.push("}");const pythonOutput=dictLines.join("\n");const tableLines=["| Command ID | Palette Label |","| :--- | :--- |"];for(const id of sortedIds){const escapedLabel=commandMap[id].replace(/\|/g,"\\|");tableLines.append?tableLines.append(`| \`${ id }\` | ${ escapedLabel } |`):tableLines.push(`| \`${ id }\` | ${ escapedLabel } |`)}const markdownOutput=tableLines.join("\n");console.log(pythonOutput);console.log("\nMarkdown Table Output:\n"+markdownOutput);try{const{clipboard}=require('electron');clipboard.writeText(pythonOutput);console.log(`%cExtraction Complete: ${sortedIds.length } commands exported and copied to clipboard.`,"color: #00dd00; font-weight: bold;")}catch(clipErr){console.warn("Clipboard access failed. Copy output manually from the console above.")}})();

joplin_command_names = {
    "CreateBackup": "Create backup",
    "addProfile": "Create new profile...",
    "attachFile": "Attach file",
    "commandPalette": "Command palette...",
    "copyDevCommand": "Copy dev mode command to clipboard",
    "deleteFolder": "Delete notebook",
    "deleteNote": "Delete note",
    "duplicateNote": "Duplicate",
    "editAlarm": "Set alarm",
    "editProfileConfig": "Edit profile configuration...",
    "editor.deleteLine": "Delete line",
    "editor.duplicateLine": "Duplicate line",
    "editor.execCommand": "editor.execCommand",
    "editor.focus": "editor.focus",
    "editor.indentLess": "Indent less",
    "editor.indentMore": "Indent more",
    "editor.redo": "Editor: Redo",
    "editor.scrollToText": "editor.scrollToText",
    "editor.setText": "editor.setText",
    "editor.sortSelectedLines": "Sort selected lines",
    "editor.swapLineDown": "Swap line down",
    "editor.swapLineUp": "Swap line up",
    "editor.toggleComment": "Toggle comment",
    "editor.undo": "Editor: Undo",
    "emptyTrash": "Empty trash",
    "exportDeletionLog": "Export deletion log",
    "exportFolders": "exportFolders",
    "exportNotes": "exportNotes",
    "exportPdf": "PDF - PDF File",
    "focusElement": "focusElement",
    "focusElementNoteBody": "Note body",
    "focusElementNoteList": "Note list",
    "focusElementNoteTitle": "Note title",
    "focusElementNoteViewer": "Note viewer",
    "focusElementSideBar": "Sidebar",
    "focusElementToolbar": "Toolbar",
    "focusSearch": "Search in all the notes",
    "gotoAnything": "Goto Anything...",
    "hideModalMessage": "hideModalMessage",
    "historyBackward": "Back",
    "historyForward": "Forward",
    "insertDateTime": "Insert time",
    "insertText": "insertText",
    "jop-freehand-drawing-jsdraw-plugin-deleteAutosave": "Delete all autosaved drawings",
    "jop-freehand-drawing-jsdraw-plugin-insertDrawing": "Insert Drawing",
    "jop-freehand-drawing-jsdraw-plugin-insertDrawing__newWindow": "Insert drawing in new window",
    "jop-freehand-drawing-jsdraw-plugin-restoreAutosave": "Restore from autosaved drawing",
    "leaveSharedFolder": "Leave notebook...",
    "linkToNote": "Link to note...",
    "moveToFolder": "Move to notebook",
    "newFolder": "New notebook",
    "newNote": "New note",
    "newSubFolder": "New sub-notebook",
    "newTodo": "New to-do",
    "openFolder": "openFolder",
    "openFolderDialog": "Edit",
    "openItem": "openItem",
    "openMasterPasswordDialog": "Manage master password...",
    "openNote": "openNote",
    "openNoteInNewWindow": "Open in new window",
    "openPdfViewer": "Open PDF viewer",
    "openPrimaryAppInstance": "Open primary app instance...",
    "openProfileDirectory": "Open profile directory",
    "openSecondaryAppInstance": "Open secondary app instance...",
    "openTag": "openTag",
    "pasteAsText": "Paste as text",
    "permanentlyDeleteNote": "Permanently delete note",
    "print": "Print",
    "renameFolder": "Rename",
    "renameTag": "Rename",
    "renderMarkup": "renderMarkup",
    "replaceMisspelling": "replaceMisspelling",
    "replaceSelection": "replaceSelection",
    "resetLayout": "Reset application layout",
    "restoreFolder": "Restore notebook",
    "restoreNote": "Restore note",
    "restoreNoteRevision": "Restore a note from history",
    "revealResourceFile": "Reveal file in folder",
    "scrollToHash": "scrollToHash",
    "search": "search",
    "selectedText": "selectedText",
    "setTags": "Tags",
    "showEditorPlugin": "Show editor plugin",
    "showLocalSearch": "Search in current note",
    "showModalMessage": "showModalMessage",
    "showNoteContentProperties": "Statistics...",
    "showNoteProperties": "Note properties",
    "showPrompt": "showPrompt",
    "showRevisions": "showRevisions",
    "showShareFolderDialog": "Share notebook...",
    "showShareNoteDialog": "Publish note...",
    "showSpellCheckerMenu": "Spell checker",
    "startExternalEditing": "Open in external editor",
    "stopExternalEditing": "Stop external editing",
    "switchProfile": "switchProfile",
    "switchProfile1": "Switch to profile 1",
    "switchProfile2": "Switch to profile 2",
    "switchProfile3": "Switch to profile 3",
    "synchronize": "Synchronise",
    # Note Tabs Plugin
    "tabsClear": "Remove all pinned Tabs",
    "tabsMoveLeft": "Move active Tab left",
    "tabsMoveRight": "Move active Tab right",
    "tabsPinNote": "Pin note to Tabs",
    "tabsSwitchLastActive": "Switch to last active Tab",
    "tabsSwitchLeft": "Switch to left Tab",
    "tabsSwitchRight": "Switch to right Tab",
    "tabsToggleVisibility": "Toggle Tabs visibility",
    "tabsUnpinNote": "Unpin note from Tabs",
    "textBold": "Bold",
    "textBulletedList": "Bulleted List",
    "textCheckbox": "Checkbox",
    "textCode": "Code",
    "textCopy": "Copy",
    "textCut": "Cut",
    "textHeading": "Heading",
    "textHorizontalRule": "Horizontal Rule",
    "textItalic": "Italic",
    "textLink": "Hyperlink",
    "textNumberedList": "Numbered List",
    "textPaste": "Paste",
    "textSelectAll": "Select all",
    "toggleAllFolders": "Toggle all notebooks",
    "toggleEditorPlugin": "Toggle editor plugin",
    "toggleEditors": "Toggle editors",
    "toggleExternalEditing": "Toggle external editing",
    "toggleLayoutMoveMode": "Change application layout",
    "toggleMenuBar": "Toggle menu bar",
    "toggleNoteList": "Toggle note list",
    "toggleNoteType": "Switch between note and to-do type",
    "toggleNotesSortOrderField": "Toggle sort order field",
    "toggleNotesSortOrderReverse": "Reverse sort order",
    "togglePerFolderSortOrder": "Toggle own sort order",
    "toggleSafeMode": "Toggle safe mode",
    "toggleSideBar": "Toggle sidebar",
    "toggleTabMovesFocus": "Toggle editor tab key navigation",
    "toggleVisiblePanes": "Toggle editor layout",
    "viewer.focus": "viewer.focus",
}


ctx.tags = ["user.command_client"]


def joplin_palette_command(command_id: str):
    """Fallback execution via the Command Palette modal."""
    actions.user.joplin_command_palette_key()
    actions.sleep("50ms")
    actions.insert(command_id)
    actions.sleep("30ms")
    actions.key("enter")


def command_server_or_client_fallback(command_id: str, args: list = None):
    """Execute command via file RPC; automatically falls back to palette if server is absent."""
    try:
        run_command(command_id, args)
    except NoFileServerException:
        print(
            "Command server failed; falling back to command palette. For better performance, install the Command Server plugin in Joplin: https://github.com/BlueDrink9/joplin-command-server"
        )
        joplin_palette_command(command_id)
    except Exception as e:
        joplin_palette_command(command_id)
        print("Command server failed; falling back to command palette.")
        print(e)


@mod.action_class
class Actions:
    def joplin_command_palette_key():
        """Show Joplin Command Palette"""
        actions.key("ctrl-shift-p")

    def joplin(command_id: str, args: list = None):
        """Invoke an action by Joplin command id"""
        command_server_or_client_fallback(command_id, args)


@mac_ctx.action_class("user")
class MacUserActions:
    def joplin_command_palette_key():
        actions.key("cmd-shift-p")


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.user.joplin("tabsPinNote")

    def tab_close():
        # Unpins/closes the active tab in Note Tabs
        actions.user.joplin("tabsUnpinNote")

    def tab_next():
        actions.user.joplin("tabsSwitchRight")

    def tab_previous():
        actions.user.joplin("tabsSwitchLeft")

    def tab_reopen():
        actions.user.joplin("tabsSwitchLastActive")

    def window_open():
        actions.user.joplin("openNoteInNewWindow")

    def window_close():
        if is_mac:
            actions.key("cmd-q")
        else:
            actions.key("ctrl-q")


@ctx.action_class("win")
class WinActions:
    def filename():
        title = actions.win.title()
        for suffix in (" - Joplin", " — Joplin"):
            if suffix in title:
                return title.split(suffix)[0]
        return title


@ctx.action_class("edit")
class EditActions:
    def undo():
        actions.user.joplin("editor.undo")

    def redo():
        actions.user.joplin("editor.redo")

    def copy():
        actions.user.joplin("textCopy")

    def cut():
        actions.user.joplin("textCut")

    def paste():
        actions.user.joplin("textPaste")

    def select_all():
        actions.user.joplin("textSelectAll")

    def save():
        actions.user.joplin("synchronize")

    def find(text: str = None):
        actions.user.joplin("showLocalSearch")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def find_next():
        actions.key("enter")

    def find_previous():
        actions.key("shift-enter")

    def line_swap_up():
        actions.user.joplin("editor.swapLineUp")

    def line_swap_down():
        actions.user.joplin("editor.swapLineDown")

    def line_clone():
        actions.user.joplin("editor.duplicateLine")

    def indent_more():
        actions.user.joplin("editor.indentMore")

    def indent_less():
        actions.user.joplin("editor.indentLess")

    def zoom_reset():
        if is_mac:
            actions.key("cmd-0")
        else:
            actions.key("ctrl-0")

    def zoom_in():
        if is_mac:
            actions.key("cmd-=")
        else:
            actions.key("ctrl-=")

    def zoom_out():
        if is_mac:
            actions.key("cmd--")
        else:
            actions.key("ctrl--")


@ctx.action_class("user")
class UserActions:
    def command_server_directory() -> str:
        return "joplin-command-server"

    def command_search(command: str = ""):
        actions.user.joplin_command_palette_key()
        if command:
            actions.sleep("50ms")
            actions.insert(command)

    def go_back():
        actions.user.joplin("historyBackward")

    def go_forward():
        actions.user.joplin("historyForward")

    def find_everywhere(text: str):
        actions.user.joplin("focusSearch")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def replace(text: str):
        actions.user.joplin("showLocalSearch")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def split_window():
        actions.user.joplin("toggleVisiblePanes")

    def split_window_vertically():
        actions.user.joplin("toggleVisiblePanes")

    def split_flip():
        actions.user.joplin("toggleEditors")

    def split_clear():
        actions.user.joplin("resetLayout")

    def split_next():
        actions.user.joplin("focusElementNoteViewer")

    def split_last():
        actions.user.joplin("focusElementNoteBody")

    # Not a community action
    # def delete_line():
    #     actions.user.joplin("editor.deleteLine")

    # Not a community action
    # def sort_lines():
    #     actions.user.joplin("editor.sortSelectedLines")
