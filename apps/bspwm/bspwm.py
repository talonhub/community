from talon import Module, Context, actions
import subprocess

mod = Module()
ctx = Context()

mod.tag("bspwm", desc="Enable commands to control the bspwm window manager")

def create_terminals(name, items):
    name = f"bspwm_{name}"
    mod.list(name, desc=f"BSPWM {name} terminals")
    ctx.lists[f"user.{name}"] = items

def create_capture(name: str, rule: str):
    """
    Creates a capture with the given name and rule.

    Args:
        name: The name of the capture (will be prepended with 'bspwm_')
        rule: The rule for the capture
    """
    # Prepend scope to all list and capture references.
    rule = (
        rule
        .replace("<", "<user.bspwm_")
        .replace("{", "{user.bspwm_")
    )
    name = f"bspwm_{name}"
    exec(
        f"""
@mod.capture(rule=\"\"\"{rule}\"\"\")
def {name}(m) -> str:
    # For descriptors and some other captures, we don't want to join words
    join_words = not "{name}".endswith("_descriptor")
    return " ".join(m) if join_words else str(m)
""")

    # @mod.capture(rule=rule)
    # def capture_function(m) -> str:
    #     return " ".join(m) if join_words else str(m)
    # # Rename the function to the desired name
    # capture_function.__name__ = f"bspwm_{name}"

BSPWM_CAPTURE_RULES = {
    "action": """
    <node_command> |
    <desktop_command> |
    <monitor_command> |
    <wm_command>
    """,

    # Second option for commands is an alternative option to use verb first
    "node_command": """
    {node} [<node_sel>] <node_actions>
    """,

    "desktop_command": """
    {desktop} [<desktop_sel>] <desktop_actions>
    """,

    "monitor_command": """
    {monitor} [<monitor_sel>] <monitor_actions>
    """,

    "wm_command": "{wm} <wm_actions>",

    # "object": "{node} | {desktop} | {monitor}",
    # "selector": "<node_sel> | <desktop_sel> | <monitor_sel>",
    "object": "{node} | {monitor}",
    "selector": "<node_sel> | <monitor_sel>",

    "node_actions": """
    {focus} [<node_sel>] |
    {activate} [<node_sel>] |
    {to_desktop} <desktop_sel> [{follow}] |
    {to_monitor} <monitor_sel> [{follow}] |
    {to_node} <node_sel> [{follow}] |
    {swap} <node_sel> [{follow}] |
    {presel_dir} {dir} |
    {cancel} |
    {presel_ratio} <number> |
    <state_command> |
    <resize_command> |
    {move} <number> <number> |
    {insert_receptacle} |
    {close} |
    {kill}
    """,

    "desktop_actions": """
    {focus} [<desktop_sel>] |
    {activate} [<desktop_sel>] |
    {to_monitor} <monitor_sel> [{follow}] |
    {swap} <desktop_sel> [{follow}] <monitor_sel> |
    {layout} {layout_type} |
    {remove}
    """,

    "monitor_actions": """
    {focus} [<monitor_sel>] |
    {swap} <desktop_sel> [{follow}] |
    {add_desktops} {space} |
    {remove}
    """,

    "wm_actions": """
    {dump_state} |
    {load_state} <text> |
    {adopt_orphans} |
    {record_history} ({on} | {off}) |
    {restart}
    """,

    "state_command": "{state} {state}",

    "resize_command": "{resize} {resize_direction} <number> <number>",

    "node_sel": "[<node_sel>] <node_descriptor> [<node_modifier>]",

    "desktop_sel": "[<desktop_sel>] <desktop_descriptor> [<desktop_modifier>]",

    "monitor_sel": "[<monitor_sel>] <monitor_descriptor> [<monitor_modifier>]",

    "node_descriptor": "<basic_descriptor> | {biggest} | {smallest}",

    "desktop_descriptor": "<desktop_cycle_descriptor> | <number>",

    "monitor_descriptor": "<basic_descriptor> | {primary} | <number>",

    "node_modifier": "[{not}] {common_modifier}",

    "desktop_modifier": "[{not}] ({common_modifier} | {occupied} | {local})",

    "monitor_modifier": "[{not}] ({focused} | {occupied})",

    "basic_descriptor": """
        {dir} |
        {cycle_dir} |
        {any} |
        {first_ancestor} |
        {last} |
        {newest} |
        {older} |
        {newer} |
        {focused} |
        {pointed}
        """,

    "cycle_descriptor": """
        {cycle_dir} |
        {any} |
        {last} |
        {newest} |
        {older} |
        {newer}
        """,

    "desktop_cycle_descriptor": """
        <cycle_descriptor> | {desktop_cycle_dir}
        """,

}


# Terminal definitions
create_terminals("node", {
    "node": "node",
    "window": "node",
})
create_terminals("desktop", {
    "desktop": "desktop",
    "desk": "desktop",
    "workspace": "desktop",
})
create_terminals("monitor", {
    "monitor": "monitor",
    "screen": "monitor",
})
create_terminals("wm", {"wm": "wm"})

# Command terminals
create_terminals("to_desktop", {"to desktop": "--to-desktop"})
create_terminals("to_monitor", {"to monitor": "--to-monitor"})
create_terminals("to_node", {"to node": "--to-node"})
create_terminals("follow", {"follow": "--follow"})
create_terminals("presel_dir", {"presel dir": "--presel-dir"})
create_terminals("cancel", {"cancel": "cancel"})
create_terminals("presel_ratio", {"presel ratio": "--presel-ratio"})
create_terminals("move", {"move": "--move"})
create_terminals("insert_receptacle", {"insert receptacle": "--insert-receptacle"})
create_terminals("close", {"close": "--close"})
create_terminals("kill", {"kill": "--kill"})
create_terminals("layout", {"layout": "--layout"})
create_terminals("remove", {"remove": "--remove"})
create_terminals("add_desktops", {"add desktops": "--add-desktops"})
create_terminals("dump_state", {"dump state": "--dump-state"})
create_terminals("load_state", {"load state": "--load-state"})
create_terminals("adopt_orphans", {"adopt orphans": "--adopt-orphans"})
create_terminals("record_history", {"record history": "--record-history"})
create_terminals("on", {"on": "on"})
create_terminals("off", {"off": "off"})
create_terminals("restart", {"restart": "--restart"})
create_terminals("focus", {
    "focus": "--focus",
    "go": "--focus",
})
create_terminals("activate", {"activate": "--activate"})
create_terminals("swap", {"swap": "--swap"})
create_terminals("state", {"state": "--state"})
create_terminals("resize", {"resize": "--resize"})
create_terminals("space", {"space": " "})

# Descriptor terminals
create_terminals("biggest", {"biggest": "biggest"})
create_terminals("smallest", {"smallest": "smallest"})
create_terminals("primary", {"primary": "primary"})
create_terminals("any", {"any": "any"})
create_terminals("first_ancestor", {"first ancestor": "first_ancestor"})
create_terminals("last", {"last": "last"})
create_terminals("newest", {"newest": "newest"})
create_terminals("older", {"older": "older"})
create_terminals("newer", {"newer": "newer"})
create_terminals("focused", {"focused": "focused"})
create_terminals("pointed", {"pointed": "pointed"})
create_terminals("not", {"not": "!"})
create_terminals("occupied", {"occupied": "occupied"})
create_terminals("local", {"local": "local"})

# Base types
create_terminals("dir", {
    "north": "north",
    "west": "west",
    "south": "south",
    "east": "east",
    "up": "north",
    "left": "west",
    "down": "south",
    "right": "east",
})

create_terminals("cycle_dir", {
    "next": "next",
    "prev": "prev",
    "previous": "prev",
})

create_terminals("desktop_cycle_dir", {
    "next": "next",
    "prev": "prev",
    "previous": "prev",
    "left": "prev",
    "right": "next",
})

create_terminals("state", {
    "tiled": "tiled",
    "pseudo tiled": "pseudo_tiled",
    "floating": "floating",
    "fullscreen": "fullscreen"
})

create_terminals("resize_direction", {
    "top": "top",
    "left": "left",
    "bottom": "bottom",
    "right": "right",
    "top left": "top_left",
    "top right": "top_right",
    "bottom right": "bottom_right",
    "bottom left": "bottom_left"
})

create_terminals("layout_type", {
    "tiled": "tiled",
    "monocle": "monocle"
})

create_terminals("common_modifier", {
    "focused": "focused",
    "active": "active",
    "automatic": "automatic",
    "leaf": "leaf",
    "window": "window",
    "same class": "same_class",
    "descendant of": "descendant_of",
    "ancestor of": "ancestor_of",
    "hidden": "hidden",
    "sticky": "sticky",
    "private": "private",
    "locked": "locked",
    "marked": "marked",
    "urgent": "urgent",
    "below": "below",
    "normal": "normal",
    "above": "above",
    "horizontal": "horizontal",
    "vertical": "vertical",
    "local": "local"
})

# Create all captures from the dictionary
for name, rule in BSPWM_CAPTURE_RULES.items():
    create_capture(name, rule)

# Have to define this separately because it isn't referencing an internal capture
@mod.capture(rule="<number_small>")
def bspwm_number(m) -> str:
    "number_small"
    return m

# Have to define this separately because it isn't referencing an internal capture
@mod.capture(rule="<phrase>")
def bspwm_text(m) -> str:
    "number_small"
    return m



def bspc_command(*args: tuple[str]):
    args = [arg for part in args for arg in part.split() if arg]
    result = subprocess.run(["bspc", *args], capture_output=True, text=True)
    if result.stderr:
        argstr =" ".join(args)
        print(f"BSPC error running `bspc {argstr}`: {result.stderr}")
    # else:
    #     print(f"Output: {result.stdout}")

@mod.action_class
class Actions:
    def bspwm_object_command(domain: str, actions: str, selector: str):
        """Execute a complete bspwm command"""
        bspc_command(domain, actions, selector)

    def bspwm_command(actions: str):
        """Execute a complete bspwm command"""
        bspc_command(actions)
