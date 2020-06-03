tag: vim
win.title: /NERD_tree/
-

change root: key(C)
close parent: key(x)
close all children: key(X)
refresh [directory]: key(r)
refresh root [directory]: key(R)

# file node mappings
open (line|file|node) <number>$:
    insert(":{number}\n")
    key(o)
recursive open [file]: key(O)
open file: key(o)
open file [in] split: key(i)
open file [in] vertical split: key(s)

# directory node mappings
close (line|file|node) <number>$:
    insert(":{number}\n")
    key(o)
close parent node: key(x)
close all nodes: key(X)
edit directory: key(e)

# filesystem mappings
menu: key(m)

# menu-based actions
(add|new) (node|file): "ma"
(remove|delete) (node|file): "md"
(move|rename) (node|file): "mm"
list (node|file): "ml"
copy (node|file): "mc"

# tree navigation mappings
go root [(dur|dir|directory)]: key(P)
go parent [(dur|dir|directory)]: key(p)
go first child [(dur|dir|directory)]: key(K)
go last child [(dur|dir|directory)]: key(J)

# tree filtering mappings
show hidden files: key(I)

# other mappings
quick help: key(?)
close nerd [tree]: key(q)
nerd close: key(q)
