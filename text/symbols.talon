
questo: "?"
underbar: "_"
sunder: "__"
double dash: "--"
(curly | open curly): "{"
close curly: "}"
triple tick: "'''"
ellipses: "..."
skipper: ", "
semi coal: ";"
coal gap: ": "
comma: ","  
gap: " " 
quote: "\""
ticky: "'"
back tick: "`"
dollar: "$"     
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
(inside ticks | inside tickys | ticks | tickys):
    "''"
    key(left)
(inside back ticks | inside back tickys | back ticks | back tickys):
    "``"
    key(left)
(inside parens | parens):
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
hug parens: 
    text = edit.selected_text()
    user.paste("({text})")
hug percents: 
    text = edit.selected_text()
    user.paste("%{text}%")
hug quotes:
    text = edit.selected_text()
    user.paste("'{text}'")
(double quote | dubquote) that:
    text = edit.selected_text()
    user.paste('"{text}"')
(hug ticks | hug tickys):
    text = edit.selected_text()
    user.paste("'{text}'")
(hug back ticks | hug back tickys):
    text = edit.selected_text()
    user.paste("`{text}`")

