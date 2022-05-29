tag: browser
-
click <user.letters>: user.rango_click_hint(letters)
blank <user.letters>: user.rango_open_in_new_tab(letters)
copy link <user.letters>: user.rango_copy_link(letters)
show <user.letters>: user.rango_show_link(letters)
hover <user.letters>: user.rango_hover_hint(letters)
hover fix <user.letters>: user.rango_fixed_hover_hint(letters)
dismiss: user.rango_unhover()
hint bigger: user.rango_increase_hint_size()
hint smaller: user.rango_decrease_hint_size()
hints toggle: user.rango_toggle_hints()

rango explicit:  user.rango_disable_direct_clicking()
rango direct:  user.rango_enable_direct_clicking()