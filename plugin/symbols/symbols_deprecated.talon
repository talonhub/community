empty dub string:
    user.deprecate_command("2024-11-24", "empty dub string", "quad")
    user.insert_between('"', '"')

empty escaped (dub string | dub quotes):
    user.deprecate_command("2024-11-24", "empty escaped (dub string | dub quotes)", "escaped quad")
    user.insert_between('\\"', '\\"')

empty string:
    user.deprecate_command("2024-11-24", "empty string", "twin")
    user.insert_between("'", "'")

empty escaped string:
    user.deprecate_command("2024-11-24", "empty escaped string", "escaped twin")
    user.insert_between("\\'", "\\'")

inside (parens | args):
    user.deprecate_command("2024-11-24", "inside (parens | args)", "round")
    user.insert_between("(", ")")

inside (squares | brackets | square brackets | list):
    user.deprecate_command("2024-11-24", "inside (squares | brackets | square brackets | list)", "box")
    user.insert_between("[", "]")

inside (braces | curly brackets):
    user.deprecate_command("2024-11-24", "inside (braces | curly brackets)", "curly")
    user.insert_between("{", "}")

inside percent:
    user.deprecate_command("2024-11-24", "inside percent", "percentages")
    user.insert_between("%", "%")

inside (quotes | string):
    user.deprecate_command("2024-11-24", "inside (quotes | string)", "twin")
    user.insert_between("'", "'")

inside (double quotes | dub quotes):
    user.deprecate_command("2024-11-24", "inside (double quotes | dub quotes)", "quad")
    user.insert_between('"', '"')

inside (graves | back ticks):
    user.deprecate_command("2024-11-24", "inside (graves | back ticks)", "skis")
    user.insert_between("`", "`")

angle that:
    user.deprecate_command("2024-11-24", "angle that", "diamond that")
    text = edit.selected_text()
    user.paste("<{text}>")

(square | bracket | square bracket) that:
    user.deprecate_command("2024-11-24", "(square | bracket | square bracket) that", "box that")
    text = edit.selected_text()
    user.paste("[{text}]")

(brace | curly bracket) that:
    user.deprecate_command("2024-11-24", "(brace | curly bracket) that", "curly that")
    text = edit.selected_text()
    user.paste("{{{text}}}")

(parens | args) that:
    user.deprecate_command("2024-11-24", "(parens | args) that", "round that")
    text = edit.selected_text()
    user.paste("({text})")

percent that:
    user.deprecate_command("2024-11-24", "percent that", "percentages that")
    text = edit.selected_text()
    user.paste("%{text}%")

quote that:
    user.deprecate_command("2024-11-24", "quote that", "twin that")
    text = edit.selected_text()
    user.paste("'{text}'")

(double quote | dub quote) that:
    user.deprecate_command("2024-11-24", "(double quote | dub quote) that", "quad that")
    text = edit.selected_text()
    user.paste('"{text}"')

(grave | back tick) that:
    user.deprecate_command("2024-11-24", "(grave | back tick) that", "skis that")
    text = edit.selected_text()
    user.paste("`{text}`")
