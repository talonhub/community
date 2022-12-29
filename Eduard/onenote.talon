os: windows
and app.exe: ONENOTE.EXE
-
bold: key(ctrl-b)
italic: key(ctrl-i)
strike through: key(ctrl--)
highlight: key(ctrl-alt-h)

bullet: key(ctrl-.)
check | done: key(ctrl-1)
tag clear: key(ctrl-0)

#insert date: key(alt-shift-d)

heading one: key(ctrl-alt-1)
heading two: key(ctrl-alt-2)
normal: key(ctrl-shift-n)

code:
    key(ctrl-shift-n alt-h)
    sleep(50ms)
    key(alt-l up enter)

move up: key(alt-shift-up)
move down: key(alt-shift-down)
move right: key(alt-shift-right)
move left: key(alt-shift-left)

# for consistency with Mac version, where collapsing will collapse to level 1
collapse: key(alt-shift-1)
expand: key(alt-shift-+)

go (notebook | notebooks): key(ctrl-g)

go (section | sections): key(ctrl-shift-g)
section previous: key(ctrl-shift-tab)
section next: key(ctrl-tab)

go (page | pages): key(ctrl-alt-g)
page new: key(ctrl-n)
page delete: key(ctrl-alt-g delete)
page previous: key(ctrl-pageup)
page next: key(ctrl-pagedown)
page move right: key(ctrl-alt-g shift-f10 s)
page move left: key(ctrl-alt-g shift-f10 o enter)

[page] rename date [<user.prose>]$:
    key(ctrl-shift-t alt-shift-d)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")
    
[page] rename [<user.prose>]$:
    key(ctrl-shift-t)
    user.insert_formatted(prose or "", "CAPITALIZE_FIRST_WORD")
    
go forward: key(alt-right)
go back[ward]: key(alt-left)

[open] link: key(shift-f10 l)
edit link: key(ctrl-k)
copy link: key(shift-f10 p)
paste link: key(ctrl-k alt-e ctrl-v enter)
remove link: key(shift-f10 r)

# not standard OneNote; triggers an AutoHotKey macro I wrote
#today: key(super-alt-d)

#tomorrow:
    key(super-alt-shift-d)
    sleep(300ms)
    key(1)
    
#<digit_string> days:
    key(super-alt-shift-d)
    sleep(300ms)
    insert(digit_string)
    
# back to progress (first notebook, first section)
go progress:
    key(ctrl-g home enter tab:2 down enter esc)
settings():
    user.context_sensitive_dictation = 1