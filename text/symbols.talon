questo: "?"
underbar: "_"
double dash: "--"
(curly | left curly): "{"
right curly: "}"
triple tick: "'''"
(dot dot | dotdot): ".."
ellipses: "..."
spamma: ", "
semi: ";" 
comma: ","  
spacey: " " 
quote: "\""
ticky: "'"
back tick: "`"
dollar: "$"     
dotty: "."
plus: "+"
minus: "-"
arrow: "->"
fat arrow: " => "
new line: "\\n"
carriage return: "\\r"
line feed: "\\r\\n"

empty escaped (dubstring|dub quotes):
    '\\"\\"'
    key(left)
    key(left)
empty escaped string:
    "\\'\\'"
    key(left)
    key(left)
(inside ticks | ticks):
    "''"
    key(left)
(inside back ticks | back ticks):
    "``"
    key(left)
(inside prekris | prekris):
	insert("()")
	key(left)
(inside squares | squares): 
	insert("[]") 
	key(left)
(inside curlys | curlys): 
	insert("{}") 
	key(left)
(inside percents | percents): 
	insert("%%") 
	key(left)
(inside quotes | quotes):
	insert('""')
	key(left)
(inside angles | angles):
	insert('<>')
	key(left)
hug angles: 
    text = edit.selected_text()
    user.paste("<{text}>")
hug curlys: 
    text = edit.selected_text()
    user.paste("{{{text}}}")
hug squares: 
    text = edit.selected_text()
    user.paste("[{text}]")
hug prekris: 
    text = edit.selected_text()
    user.paste("({text})")
hug percents: 
    text = edit.selected_text()
    user.paste("%{text}%")
hug quotes:
    text = edit.selected_text()
    user.paste('"{text}"')
hug ticks:
    text = edit.selected_text()
    user.paste("'{text}'")
hug back ticks:
    text = edit.selected_text()
    user.paste("`{text}`")

