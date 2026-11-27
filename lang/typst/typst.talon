code.language: typst
-

tag(): user.code_comment_line
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions

(level | heading | header) one:
    edit.line_start()
    insert("= ")

(level | heading | header) two:
    edit.line_start()
    insert("== ")

(level | heading | header) three:
    edit.line_start()
    insert("=== ")

(level | heading | header) four:
    edit.line_start()
    insert("==== ")

(level | heading | header) five:
    edit.line_start()
    insert("===== ")

(level | heading | header) six:
    edit.line_start()
    insert("====== ")

list (bullet | one):
    edit.line_start()
    insert("- ")

list two:
    edit.line_start()
    insert("  - ")

list (number | numbered):
    edit.line_start()
    insert("+ ")

code block: user.insert_snippet("```$1\n$0\n```")

math block: user.insert_snippet("$ $0 $")

label <user.text>: insert("<{text}>")

ref <user.text>: insert("@{text}")

code mode: user.insert_snippet("#($0)")

markup mode: user.insert_snippet("[$0]")

bold: user.insert_snippet("*$0*")
italic: user.insert_snippet("_$0_")
mono: user.insert_snippet("`$0`")
link: user.insert_snippet_by_name("link")
figure: user.insert_snippet_by_name("figure")
table: user.insert_snippet_by_name("table")
quote: user.insert_snippet_by_name("quote")
highlight: user.insert_snippet_by_name("highlight")
underline: user.insert_snippet_by_name("underline")
strike: user.insert_snippet_by_name("strike")
footnote: user.insert_snippet_by_name("footnote")

function definition: user.insert_snippet_by_name("functionDeclaration")
show set rule: user.insert_snippet_by_name("show set rule")
show rule: user.insert_snippet_by_name("show rule")
set rule: user.insert_snippet_by_name("set rule")
place: user.insert_snippet_by_name("place")
