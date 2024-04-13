code.language: protobuf
-
tag(): user.code_block_c_like

# this is pretty bare-bones, further contributions welcome
block: user.code_block()

state message: "message "
state package: "package "
state reserved: "reserved "
state enum: "enum "
op equals: " = "
state import: "import "
state import public: "import public "
state option: "option "
state repeated: "repeated "

type {user.code_type}: "{code_type}"
repeated type {user.code_type}: "repeated {code_type}"
