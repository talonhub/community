# knausj_talon
Talon configs for Mac, Windows, and Linux. Very much in progress. This is also intended to work with both dragon and wav2letter.

Clone repo into ~/.talon/user/knausj_talon

    git clone git@github.com:knausj85/knausj_talon.git knausj_talon

It should look like

talon\user\knausj_talon

talon\user\knausj_talon\actions

talon\user\knausj_talon\lang

...

Otherwise it won't work. This is because paths to actions use folder names,
so avoid collisions we need a specific name.

## Talon file

Talon files maps words you want to say to things to do (definitions). They look a bit like YAML. 
They are split into 2 sections, the context and below are definitions.

### Context
There is a "header" section which is the context to activate the commands. This is everything above a
single - (hyphen/dash)

```os: windows
os: linux
app: Slack
app: slack.exe
```

The above restricts the definitions to an os of linux or windows, and an app name of Slack or slack.exe
You can also filter by app title:

```
app: Gnome-terminal
title: /emacs/
```

So in this case the definitions would only be active for the Gnome-terminal app with a title that contains emacs
The /'s around emacs mean it's a regular expression, so you can do all kinds of matching.

### Definitions

```
([channel] unread next | goneck): key(alt-shift-down)
```

() form a group

| means or

[] is optional

So in the above example you could say "channel unread next" or "goneck" or "unread next" and alt,
shift and down will be pressed at the same time.

Multiple things can happen by splitting the commands with a new line:

```insert code:
    insert("``````")
    key(left left left)
    key(shift-enter)
    key(shift-enter)
    key(up)
```

You can also do multiple presses in one key command, `key(left left left)` will press left three times

## Action files

Action files are where you define complex commands for talon (not just key presses). 
Below is the required structure

```python
from talon import Module, Context, actions, settings

mod = Module('description')
@mod.action_class
class Actions:
    def bare_action(): "Action prototypes must have a docstring."
    def capitalize(s: str) -> str:
    """This capitalizes a string."""
        return s.capitalize()
```

The [code](https://github.com/knausj85/knausj_talon/tree/master/code) folder has plenty of in-use examples

### Calling actions from talon files

Actions aren't much use unless you use them! You need to specify the full python path 
(the directory path separated by .) and call the function:

```channel <dgndictation>: 
    key(ctrl-k)
    user.knausj_talon.code.formatters.to_text(dgndictation)
```

## Another way to hook things up

I'm not sure what this is called, but you can make an empty actions file like [password manager](https://github.com/knausj85/knausj_talon/blob/master/code/password_manager.py)
and then define different things to do based on context e.g. [windows implementation](https://github.com/knausj85/knausj_talon/blob/master/code/win/password_manager.talon)
vs [mac implementation](https://github.com/knausj85/knausj_talon/blob/master/code/mac/password_manager.talon)

Then people can use those from a [generic place](https://github.com/knausj85/knausj_talon/blob/master/misc/1password.talon)
