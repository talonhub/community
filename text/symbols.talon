question [mark]: "?"
(downscore | underscore): "_"
# double dash: "--"
(bracket | left bracket): "{"
(are bracket | right bracket): "}"
triple quote: "'''"
(triple back tick):
    insert("```")
semi end: ";;"
# (dot dot | dotdot): ".."
ellipses: "..."
(comma and | spamma): ", "
plus: "+"
# arrow: "->"
# dub arrow: "=>"
new line: "\\n"
carriage return: "\\r"
line feed: "\\r\\n"
empty dubstring:
    '""'
    key(left)
empty escaped (dubstring|dub quotes):
    '\\"\\"'
    key(left)
    key(left)
empty string:
    "''"
    key(left)
empty escaped string:
    "\\'\\'"
    key(left)
    key(left)
# (inside parens | args):
# 	insert("()")
# 	key(left)
inside (squares | square brackets | list):
	insert("[]")
	key(left)
inside (bracket | braces):
	insert("{}")
	key(left)
inside percent:
	insert("%%")
	key(left)
inside (quotes | string):
	insert("''")
	key(left)
inside (double quotes | dubquotes):
    insert('""')
	key(left)
inside (back ticks):
	insert("``")
	key(left)
angle that:
    text = edit.selected_text()
    user.paste("<{text}>")
(square | square bracket) that:
    text = edit.selected_text()
    user.paste("[{text}]")
(bracket | brace) that:
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
(double quote | dubquote) that:
    text = edit.selected_text()
    user.paste('"{text}"')
(back tick) that:
    text = edit.selected_text()
    user.paste('`{text}`')
