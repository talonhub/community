tag: user.bspwm
-

# e.g. "node focus right", "desktop swap next"
<user.bspwm_domain> <user.bspwm_command> <user.bspwm_selector>:
    user.bspwm_command(bspwm_domain, bspwm_selector, bspwm_command)
# Swap verb and subject, more natural. e.g. "node focus right", "desktop swap next"
<user.bspwm_command> <user.bspwm_domain> <user.bspwm_selector>:
    user.bspwm_command(bspwm_domain, bspwm_selector, bspwm_command)

# Shorthand for faster focus switching
<user.bspwm_domain> <user.bspwm_selector>:
    user.bspwm_command(bspwm_domain, bspwm_selector, "--focus")

<user.bspwm_domain> <user.bspwm_desktop_selector> state <user.bspwm_state>:
    user.bspwm_state_command(bspwm_domain, bspwm_desktop_selector, bspwm_state)

<user.bspwm_domain> <user.bspwm_node_selector> flag <user.bspwm_flag>:
    user.bspwm_flag_command(bspwm_domain, bspwm_node_selector, bspwm_flag)

<user.bspwm_domain> <user.bspwm_desktop_selector> flag <user.bspwm_flag>:
    user.bspwm_flag_command(bspwm_domain, bspwm_desktop_selector, bspwm_flag)
