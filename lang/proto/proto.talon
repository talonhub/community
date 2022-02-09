mode: command
and mode: user.protobuf
mode: command
and mode: user.auto_lang
and code.language: protobuf
-

state message: "message "
state package: "package "
state reserved: "reserved "
state enum: "enum "
op equals: " = "
state import: "import "
state import public: "import public "
state option: "option "
state repeated: "repeated "

<user.code_insert_type>$:
    insert("{code_insert_type}")
