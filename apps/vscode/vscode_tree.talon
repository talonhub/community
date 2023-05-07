app: vscode
-
# This opens the file tree in the sidebar
bar brow: user.vscode("workbench.view.extension.filetree")

# File tree commands
brow <user.letters>:
    user.run_rpc_command("talon-filetree.toggleDirectoryOrOpenFile", letters)
[brow] daddy <user.letters>:
    user.run_rpc_command("talon-filetree.closeParent", letters)
brow <user.letters> <number>:
    user.run_rpc_command("talon-filetree.expandDirectory", letters, number)
brow collapse <user.letters>:
    user.run_rpc_command("talon-filetree.expandDirectory", letters, 0)
brow move <user.letters> to <user.letters>:
    user.run_rpc_command("talon-filetree.moveFile", letters_1, letters_2)
brow move <user.letters> [to] root:
    user.run_rpc_command("talon-filetree.moveFile", letters_1)
# the recommended way to open a file is using the "toggleDirectoryOrOpenFile" command
# but this may be useful for people that want to separate the two actions
# e.g. to create very distinct commands that are easier for talon to differentiate
brow open <user.letters>:
    user.run_rpc_command("talon-filetree.openFile", letters)
brow rename <user.letters>: 
    user.run_rpc_command("talon-filetree.renameFile", letters)
brow create <user.letters>:
    user.run_rpc_command("talon-filetree.createFile", letters)
brow delete <user.letters>:
    user.run_rpc_command("talon-filetree.deleteFile", letters)
brow collapse root:
    user.run_rpc_command("talon-filetree.collapseRoot")
brow select <user.letters>:
    user.run_rpc_command("talon-filetree.select", letters)
brow git:
    user.run_rpc_command("talon-filetree.toggleGitIgnoredFiles")
brow current:
    user.run_rpc_command("talon-filetree.revealCurrentFile")