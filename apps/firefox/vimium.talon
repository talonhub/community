os: linux
tag: user.vimium
-

# Navigating the page
down:
    key("j")
up:
    key("k")
[page] top:
    key("g")
    key(g)
[page] bottom:
    key("G")
half up:
    key("u")
half down:
    key("d")
# XXX - these conflict with tech edit boxes
#left:
#    key("h")
#right:
#    key("l")
(page|tab) (refresh|reload):
    key("r")
(address|Earl|link) copy:
    insert("yy")
copy (address|Earl|link):
    insert("yy")
yankee:
    insert("yy")
open clipboard link:
    key("p")
open new clipboard link:
    key("P")
(insert mode|disable vimium):
    key("i")
visual mode:
    key("v")
visual line mode:
    key("V")
enable vimium:
    key("escape")
focus input:
    key("g")
    key("i")
[open] links [hints]:
    key("f")
[open] links [hints] new:
    key("F")
# TODO: open multiple links
copy page links:
    insert("yf")
follow previous [link]:
    insert("[[")
follow next [link]:
    insert("]]")
select next frame:
    insert("gf")
select main frame:
    insert("gF")
mark <user.letter>:
    insert("m{letter}")
go to mark <user.letter>':
    insert("`{letter}")

# Using the vomnibar
(page|tab) open:
    insert("o")
(page|tab) open <user.text>:
    key("o")
    insert("{text}")
(page|tab) open new:
    insert("O")
(page|tab) open new <user.text>:
    key("O")
    insert("{text}")
(page|tab) open bookmark:
    insert("b")
(page|tab) open bookmark <user.text>:
    insert("b")
    insert("{text}")
(page|tab) open bookmark new:
    insert("B")
(page|tab) open bookmark new <user.text>:
    insert("B")
    insert("{text}")
tab find:
    key("T")
edit address bar:
    insert("ge")
edit address bar new tab:
    insert("gE")

# Using find
#  Searching
page (search|find) <user.text>:
    key("/")
    insert("{text}")
    key("enter")
page (search|find):
    key("/")
result next:
    key("n")
result last:
    key("N")

# Navigating history
page back:
    key("H")
page forward:
    key("L")

# Manipulating tabs

(page|tab) new:
    key("t")
(page|tab) (previous|left):
    insert("gT")
(page|tab) (next|right):
    insert("gt")
(page|tab) flip:
    key("^")
(page|tab) (end|last):
    key("g")
    key($)
tab <number_small>:
    key("g")
    key(0)
    sleep(200ms)
    user.repeat_insert("gt", number_small)
(page|tab) duplicate:
    insert("yt")
# pin tab
# mute tab
(page|tab) close:
    key("x")
(page|tab) reopen:
    key("X")
(page|tab) new tab:
    key("W")
move tab left:
    insert("<<")
move tab right:
    insert(">>")

# Miscellaneous
vimium help:
    key("?")

# Unsorted
web search :
    key("ctrl-k")
web search for <user.text>:
    key("ctrl-k")
    sleep(100ms)
    insert("{text}")
# NOTE: If you use ddg by default
# duckduckgo google mode
google <user.text>:
    key("ctrl-k")
    sleep(100ms)
    insert("!g {text}")
# duckduckgo
duck duck <user.text>:
    key("ctrl-k")
    sleep(100ms)
    insert("{text}")

#
(page|tab) focus:
    # highlight URL bar
    key("ctrl-l")
    sleep(10ms)
    # pop keyboard
    key("escape")
    # trigger find (won't work unless we were in URL bar
    key("ctrl-f")
    sleep(10ms)
    # escape out of find window
    key("escape")
    key("escape")
    # now have general focus
page close:
    app.tab_close()
