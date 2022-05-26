tag: user.css
-
tag(): user.code_comment_block_c_like
tag(): user.code_functions_common
tag(): user.code_libraries
tag(): user.code_operators_math

settings():
    user.code_public_variable_formatter = "DASH_SEPARATED"

block: user.code_block()

attribute [<user.text>]:
    name = user.formatted_text(text or "", "DASH_SEPARATED")
    user.insert_between("[{name}", "]")

prop <user.text>:
    name = user.formatted_text(text, "DASH_SEPARATED")
    user.insert_between("{name}: ", ";")

# for media/supports queries, or if you don't like prop
rule <user.text>:
    name = user.formatted_text(text, "DASH_SEPARATED")
    insert("{name}: ")

value <user.number_string> [{user.css_unit}]:
    "{number_string}{css_unit or ''}"
value <user.number_string> point <digit_string> [{user.css_unit}]:
    "{number_string}.{digit_string}{css_unit or ''}"

(value|state) {user.css_global_value}: "{css_global_value}"
value <user.text>: user.insert_formatted(text, "DASH_SEPARATED")

variable <user.text>:
    name = user.formatted_text(text, settings.get("user.code_public_variable_formatter"))
    insert("var(--{name})")

op var: user.insert_between("var(--", ")")

at {user.css_at_rule}: "@{css_at_rule} "
unit {user.css_unit}: insert(css_unit)

[value] current color: "currentColor"
op important: " !important"
