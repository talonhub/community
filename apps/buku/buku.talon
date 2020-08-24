os: linux
tag: terminal
-

# general options
bookoo help: "buku -h\n"
bookoo version: "buku -v\n"
bookoo auto add:
    insert("buku -a ")
    edit.paste()
    key(enter)
    insert("buku -w -1\n")

bookoo update: "buku -u "
bookoo edit: "buku -w "
bookoo edit last:
    insert("buku -w -1\n")

# edit options

# search options
bookoo search: "buku -s "
