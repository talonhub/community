mode: all
app: vscode
-

^lets think$:
  user.vscode("cursorless.toggleDecorations")
  speech.disable()

^got it$:
  user.vscode("cursorless.toggleDecorations")
  speech.enable()
