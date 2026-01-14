graph commit [<user.text>]:
    insert("gt modify -c -m \"")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))
    insert("\"")
    key("left")

graph create [<user.text>]:
    insert("gt create -m \"")
    insert(user.formatted_text(text or "", "CAPITALIZE_FIRST_WORD"))
    insert("\"")
    key("left")

graph modify and submit:
    insert("gt modify && gt submit --stack")

graph {user.graphite}:
    insert("gt {graphite}")
