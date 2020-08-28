from talon import Context, Module

mod = Module()

tagList = ["firefox", "gdb", "tmux", "tabs"]
modes = {
    "gdb": "a way to force gdb commands to be loaded",
}

for entry in tagList:
    mod.tag(entry, f"tag to load {entry} and/or related plugins ")

for key, value in modes.items():
    mod.mode(key, value)

