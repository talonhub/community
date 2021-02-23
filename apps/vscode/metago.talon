app: vscode
-

take line up: user.vscode("metaGo.selectLineUp")
take line: user.vscode("metaGo.selectLineDown")

bracket switch: user.vscode("metaGo.changeSurroundingPair")

# jump to: user.vscode("metaGo.gotoSmart")
# jump word <word>: user.jump("metaGo.gotoSmart", word)
jerry: user.vscode("metaGo.gotoBefore")
josie: user.vscode("metaGo.gotoAfter")
jump block up: user.vscode("metaGo.gotoEmptyLineUp")
jump block [down]: user.vscode("metaGo.gotoEmptyLineDown")
jump bracket: user.vscode("metaGo.jumpToBracket")
jump very:
    key(cmd-shift-. enter)

# take to: user.vscode("metaGo.selectSmart")
tasty: user.vscode("metaGo.selectBefore")
toasty: user.vscode("metaGo.selectAfter")
take block up: user.vscode("metaGo.selectEmptyLineUp")
take block [down]: user.vscode("metaGo.selectEmptyLineDown")
take outer: user.vscode("metaGo.inSurroundingPairSelectionWithPairs")
take inner <user.symbol_key>:
    user.vscode("metaGo.inSurroundingPairSelection")
    key(symbol_key)
    sleep(7ms)

cursor add: user.vscode("metaGo.addCursorSmart")
cursor add before: user.vscode("metaGo.addCursorBefore")
cursor add after: user.vscode("metaGo.addCursorAfter")

actop: user.vscode("metaGo.scrollCurrentLineToTop")
acteen: user.vscode("metaGo.scrollCurrentLineToMiddle")
actum: user.vscode("metaGo.scrollCurrentLineToBottom")

take rightest: user.vscode("metaGo.cursorSpaceWordRightSelect")
take leftest: user.vscode("metaGo.cursorSpaceWordLeftSelect")
kitest: user.vscode("metaGo.cursorSpaceWordRight")
klavest: user.vscode("metaGo.cursorSpaceWordLeft")

swap anchor: user.vscode("metaGo.selectionSwitchActiveWithAnchor")