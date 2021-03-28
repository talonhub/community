app: vscode
-
<user.select> [{user.symbol_color}] <user.any_alphanumeric_key>:
	user.vscode_and_wait("decorative-navigation.selectToken", symbol_color or "default", any_alphanumeric_key)
	sleep(50ms)

<user.teleport> [{user.symbol_color}] <user.any_alphanumeric_key>:
	user.vscode("decorative-navigation.selectToken", symbol_color or "default", any_alphanumeric_key)
	key(left)

def show [{user.symbol_color}] <user.any_alphanumeric_key>:
	user.vscode("decorative-navigation.selectToken", symbol_color or "default", any_alphanumeric_key)
	user.vscode("editor.action.revealDefinition")

action(user.dental_click): user.vscode("decorative-navigation.toggleDecorations")