#Adding Positron commands, building on Nicolas Riley's personal repo
app: positron
-
notebook new: user.vscode("quarto.newNotebook")
quarto new: user.vscode("quarto.fileNewDocument")

panel console: user.vscode("workbench.action.positronConsole.focusConsole")

sec (viewer | preview): user.vscode("workbench.panel.positronPreview.focus")
sec help: user.vscode("workbench.panel.positronHelp.focus")
sec variables: user.vscode("positronVariables.focus")
sec plots: user.vscode("workbench.panel.positronPlots.focus")

help that: user.vscode("positron.help.showHelpAtCursor")

#Plot Commands

plot copy: user.vscode("workbench.action.positronPlots.copy")
plot clear: user.vscode("workbench.action.positronPlots.clear")
plot open: user.vscode("workbench.action.positronPlots.openEditor")
plot refresh: user.vscode("workbench.action.positronPlots.refresh")
plot next: user.vscode("workbench.action.positronPlots.next")
plot (previous | last): user.vscode("workbench.action.positronPlots.previous")
plot toggle: user.vscode("workbench.action.positron.togglePlots")
