from talon import Context, Module

mod = Module()

modes = {
    "gdb": "a way to force gdb commands to be loaded",
    "windbg": "a way to force windbg commands to be loaded",
    "ida": "a way to force ida commands to be loaded",
    "debug": "a way to force debugger commands to be loaded",
    "admin": "enable extra administration commands terminal (docker, etc)",
    "presentation": "a more strict form of sleep where only a more strict wake up command works",
    
}

for key, value in modes.items():
    mod.mode(key, value)
