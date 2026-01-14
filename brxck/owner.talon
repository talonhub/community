link rez <number>:
    insert("https://linear.app/owner/issue/res-{number}")

short rez <number>: insert("RES-{number}")

mark rez <number>:
    insert("[RES-{number}](https://linear.app/owner/issue/res-{number})")

open rez <number>:
    user.open_url("https://linear.app/owner/issue/res-{number}")

branch rez <number> <user.text>:
    insert("res-{number}-")
    user.insert_formatted(text, "DASH_SEPARATED")

branch <user.text> rez <number>:
    insert("res-{number}-")
    user.insert_formatted(text, "DASH_SEPARATED")
