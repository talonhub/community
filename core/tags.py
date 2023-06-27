from talon import Module

mod = Module()

tagList = [
    "disassembler",
    "git",  # commandline tag for git commands
    "ida",
    "tabs",
    "generic_windows_shell",
    "generic_unix_shell",
    "readline",
    "taskwarrior",  # commandline tag for taskwarrior commands
    "tmux",
]
for entry in tagList:
    mod.tag(entry, f"tag to load {entry} and/or related plugins ")
