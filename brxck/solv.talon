link message <number>:
    insert("https://linear.app/solv/issue/msg-{number}")

short message <number>: insert("MSG-{number}")

mark message <number>:
    insert("[MSG-{number}](https://linear.app/solv/issue/msg-{number})")

open message <number>:
    user.open_url("https://linear.app/solv/issue/msg-{number}")

branch message <number> <user.text>:
    insert("msg-{number}-")
    user.insert_formatted(text, "DASH_SEPARATED")

branch <user.text> message <number>:
    insert("msg-{number}-")
    user.insert_formatted(text, "DASH_SEPARATED")

open repo {user.solv_repository}:
    user.open_url("https://github.com/solvhealth/{user.solv_repository}")

botler {user.botler_command} {user.solv_repository}:
    insert("@BOTler {botler_command} {user.solv_repository}")

{user.linear_keyword} message <number>:
    user.insert_formatted(linear_keyword, "CAPITALIZE_FIRST_WORD")
    insert(" MSG-{number}")
