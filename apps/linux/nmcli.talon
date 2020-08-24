os: linux
tag: terminal
-

net man running: "nmcli -t -f RUNNING general\n"
net man status: "nmcli general\n"
net man devices: "nmcli\n"
net man connect :
    insert("nmcli con up ")
    key(tab)
net man disconnect :
    insert("nmcli con down ")
    key(tab)
net man edit:
    insert("nmcli con edit ")
    key(tab)
