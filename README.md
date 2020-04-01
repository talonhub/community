# knausj_talon

Talon configs for Mac, Windows, and Linux. Very much in progress. This is also intended to work with both Dragon Naturally Speaking and wav2letter.

Clone repo into `~/.talon/user`

    `cd ~/.talon/user`
    `git clone git@github.com:knausj85/knausj_talon.git knausj_talon`

The folder structure should look like:

`~/.talon/user/knausj_talon`

`~/.talon/user/knausj_talon/code`

`~/.talon/user/knausj_talon/lang`

If using wav2letter, extract the entire contents of the tarball (found pinned in Talon's @beta slack channel) in `~/.talon`. The resulting tree should be:
`~/.talon/w2l/en_US`
`~/.talon/user/w2l.py`

## Jetbrains commands

For Jetbrains commands to work you must install https://plugins.jetbrains.com/plugin/10504-voice-code-idea
into each editor.

...

## Windows

Talon should be located in the Program Files directory (or another 'secure' directory). Talon has been signed and now utilizes uiAccess.

C:\Program Files\talon

Note this is required for

(1) eye tracking to work with applications that are run as admin (e.g., regedit) on Windows; and

(2) the zoom mouse to appear over the start menu, and other applications with uiAccess; and

(3) Talon to interact with User Account Control dialogs

## .talon file

.talon files may be used for

- implementing actions
- defining the overall context for commands and actions
- implementing voice commands

### Context

There is a "header" section in .talon files that defines the context for the commands. This is everything above the hyphen/dash in the .talon file.

```insert code:
os: windows
os: linux
app: Slack
app: slack.exe
app: Teams
-
```

The above restricts the commands:

- Linux or Windows OS; and
- An app name of Slack, slack.exe, or Teams.

Any commands would not be available on Mac OS, for example.

You can also filter by window title.

```
app: Gnome-terminal
title: /emacs/
-
```

In this case the definitions would only be active for the Gnome-terminal app with a window title that contains emacs.
The /'s around emacs mean it's a regular expression, so you can do all kinds of matching. This should be done sparingly in scripts you intend to share.

### Defining Voice Commands

Going forward, all voice commands will be implemented in .talon files.

```insert code:
([channel] unread next | goneck): key(alt-shift-down)
```

() form a group

| means or

[] means optional

In the above example, saying any of below voice commands:

- "channel unread next"
- "unread next"
- "goneck"

will execute the shortcut alt-shift-down.

You can perform many actions with a single command, as below:

```insert code:
    insert("``````")
    key(left left left)
    key(shift-enter)
    key(shift-enter)
    key(up)
```

Note that you can also do many key presses in one command, `key(left left left)` will press left three times.

## Modules: Declaring actions and captures

With python scripts, you may declare and implement new actions and captures.

Modules declare actions and captures; actions may have a default implementation. Actions and captures then can be combined to compose extremely useful voice commands in .talon files.

### Actions

Actions are the functionality assigned to a voice command, e.g. the action for the command "new tab" would implement opening the tab.

All user-defined actions in this repository are prefixed with "user." by talon

```python
from talon import Module, Context, actions, settings

mod = Module()
@mod.action_class
class Actions:
    def bare_action():
        """Action prototypes must have a docstring."""

    def capitalize(s: str) -> str:
    """This capitalizes a string."""
        return s.capitalize()
```

In the above example, `bare_action()` is declared, but not implemented. On the other hand, `capitalize()` has a default implementation that could be overridden for some contexts.

Actions may be implemented in a .talon file, allowing the implementation to be customized per-context as needed. The below example for `bare_action()` is active only (1) on Linux and (2) when the Slack application has focus.

```insert code:
os: linux
app: Slack
-
action(user.bare_action):
    insert("LINUX")

```

This makes actions very reusable, particularly across OSes, applications, and programming languages. In this way, you could define a single command that works across all programming languages, etc.

For example, window_management.talon leverages this ability to redefine actions per context to make voice commands that do the right thing regardless of operating system (voice commands on the left and actions on the right):

```insert code:
new window: app.window_open()
next window: app.window_next()
last window: app.window_previous()
close window: app.window_close()
focus <user.running_applications>: user.switcher_focus(running_applications)
```

The Talon-declared app actions are defined per-operating system in separate OS-specific .talon files. The voice commands themselves work across all operating systems.

Note that if you attempt to use an action in a context that has no implementation for the action, you will see warnings in the Talon log.

### Captures

Captures must be declared in a module, and do not currently support having a default implementation within the module like actions. This is coming soon.

These examples are from `formatters.py`.

```python:
mod = Module()
mod.list('formatters', desc='list of formatters')

@mod.capture
def formatters(m) -> list:
    "Returns a list of formatters"
```

The above declares a 'formatters' capture that returns a list. The module also declares a list/mapping of the formatters to capture (snake, camel, etc). These mappings can be static, as in formatters.py, or dynamic, as in switcher.py, which is used to switch between running applications).

To implement a capture, you must create a context in python. Note that contexts are anonymous.

```python:
ctx = Context()
@ctx.capture(rule='{self.formatters}+')
def formatters(m):
    return m.formatters
```

When used in .talon, this capture will provide a list of words matching any the module's 'formatters' list defined above. The result can then be provided to another action.

You may define other useful captures by combining captures too. For example, the below capture will provide formatted text for commands such as "allcaps dubstring something interesting" => "SOMETHING INTERESTING" -

```python:
@ctx.capture(rule='<self.formatters> <phrase>')
def format_text(m):
    return FormatText(m.phrase, m.formatters)
```

Once defined, you can then use the captures and associated actions in .talon files!

```insert code:
<user.formatters_format_text> [over]: insert(format_text)
```

This will simply insert the pre-formatted text into your editor.
