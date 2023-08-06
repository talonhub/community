# -1 because we are repeating, so the initial command counts as one
<number_small>: core.repeat_command(number_small - 1)
^<number_small>: skip()
(repeat that | twice): core.repeat_command(1)
repeat that <number_small> [times]: core.repeat_command(number_small)

(repeat phrase | again) [<number_small> times]:
    core.repeat_partial_phrase(number_small or 1)
