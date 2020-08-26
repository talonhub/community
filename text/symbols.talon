question [mark]: "?"
(downscore | underscore): "_"
double dash: "--"
(bracket | brack | left bracket): "{"
(rbrack | are bracket | right bracket): "}"
triple quote: "'''"
(dot dot | dotdot): ".."
#ellipses: "…"
ellipses: "..."
(comma and | spamma): ", "
plus: "+"
arrow: "->"
dub arrow: "=>"
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
(inside parens | args):
	insert("()")
	key(left)
inside (squares | list): 
	insert("[]") 
	key(left)
inside (bracket | braces): 
	insert("{}") 
	key(left)
inside percent: 
	insert("%%") 
	key(left)
inside quotes:
	insert('""')
	key(left)
angle this: 
    old_clip = clip.text()
    edit.copy()
	sleep(100ms)
	text = clip.text()
	insert("<{text}>")
	clip.set_text(old_clip)
(bracket | brace) this: 
    old_clip = clip.text()
    edit.copy()
	sleep(100ms)
	text = clip.text()
	clip.set_text("{{{text}}}")
	edit.paste()
	clip.set_text(old_clip)
(parens | args) this: 
    old_clip = clip.text()
    edit.copy()
	sleep(100ms)
	text = clip.text()
	clip.set_text("({text})")
	edit.paste()
	clip.set_text(old_clip)
percent this: 
    old_clip = clip.text()
    edit.copy()
	sleep(100ms)
	text = clip.text()
	clip.set_text("%{text}%")
	edit.paste()
	clip.set_text(old_clip)
quote this:
    old_clip = clip.text()
    edit.copy()
	sleep(100ms)
	text = clip.text()
	clip.set_text('"{text}"')
	edit.paste()
	clip.set_text(old_clip)