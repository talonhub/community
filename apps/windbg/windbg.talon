# XXX - trigger alt-1 to hit command window for necessary commands?
# ex: user.windbg_insert_in_cmd()
#    edit.left()
tag: user.windbg
-
tag(): user.debugger

register <user.registers>:
    key(@)
    insert("{registers}")

open help: insert(".hh\n")

# xxx - add window switching

add microsoft symbols:
    insert("srv*C:\\symbols*http://msdl.microsoft.com/download/symbols;\n")
force reload symbols: insert(".reload /f\n")
reload symbols: insert(".reload\n")
loaded modules: insert("lm l\n")

display pointers: insert("dps ")

# XXX - should be generic
dereference pointer: user.insert_between("poi(", ")")

show version: key(ctrl-alt-w)

##
# Windows
##

view command: key(alt-1)
view watch: key(alt-2)
view locals: key(alt-3)
view registers: key(alt-4)
view memory: key(alt-5)
view call stack: key(alt-6)
view disassembly: key(alt-7)
view scratch pad: key(alt-8)
view (processes | threads): key(alt-9)

# XXX - temp
dump function params: "r @rcx,@rdx,@r8,@r9\n"

(lib | library) <user.windows_dlls>: "{windows_dlls}"
