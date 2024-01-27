not tag: user.disable_unprefixed_numbers
-
<user.number_string>:
    insert("{number_string}")
    user.deprecate_command("2024-01-27", "unprefixed <user.number_string>", "prefixed <user.number_string>")
