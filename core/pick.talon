# select from a list with the keyboard
(pic | pick): key(return)
(pic | pick) <number_small>:
    key("down:{number_small - 1}")
    sleep(50ms)
    key(return)
(pic | pick) down <number_small>:
    key("down:{number_small}")
    sleep(50ms)
    key(return)
(pic | pick) up <number_small>:
    key("up:{number_small}")
    sleep(50ms)
    key(return)
