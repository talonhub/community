link onion <number>:
  insert("https://solvhealth.atlassian.net/browse/ONION-{number}")

short onion <number>:
  insert("ONION-{number}")

mark onion <number>:
  insert("[ONION-{number}](https://solvhealth.atlassian.net/browse/ONION-{number})")

open onion <number>:
  user.open_url("https://solvhealth.atlassian.net/browse/ONION-{number}")

open repo {user.solv_repositories}:
  user.open_url("https://github.com/solvhealth/{user.solv_repositories}")

botler {user.botler_commands} {user.solv_repositories}:
  insert("@BOTler {user.botler_commands} {user.solv_repositories}")

botler {user.botler_commands} {user.solv_repositories} force:
  insert("@BOTler {user.botler_commands} {user.solv_repositories} -f")
