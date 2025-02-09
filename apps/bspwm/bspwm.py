from talon import Module, Context, actions, app
import logging
import subprocess

mod = Module()
ctx = Context()

mod.tag("bspwm", desc="Enable commands to control the bspwm window manager")

mod = Module()
mod.list("bspwm_domain", desc="BSPWM domains")
mod.list("bspwm_node_selector", desc="BSPWM node selectors")
mod.list("bspwm_desktop_selector", desc="BSPWM desktop selectors")
mod.list("bspwm_monitor_selector", desc="BSPWM monitor selectors")
mod.list("bspwm_selector", desc="BSPWM combined selectors")
mod.list("bspwm_command", desc="BSPWM commands")
mod.list("bspwm_state", desc="BSPWM states")
mod.list("bspwm_flag", desc="BSPWM flags")
mod.list("bspwm_modifier", desc="BSPWM modifiers")

ctx = Context()
ctx.lists["user.bspwm_domain"] = {
    "node": "node",
    "window": "node",
    "desktop": "desktop",
    # Shorthand
    "desk": "desktop",
    "monitor": "monitor",
    "screen": "monitor",
    "window manager": "wm",
}

DIR = {
    "north": "north",
    "west": "west",
    "south": "south",
    "east": "east",
    "next": "next",
    "up": "north",
    "left": "west",
    "down": "south",
    "right": "east",
}
# TODO: make .local for all except monitor, and have 'big' or 'way' variants that aren't local
CYCLE_DIR = {
    "next": "next",
    "previous": "prev",
    "prev": "prev",
}
ctx.lists["user.bspwm_node_selector"] = {
    **DIR,
    **CYCLE_DIR,
    "focused": "focused",
    "pointed": "pointed",
}

DESKTOP_MODIFIERS = {
    "in local": ".local",
    "in occupied": ".occupied",
    "in urgent": ".urgent",
    "in active": ".active",
    "in focused": ".focused",
}

ctx.lists["user.bspwm_desktop_selector"] = {
    "any": "any",
    "focused": "focused",
    "last": "last",
    "newest": "newest",
    "older": "older",
    "newer": "newer",
    **CYCLE_DIR,
    "right": "next.local",
    "left": "prev.local",
}

ctx.lists["user.bspwm_monitor_selector"] = {
    "any": "any",
    "focused": "focused",
    "pointed": "pointed",
    "primary": "primary",
    "last": "last",
    "newest": "newest",
    "older": "older",
    "newer": "newer",
    **CYCLE_DIR,
    **DIR,
    "occupied": ".occupied",
    "focused only": ".focused",
}

# ctx.lists["user.bspwm_selector"] = {
#     **ctx.lists["user.bspwm_node_selector"],
#     **ctx.lists["user.bspwm_desktop_selector"],
#     **ctx.lists["user.bspwm_monitor_selector"],
# }

ctx.lists["user.bspwm_command"] = {
    "focus": "--focus",
    "activate": "--activate",
    "swap": "--swap",
    "move": "--move",
    "send to desktop": "--to-desktop",
    "send to monitor": "--to-monitor",
    "to desktop": "--to-desktop",
    "to monitor": "--to-monitor",
    "resize": "--resize",
    "close": "--close",
    "kill": "--kill",
    "state": "--state",
    "flag": "--flag",
}

ctx.lists["user.bspwm_state"] = {
    "tiled": "tiled",
    "pseudo tiled": "pseudo_tiled",
    "floating": "floating",
    "fullscreen": "fullscreen",
}

ctx.lists["user.bspwm_flag"] = {
    "hidden": "hidden",
    "sticky": "sticky",
    "private": "private",
    "locked": "locked",
    "marked": "marked",
    "urgent": "urgent",
}

ctx.lists["user.bspwm_modifier"] = {
    "focused": "focused",
    "active": "active",
    "leaf": "leaf",
    "window": "window",
    "same class": "same_class",
}

# Capture rules using the lists defined above
@mod.capture(rule="{user.bspwm_domain}")
def bspwm_domain(m) -> str:
    """Capture BSPWM domain"""
    return str(m)

@mod.capture(rule="<user.bspwm_node_selector> | <user.bspwm_monitor_selector> | <user.bspwm_desktop_selector>")
def bspwm_selector(m) -> str:
    """Capture any BSPWM selector"""
    return str(m)

@mod.capture(rule="{user.bspwm_node_selector}")
def bspwm_node_selector(m) -> str:
    """Capture BSPWM node selector"""
    return str(m)

@mod.capture(rule="{user.bspwm_desktop_selector} | <number_small>")
def bspwm_desktop_selector(m) -> str:
    """Capture BSPWM desktop selector"""
    print(m)
    if hasattr(m, "number_small"):
        return f"^{m.number_small}"  # BSPWM syntax for numbered desktops
    if hasattr(CYCLE_DIR, m):
        # For desktops, don't focus outside current monitor, so you can cycle around.
        # Probably should be exposed as an option.
        return f"{m}.local"
    return str(m)

@mod.capture(rule="{user.bspwm_monitor_selector} | <number_small>")
def bspwm_monitor_selector(m) -> str:
    """Capture BSPWM monitor selector"""
    if hasattr(m, "number_small"):
        return f"^{m.number_small}"  # BSPWM syntax for numbered monitors
    return str(m)

@mod.capture(rule="{user.bspwm_command}")
def bspwm_command(m) -> str:
    """Capture BSPWM command"""
    return str(m)

def bspc_command(*args: str):
    """Execute a bspc command."""
    args = [item for item in args if item]
    print(args)
    # args = " ".join(args).split(" ")
    result = subprocess.run(["bspc", *args], capture_output=True)
    if result.stderr:
        raise subprocess.CalledProcessError(
                returncode = result.returncode,
                cmd = result.args,
                stderr = result.stderr
                )
    if result.stdout:
        print("Command Result: {}".format(result.stdout.decode('utf-8')))


@mod.action_class
class Actions:
    def bspwm_command(domain: str, selector: str, command: str):
        """Execute a bspwm command"""
        bspc_command(domain, command, selector)

    def bspwm_state_command(domain: str, selector: str, state: str):
        """Set the state of a bspwm node"""
        bspc_command(domain, "--state", state, selector)

    def bspwm_flag_command(domain: str, selector: str, flag: str):
        """Set a flag on a bspwm node"""
        bspc_command(domain, "--flag", flag, selector)

    def bspwm_node_change_action(command: str, selector: str):
        """Handle actions affecting a node"""
        bspc_command("node", command, selector)

    # def bspwm_action(command: str, noun: str, selector: str):
    #     """Handle a general bspwm action."""
    #     if selector.isdigit():
    #         if noun == "desktop":
    #             bspc_command("desktop", command, f"^{selector}")
    #         elif noun == "monitor":
    #             bspc_command("monitor", command, f"@{selector}")
    #         return

        # bspc_command(noun, command, selector)
