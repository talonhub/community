mode: all
speech.engine: dragon
-
# The optional <phrase> afterwards allows these to match even if you say arbitrary text
# after this command, without having to wait for the speech timeout.

# This is handy because you often need to put Talon asleep in order to immediately
# talk to humans, and it's annoying to have to say "sleep all", wait for the timeout,
# and then resume your conversation.

# With this, you can say "sleep all hey bob" and Talon will immediately go to
# sleep and ignore "hey bob". Note that subtitles will show "sleep all hey bob",
# because it's part of the rule definition, but "hey bob" will be ignored, because
# we don't do anything with the <phrase> in the body of the command.
^talon sleep [<phrase>]$: speech.disable()
^talon wake [<phrase>]$: speech.enable()

^sleep all [<phrase>]$:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.dragon_engine_sleep()
