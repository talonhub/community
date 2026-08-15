# Adding Quarto Markdown Support For Positron and VSCode
app: vscode
app: positron
win.file_ext: .qmd
-

# Quarto Markdown
cell <user.spatial_previous_next>: user.vscode_go(spatial_previous_next, "quarto.goToPreviousCell", "quarto.goToNextCell")
notebook run head: user.vscode("quarto.runCellsAbove")
notebook run tail: user.vscode("quarto.runCellsBelow")
cellbrun here: user.vscode("quarto.runCurrentCell")
cell run: user.vscode("quarto.runCurrentAdvance")
cell run <user.spatial_previous_next>: user.vscode_go(spatial_previous_next, "quarto.runPreviousCell", "quarto.runNextCell")
run [that]: user.vscode("quarto.runCurrent")
notebook run: user.vscode("quarto.runAllCells")
cell new: user.vscode("quarto.insertCodeCell")
[quarto] preview: user.vscode("quarto.previewScript")

go to [<user.text>]:
    user.vscode("workbench.action.gotoSymbol")
    insert(text)
