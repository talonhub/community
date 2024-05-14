# pick item from a dropdown
choose <number_small>: user.choose(number_small)
choose up <number_small>: user.choose_up(number_small)

# DEPRECATED
drop down <number_small>:
    user.deprecate_command("2024-05-13", "drop down", "choose")
drop down up <number_small>:
    user.deprecate_command("2024-05-13", "drop down up", "choose up")
