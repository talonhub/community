# https://support.office.com/en-us/article/keyboard-shortcuts-for-outlook-3cdeb221-7ae5-4c1d-8c1d-9e63216c1efd#PickTab=Web
# the shortcuts below our based half of the bill in short cut menu, but the
# link above has significantly more that could so be added
os: linux
tag: browser
win.title: /Outlook/
-

# write email
new message: key(n)
send [this] message: key(alt-s)
reply [to] [this] message: key(r)
reply all [to] [this] message: key(ctrl-shift-r)
forward [this] message: key(ctrl-shift-f)
save [draft]: key(ctrl-s)
discard [draft]: key(esc)
insert [a] [hyper] link: key(ctrl-k)

# email list
(select | unselect) [this] message: key(ctrl-space)
select all [messages]: key(ctrl-a)
clear all [messages]: key(esc)
select first [message]: key(home)
select last [message]: key(and)

# read email
open [this] message: key(o)
open [this] message [in] [a] new window: key(shift-enter)
close [this] message: key(esc)
[open] [the] next (item | message): key(ctrl-.)
[open] [the] (prev | previous) item: key(ctrl-,)
next reading [pane] (item | message): key(.)
(prev | previous) [pane] (item | message): key(,)
(expand | collapse) [conversation]: key(x)

# go to
go [to] mail: key(ctrl-shift-1)
go [to] calendar: key(ctrl-shift-2)
go [to] people: key(ctrl-shift-3)
go [to] to do: key(ctrl-shift-4)
go [to] inbox:
    key(g)
    key(i)
go to drafts:
    key(g)
    key(d)
go to sent:
    key(g)
    key(s)
search [email]: key(alt-q)
show help: key(?)

# email actions
undo [last] [action]: key(ctrl-z)
delete [this] [message]: key(delete)
(perm | permanently) delete [this] [message]: key(shift+delete)
new folder: key(shift-e)
mark [this] [(item | message)] as read: key(q)
mark [this] [(item | message)] as unread: key(u)
flag [this] [(item | message)]: key(insert)
archive: key(e)
mark [this] [message] [as] junk: key(j)
moved to [a] folder: key(v)
categorize [this] message: key(c)
