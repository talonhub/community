tag: user.bspwm
-

# e.g. "node focus right", "desktop swap next" "node move to desktop next follow"
<user.bspwm_action>: user.bspwm_command(bspwm_action)
# Swap verb and subject, more natural. e.g. "focus node right", "swap desktop next"
<user.bspwm_node_actions> {user.bspwm_node} [<user.bspwm_node_sel>]: user.bspwm_object_command(bspwm_node, bspwm_node_actions, bspwm_node_sel or "")
<user.bspwm_desktop_actions> {user.bspwm_desktop} [<user.bspwm_desktop_sel>]: user.bspwm_object_command(bspwm_desktop, bspwm_desktop_actions, bspwm_desktop_sel or "")
<user.bspwm_monitor_actions> {user.bspwm_monitor} [<user.bspwm_monitor_sel>]: user.bspwm_object_command(bspwm_monitor, bspwm_monitor_actions, bspwm_monitor_sel or "")

# Shorthand for quick focusing: "node right", "desktop next"
<user.bspwm_object> <user.bspwm_selector>: user.bspwm_object_command(bspwm_object, "--focus", bspwm_selector)
# Desktop is special/annoying because left=prev rather than west.
{user.bspwm_desktop} <user.bspwm_desktop_sel>: user.bspwm_object_command(bspwm_desktop, "--focus", bspwm_desktop_sel)

