code.language: typescript
code.language: typescriptreact
-

type union [<user.code_type>]: " | {code_type or ''}"
type intersect [<user.code_type>]: " & {code_type or ''}"

state type: user.insert_between("type ", " = ")

as const: " as const"
