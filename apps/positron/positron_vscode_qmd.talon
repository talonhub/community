# Adding Quarto Markdown Support For Positron and VSCode
app.bundle: vscode
app.bundle: positron
win.file_ext: .qmd
-

# Quarto Markdown
cell next: user.vscode("quarto.goToNextCell")
cell (previous | last): user.vscode("quarto.goToPreviousCell")
notebook run head: user.vscode("quarto.runCellsAbove")
notebook run tail: user.vscode("quarto.runCellsBelow")
cellbrun here: user.vscode("quarto.runCurrentCell")
cell run: user.vscode("quarto.runCurrentAdvance")
cell run next: user.vscode("quarto.runNextCell")
cell run last: user.vscode("quarto.runPreviousCell")
run [that]: user.vscode("quarto.runCurrent")
notebook run: user.vscode("quarto.runAllCells")
cell new: user.vscode("quarto.insertCodeCell")
[quarto] preview: user.vscode("quarto.previewScript")

go to [<user.text>]:
    user.vscode("workbench.action.gotoSymbol")
    insert(text)
