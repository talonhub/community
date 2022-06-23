from talon import Module

mod = Module()

tagList = [
    "debugger",
    "disassembler",
    "gdb",
    "git",  # commandline tag for git commands
    "ida",
    "tabs",
    "generic_windows_shell",
    "generic_unix_shell",
    "taskwarrior",  # commandline tag for taskwarrior commands
    "tmux",
    "windbg",
]
for entry in tagList:
    mod.tag(entry, f"tag to load {entry} and/or related plugins ")
