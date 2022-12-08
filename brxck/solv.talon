link onion <number>:
    insert("https://solvhealth.atlassian.net/browse/ONION-{number}")

short onion <number>: insert("ONION-{number}")

mark onion <number>:
    insert("[ONION-{number}](https://solvhealth.atlassian.net/browse/ONION-{number})")

open onion <number>:
    user.open_url("https://solvhealth.atlassian.net/browse/ONION-{number}")

open repo {user.solv_repository}:
    user.open_url("https://github.com/solvhealth/{user.solv_repository}")

botler {user.botler_command} {user.solv_repository}:
    insert("@BOTler {botler_command} {user.solv_repository}")
