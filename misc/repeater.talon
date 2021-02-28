# -1 because we are repeating, so the initial command counts as one
<number> now: core.repeat_command(number-1)
twice: core.repeat_command(1)
(repeat that|again): core.repeat_phrase(1)
repeat that <number_small> [times]: core.repeat_phrase(number_small)
