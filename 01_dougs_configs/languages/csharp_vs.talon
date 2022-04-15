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

[state] (int | integer | ant): "int"
state string: "string"

insert get set: 
    insert(" {")
    insert(" get; set; }")