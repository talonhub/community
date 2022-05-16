os: windows
app: visual_studio
tag: user.csharp
-

def for each: "foreach"
op lambda: user.code_operator_lambda()

insert property:
    insert("prop")
    key(alt-t)
    key(tab)
    key(tab)

insert get set: 
    insert(" {")
    insert(" get; set; }")

# throw [new] <user.text> exception: 
#     insert('throw new ')
#     insert(user.formatted_text(text, "PUBLIC_CAMEL_CASE"))
#     insert('();')
#     key(left)
#     key(left)

throw [new] {user.csharp_exceptions}: 
    insert('throw new ')
    insert(user.csharp_exceptions)
    insert('();')
    key(left)
    key(left)

[state] (int | integer | ant): "int"
state string: "string"



nameof [<user.text>]:
    insert('nameof(')
    insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))
    insert(')')