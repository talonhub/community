app: keepass
-
# Database
open database: key(ctrl-o)
save database: key(ctrl-s)
close database: key(ctrl-w)
lock database: key(ctrl-l)
quit: key(ctrl-q)

# Entries
[add] new entry: key(ctrl-n)
clone entry: key(ctrl-k)
(view | edit) entry: key(ctrl-e)
delete entry: key(ctrl-d)
copy user [name]: key(ctrl-b)
copy password: key(ctrl-c)
open (earl | url | link): key(ctrl-u)
copy (earl | url | link): key(ctrl-alt-u)
find: key(ctrl-f)
find <user.text>:
    key(ctrl-f)
    insert("{text}")
