os: linux
tag: terminal
-

# ghidraSvr
ghidra server status: "server/ghidraSvr status\n"
ghidra server stop: "server/ghidraSvr stop\n"
ghidra server start: "server/ghidraSvr start\n"
ghidra server install: "server/ghidraSvr install\n"
ghidra server restart: "server/ghidraSvr restart\n"
ghidra server: "server/ghidraSvr "

# svrAdmin
ghidra admin: "server/svrAdmin "
ghidra list (repo|repositories): "server/svrAdmin -list\n"
ghidra list user access: "server/svrAdmin -list -users\n"
ghidra list users: "server/svrAdmin -users\n"
ghidra add user: "server/svrAdmin -add "
ghidra remove user: "server/svrAdmin -remove "
ghidra reset password: "server/svrAdmin -reset "

# misc
ghidra edit config: "vi server/server.conf\n"
# NOTE: you will have to edit this path to match your repo directory
ghidra edit log: "vi ../repo/server.log\n"
