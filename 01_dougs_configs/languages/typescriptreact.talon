tag: user.typescriptreact
-
tag(): user.typescript
tag(): user.css


element div: 
    insert("<div")
    insert(">")

element span: 
    insert("<span")
    insert(">")

element <user.text>:
    insert("<")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
    insert(">")

element self close <user.text>:
    insert("<")
    insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
    insert("/>")