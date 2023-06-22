tag: user.markdown
-
(level | heading | header) one:
    edit.line_start()
    "# "
(level | heading | header) two:
    edit.line_start()
    "## "
(level | heading | header) three:
    edit.line_start()
    "### "
(level | heading | header) four:
    edit.line_start()
    "#### "
(level | heading | header) five:
    edit.line_start()
    "##### "
(level | heading | header) six:
    edit.line_start()
    "###### "

list [one]:
    edit.line_start()
    "- "
list two:
    edit.line_start()
    "    - "
list three:
    edit.line_start()
    "        - "
list four:
    edit.line_start()
    "            - "
list five:
    edit.line_start()
    "                - "
list six:
    edit.line_start()
    "                    - "

{user.markdown_code_block_language} block:
    "```{markdown_code_block_language}"
    key(enter:2)
    "```"
    key(up)

link:
    "[]()"
    key(left:3)
