from talon import Context, Module

mod = Module()

tagList = [
    "firefox",
    "gdb",
    "windbg",
    "tmux",
    "tabs",
    "debugger",
    "disassembler",
    "ida",
]
for entry in tagList:
    mod.tag(entry, f"tag to load {entry} and/or related plugins ")
