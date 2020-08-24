from talon import Context, Module

mod = Module()

tagList = [
    "debugger",
    "disassembler",
    "firefox",
    "gdb",
    "ida",
    "tabs",
    "tmux",
    "windbg",
]
for entry in tagList:
    mod.tag(entry, f"tag to load {entry} and/or related plugins ")
