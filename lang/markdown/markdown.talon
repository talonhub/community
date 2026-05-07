code.language: markdown
-

(level | heading | header) one:
    edit.line_start()
    insert("# ")
(level | heading | header) two:
    edit.line_start()
    insert("## ")
(level | heading | header) three:
    edit.line_start()
    insert("### ")
(level | heading | header) four:
    edit.line_start()
    insert("#### ")
(level | heading | header) five:
    edit.line_start()
    insert("##### ")
(level | heading | header) six:
    edit.line_start()
    insert("###### ")

list [one]:
    edit.line_start()
    insert("- ")
list two:
    edit.line_start()
    insert("    - ")
list three:
    edit.line_start()
    insert("        - ")
list four:
    edit.line_start()
    insert("            - ")
list five:
    edit.line_start()
    insert("                - ")
list six:
    edit.line_start()
    insert("                    - ")

{user.markdown_code_block_language} block:
    user.insert_snippet("```{markdown_code_block_language}\n$0\n```")

link: user.insert_snippet_by_name("link")
