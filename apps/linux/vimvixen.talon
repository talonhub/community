os: linux
tag: firefox
-
settings():
    user.vimvixen_auto_focus = 1

(page|tab) (previous|left):
    user.vimvixen_key("K")
(page|tab) (next|right):
    user.vimvixen_key("J")
(page|tab) (home|first):
    user.vimvixen_key("g")
    key(0)
(page|tab) (end|last):
    user.vimvixen_key("g")
    key($)
(page|tab) new:
    user.vimvixen_key("ctrl-t")
(page|tab) reopen:
    user.vimvixen_key("ctrl-shift-t")
(page|tab) close:
    user.vimvixen_key("d")
(page|tab) select:
    user.vimvixen_key("b")
last (page|tab):
    user.vimvixen_key("ctrl-6")
(page|tab) find:
    user.vimvixen_key("b")
    key(tab)
(page|tab) find <phrase>:
    user.vimvixen_key("b")
    insert("{phrase}")
(page|tab) open:
    user.vimvixen_key("escape")
    insert(":open ")
    key(tab)
(page|tab) open <phrase>:
    user.vimvixen_focus()
    insert(":open {phrase}")
    key(tab)
[(page|tab)] back:
    user.vimvixen_key("H")
[(page|tab)] forward:
    user.vimvixen_key("L")
[(page|tab)] refresh:
    user.vimvixen_key("r")
link:
    user.vimvixen_key("f")
link new:
    user.vimvixen_key("shift-f")
(address|Earl|link) bar:
    user.vimvixen_key("ctrl-l")
(address|Earl|link) copy:
    user.vimvixen_key("y")
copy (address|Earl|link):
    user.vimvixen_key("y")
add bookmark:
    user.vimvixen_key("a")
focus input:
    user.vimvixen_key("g")
    key("i")
zoom in:
    user.vimvixen_key("z")
    key("i")
zoom out:
    user.vimvixen_key("z")
    key("o")
zoom reset:
    user.vimvixen_key("z")
    key(z)
focus:
    user.vimvixen_focus()
search :
    user.vimvixen_key("ctrl-k")
search for <phrase>:
    user.vimvixen_key("ctrl-k")
    sleep(100ms)
    insert("{phrase}")
# If you use ddg by default
# duckduckgo google mode
google <phrase>:
    user.vimvixen_key("ctrl-k")
    sleep(100ms)
    insert("!g {phrase}")
# duckduckgo
duck duck <phrase>:
    user.vimvixen_key("ctrl-k")
    sleep(100ms)
    insert("{phrase}")

#  Moving around
(page|screen|scroll) down:
    user.vimvixen_key("ctrl-f")
half down:
    user.vimvixen_key("ctrl-d")
(page|screen|scroll) up:
    user.vimvixen_key("ctrl-b")
half up:
    user.vimvixen_key("ctrl-u")
top:
    user.vimvixen_key("g")
    key(g)
bottom:
    user.vimvixen_key("G")

mark <user.letter>:
    insert("m%({letter})s")
go to mark <user.letter>':
    insert("%({letter})s")
#  Searching
find <phrase>:
    user.vimvixen_key("/")
    insert("{phrase}")
    user.vimvixen_key("enter")
find:
    user.vimvixen_key("/")
next [result]:
    user.vimvixen_key("n")
(prev|previous) [result]:
    user.vimvixen_key("N")
(enable|disable) vixen:
    user.vimvixen_key("shift-escape")
open clipboard link:
    user.vimvixen_key("p")
open new clipboard link:
    user.vimvixen_key("P")
