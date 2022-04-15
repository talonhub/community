app: vscode
mode: command
mode: user.vue
mode: user.auto_lang
and code.language: vue
app: vscode
-
tag(): user.javascript
tag(): user.typescript

insert vue brackets:
    key("delete")
    insert("{")
    insert("{  ")
    insert("}")
    insert("}")
    key("left")
    key("left")
    key("left")

insert vue for: 
    insert("v-for=\"\"")
    key("left")
insert vue if:
    insert("v-if=\"\"")
    key("left")
insert vue else: "v-else"
