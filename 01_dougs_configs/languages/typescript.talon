app: vscode
mode: command
mode: user.typescript
mode: user.auto_lang
and code.language: typescript
-
tag(): user.javascript

(type | typed) as boolean: ": boolean"
(type | typed) as number: ": number"
(type | typed) as string: ": string"
(type | typed) as null: ": null"

state private [<user.text>]:
    insert("private ")
    insert(user.text or "")

state type: "type "

(type | typed) as record:
    insert(": Record<>")
    key(left)

(type | typed) as <user.format_text>:
    insert(": ")
    insert(format_text)


# SNIPPETS

insert throw error:
    user.vscode("editor.action.insertSnippet")
    insert("ts-throw-error")
    sleep(50ms)
    key("enter")

insert field:
    user.vscode("editor.action.insertSnippet")
    insert("ts-field")
    sleep(50ms)
    key("enter")

insert record field:
    user.vscode("editor.action.insertSnippet")
    insert("ts-record-field")
    sleep(50ms)
    key("enter")

insert method:
    user.vscode("editor.action.insertSnippet")
    insert("ts-method")
    sleep(50ms)
    key("enter")

insert getter:
    user.vscode("editor.action.insertSnippet")
    insert("ts-getter")
    sleep(50ms)
    key("enter")

insert setter:
    user.vscode("editor.action.insertSnippet")
    insert("ts-setter")
    sleep(50ms)
    key("enter")

insert private field:
    user.vscode("editor.action.insertSnippet")
    insert("ts-private-field")
    sleep(50ms)
    key("enter")

insert private record:
    user.vscode("editor.action.insertSnippet")
    insert("ts-private-record")
    sleep(50ms)
    key("enter")