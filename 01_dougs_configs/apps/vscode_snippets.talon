
app: vscode
mode: command
-

insert if:
    user.vscode("editor.action.insertSnippet")
    insert("if statement")
    key("enter")

insert for loop:
    user.vscode("editor.action.insertSnippet")
    insert("for loop")
    key("enter")

insert function:
    user.vscode("editor.action.insertSnippet")
    insert("function")
    key("enter")

null coalesce: " ?? "