app: vscode
-

# <user.select> line up: user.vscode("metaGo.selectLineUp")
# <user.select> line: user.vscode("metaGo.selectLineDown")

bracket switch: user.vscode("metaGo.changeSurroundingPair")

# <user.teleport> to: user.vscode("metaGo.gotoSmart")
# <user.teleport> word <word>: user.jump("metaGo.gotoSmart", word)
# <user.select> before: user.vscode("metaGo.gotoBefore")
# <user.select> after: user.vscode("metaGo.gotoAfter")
razor: user.vscode("metaGo.gotoEmptyLineUp")
dropper: user.vscode("metaGo.gotoEmptyLineDown")
# <user.teleport> bracket: user.vscode("metaGo.jumpToBracket")
# <user.teleport> very:
#     key(cmd-shift-. enter)

# <user.select> to: user.vscode("metaGo.selectSmart")
# tasty: user.vscode("metaGo.selectBefore")
# toasty: user.vscode("metaGo.selectAfter")
<user.select> upper: user.vscode("metaGo.selectEmptyLineUp")
<user.select> downer: user.vscode("metaGo.selectEmptyLineDown")
<user.delete> downer:
    user.vscode("metaGo.selectEmptyLineDown")
    key(backspace)
<user.delete> upper:
    user.vscode("metaGo.selectEmptyLineUp")
    key(backspace)
# <user.select> outside: user.vscode("metaGo.inSurroundingPairSelectionWithPairs")
# <user.select> inside <user.symbol_key>:
#     user.vscode("metaGo.inSurroundingPairSelection")
#     key(symbol_key)
#     sleep(25ms)

# cursor add: user.vscode("metaGo.addCursorSmart")
# cursor add before: user.vscode("metaGo.addCursorBefore")
# cursor add after: user.vscode("metaGo.addCursorAfter")

act up: user.vscode("metaGo.scrollCurrentLineToTop")
act eat: user.vscode("metaGo.scrollCurrentLineToMiddle")
act down: user.vscode("metaGo.scrollCurrentLineToBottom")

<user.select> right big: user.vscode("metaGo.cursorSpaceWordRightSelect")
<user.select> left big: user.vscode("metaGo.cursorSpaceWordLeftSelect")
tug big: user.vscode("metaGo.cursorSpaceWordLeft")
push big: user.vscode("metaGo.cursorSpaceWordRight")

swap anchor: user.vscode("metaGo.selectionSwitchActiveWithAnchor")