## BSPWM talon

This integrates the bspc control grammar for the [bspwm window
manager](https://github.come/baskerville/bspwm) with talon.

Enable it by adding the `tag(): user.bspwm` to one of your .talon files, e.g.
```talon
os: linux
-
tag(): user.bspwm
```

It is designed to match the bspc command line interface as closely as possible, so
you can directly convert most bspc commands to spoken commands.
For example, `bspc node --focus east` becomes "node focus east".
Other speech examples include "node focus right", "desktop swap next" "node to desktop next follow".

For convenience, some shortcuts and alternative utternances are included.
Mappings to replace works, e.g. to say "window" in place of "node", can be seen in `create_terminal` calls in [./bspwm.py](./bspwm.py). Some examples are below.

```python
    "node": "node",
    "window": "node",
    "desktop": "desktop",
    "desk": "desktop",
    "workspace": "desktop",
    "monitor": "monitor",
    "screen": "monitor",
    "to desktop": "--to-desktop",
    "to desk": "--to-desktop",
    "to workspace": "--to-desktop",
    "send": "--to-desktop",
    "to monitor": "--to-monitor",
    "to screen": "--to-monitor",
    "courier": "--to-monitor",
    "jump": "--to-monitor",
    "to node": "--to-node",
    "to window": "--to-node",
    "move": "--to-node",
    "warp": "--to-node",
    "focus": "--focus",
    "go": "--focus",
```
This also includes left and right etc as alternatives to east, west etc, as well as
for next and previous.

For quick focusing, you can omit "focus" and just say the object and
direction, for example "node left" or "screen right". This is enabled as a special
case in the talon file. You can also swap the verb and subject for simple actions,
for example "focus workspace previous" or "go window south".

To quickly change state you may omit the word "state", e.g. "node fullscreen".


If you wish to customise these, you will have to redeclare the whole lists or rules
in a python file. For example:
```python
from talon import Context
ctx = Context(")"
# Ensure your file takes prescedence over the default one
ctx.matches = """
os: linux
language: en
"""

# Name is the name in bspwm.py, prefixed with "user.bspwm_"
ctx.lists["user.bspwm_to_desktop"] = {
  ""meander" in the direction of space": "--to-desktop",
}
```
