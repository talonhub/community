new line: "\n"
double dash: "--"
triple quote: "'''"
(triple grave | triple back tick | gravy): insert("```")
(dot dot | dotdot): ".."
ellipsis: "..."
(comma and | spamma): ", "
arrow: "->"
dub arrow: "=>"
empty dub string: user.insert_between('"', '"')
empty escaped (dub string | dub quotes): user.insert_between('\\"', '\\"')
empty string: user.insert_between("'", "'")
empty escaped string: user.insert_between("\\'", "\\'")
(inside (parens | round) | args): user.insert_between("(", ")")
inside (box | squares | brackets | square brackets | list): user.insert_between("[", "]")
inside (curly | braces | curly brackets): user.insert_between("{", "}")
inside percent: user.insert_between("%", "%")
inside (twin | quotes | string): user.insert_between("'", "'")
inside (quad | double quotes | dub quotes): user.insert_between('"', '"')
inside (skis | graves | back ticks): user.insert_between("`", "`")
inside diamond: user.insert_between("<", ">")
angle that:
    text = edit.selected_text()
    user.paste("<{text}>")
(square | bracket | square bracket) that:
    text = edit.selected_text()
    user.paste("[{text}]")
(brace | curly bracket) that:
    text = edit.selected_text()
    user.paste("{{{text}}}")
(parens | args) that:
    text = edit.selected_text()
    user.paste("({text})")
percent that:
    text = edit.selected_text()
    user.paste("%{text}%")
quote that:
    text = edit.selected_text()
    user.paste("'{text}'")
(double quote | dub quote) that:
    text = edit.selected_text()
    user.paste('"{text}"')
(grave | back tick) that:
    text = edit.selected_text()
    user.paste("`{text}`")
