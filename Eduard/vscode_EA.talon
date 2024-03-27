#custom vscode commands go here
app: vscode
-


# jupyter
cell next: user.vscode("list.focusDown")
cell last: user.vscode("list.focusUp")
run head notebook: user.vscode("notebook.cell.executeCellsAbove")
run cell: user.vscode("notebook.cell.executeAndSelectBelow")
run notebook: user.vscode("notebook.execute")
cell edit: user.vscode("notebook.cell.edit")
cell last edit: user.vscode("notebook.focusPreviousEditor")
cell exit: user.vscode("notebook.cell.quitEdit")
new cell: user.vscode("jupyter.notebookeditor.addcellbelow")
new mark:
    user.vscode("jupyter.notebookeditor.addcellbelow")
    key("escape")
    key("m")
delete cell: 
    key("escape")
    key("d:2")

running: user.vscode('notebook.revealRunningCell')
clear notebook outputs: user.vscode('notebook.clearAllCellsOutputs')
focus output: user.vscode('notebook.cell.focusInOutput')
fold: user.vscode('notebook.fold')
unfold: user.vscode('notebook.unfold')
interrupt: user.vscode('notebook.cancelExecution')
go failed: user.vscode('notebook.revealLastFailedCell')
clear cell output: user.vscode('notebook.cell.clearOutputs.')

equal: ' = '