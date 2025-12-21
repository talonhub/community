tag: browser
and not tag: user.rango_disabled
-
tag(): user.rango_direct_clicking
tag(): user.rango_number_hints

# Click
click <user.rango_target>: user.rango_click_element(rango_target)

# Mouse click and move
mouse click <user.rango_target>: user.rango_mouse_click_element(rango_target, 0)
menu <user.rango_target>: user.rango_mouse_click_element(rango_target, 1)
move to <user.rango_target>: user.rango_mouse_move_to_element(rango_target)

# Focus
focus <user.rango_target>: user.rango_focus_element(rango_target)

# Focus click element
flick <user.rango_target>: user.rango_focus_and_activate_element(rango_target)

go input: user.rango_focus_first_input()

# Focus tab
(go tab | slot) <user.rango_tab_target>: user.rango_activate_tab(rango_tab_target)
[tab] marker refresh: user.rango_refresh_tab_markers()

# Focus tab with audio
go sound: user.rango_focus_next_tab_with_sound()
go playing: user.rango_focus_next_audible_tab()
go muted: user.rango_focus_next_muted_tab()
go last sound: user.rango_focus_tab_last_sounded()

# Mute tabs
mute this: user.rango_mute_current_tab()
unmute this: user.rango_unmute_current_tab()
mute next: user.rango_mute_next_tab_with_sound()
unmute next: user.rango_unmute_next_muted_tab()
mute <user.rango_tab_target>: user.rango_mute_tab(rango_tab_target)
unmute <user.rango_tab_target>: user.rango_unmute_tab(rango_tab_target)
mute all: user.rango_mute_all_tabs_with_sound()
unmute all: user.rango_unmute_all_muted_tabs()

# Close tab
tab close <user.rango_tab_target>: user.rango_close_tab(rango_tab_target)

# Open in a new tab
blank <user.rango_target>: user.rango_open_in_new_tab(rango_target)
stash <user.rango_target>: user.rango_open_in_background_tab(rango_target)

# Navigation
go root: user.rango_navigate_to_page_root()
page next: user.rango_navigate_to_next_page()
page last: user.rango_navigate_to_previous_page()

# Move current tab to a new window
tab split: user.rango_move_tab_to_new_window()

# Focus previous tab
tab back: user.rango_focus_previous_tab()

# Focus or create tab from your `talonhub/community` websites.csv
visit {user.website}: user.rango_focus_or_create_tab_by_url(website)

# Focus tab by text
tab hunt <user.text>: user.rango_focus_tab_by_text(text)
tab ahead: user.rango_cycle_tabs_by_text(1)
tab behind: user.rango_cycle_tabs_by_text(-1)

# Close tabs
tab close other: user.rango_close_other_tabs()
tab close left: user.rango_close_tabs_to_left()
tab close right: user.rango_close_tabs_to_right()
tab close first [<number_small>]: user.rango_close_tabs_left_end(number_small or 1)
tab close final [<number_small>]: user.rango_close_tabs_right_end(number_small or 1)
tab close previous [<number_small>]: user.rango_close_previous_tabs(number_small or 1)
tab close next [<number_small>]: user.rango_close_next_tabs(number_small or 1)

# Clone tab
tab clone: user.rango_clone_current_tab()

# Hover
hover <user.rango_target>: user.rango_hover_element(rango_target)
dismiss: user.rango_unhover_all()

# Show link address
show <user.rango_target>: user.rango_show_link(rango_target)

# Hide hint
hide <user.rango_target>: user.rango_hide_hint(rango_target)

# Scroll
upper: user.rango_scroll("main", "up")
upper <number_small>: user.rango_scroll("main", "up", number_small)
upper all: user.rango_scroll("main", "up", 9999)
tiny up: user.rango_scroll("main", "up", 0.2)

downer: user.rango_scroll("main", "down")
downer <number_small>: user.rango_scroll("main", "down", number_small)
downer all: user.rango_scroll("main", "down", 9999)
tiny down: user.rango_scroll("main", "down", 0.2)

scroll left: user.rango_scroll("main", "left")
scroll left all: user.rango_scroll("main", "left", 9999)
tiny left: user.rango_scroll("main", "left", 0.2)

scroll right: user.rango_scroll("main", "right")
scroll right all: user.rango_scroll("main", "right", 9999)
tiny right: user.rango_scroll("main", "right", 0.2)

# Scroll the left or right sidebars
upper left: user.rango_scroll("leftSidebar", "up")
upper left all: user.rango_scroll("leftSidebar", "up", 9999)

downer left: user.rango_scroll("leftSidebar", "down")
downer left all: user.rango_scroll("leftSidebar", "down", 9999)

upper right: user.rango_scroll("rightSidebar", "up")
upper right all: user.rango_scroll("rightSidebar", "up", 9999)

downer right: user.rango_scroll("rightSidebar", "down")
downer right all: user.rango_scroll("rightSidebar", "down", 9999)

# Scroll at element
upper <user.rango_target>: user.rango_scroll_at_element(rango_target, "up")
tiny up <user.rango_target>: user.rango_scroll_at_element(rango_target, "up", 0.2)

downer <user.rango_target>: user.rango_scroll_at_element(rango_target, "down")
tiny down <user.rango_target>: user.rango_scroll_at_element(rango_target, "down", 0.2)

scroll left <user.rango_target>: user.rango_scroll_at_element(rango_target, "left")
tiny left <user.rango_target>: user.rango_scroll_at_element(rango_target, "left", 0.1)

scroll right <user.rango_target>: user.rango_scroll_at_element(rango_target, "right")
tiny right <user.rango_target>: user.rango_scroll_at_element(rango_target, "right", 0.1)

# Repeat previous scroll
up again: user.rango_scroll("repeatLast", "up")
down again: user.rango_scroll("repeatLast", "down")
left again: user.rango_scroll("repeatLast", "left")
right again: user.rango_scroll("repeatLast", "right")

# Snap scroll
crown <user.rango_target>: user.rango_snap_scroll(rango_target, "top")
center <user.rango_target>: user.rango_snap_scroll(rango_target, "center")
bottom <user.rango_target>: user.rango_snap_scroll(rango_target, "bottom")
crown <user.text>$: user.rango_snap_scroll_text(text, "top")
center <user.text>$: user.rango_snap_scroll_text(text, "center")
bottom <user.text>$: user.rango_snap_scroll_text(text, "bottom")

# Custom scroll positions
scroll save <user.text>: user.rango_store_scroll_position(text)
scroll to <user.text>: user.rango_scroll_to_position(text)

# Copy target information
copy [link] <user.rango_target>: user.rango_copy_link(rango_target)
copy mark <user.rango_target>: user.rango_copy_markdown_link(rango_target)
copy content <user.rango_target>: user.rango_copy_element_text(rango_target)

# Paste
paste to <user.rango_target>:
  user.rango_insert_text_to_input(clip.text(), rango_target)

# Insert text to field
insert <user.text> to <user.rango_target>:
  user.rango_insert_text_to_input(text, rango_target)
enter <user.text> to <user.rango_target>:
  user.rango_insert_text_to_input(text, rango_target, true)

# Cursor position
pre <user.rango_target>: user.rango_set_selection_before(rango_target)
post <user.rango_target>: user.rango_set_selection_after(rango_target)

# Clear field
change <user.rango_target>:
  user.rango_clear_input(rango_target)

# Copy current url information
copy page {user.rango_page_location_property}:
  user.rango_copy_location_property(rango_page_location_property)
copy mark address: user.rango_copy_current_tab_markdown_url()

# Modify hints appearance
hint bigger: user.rango_increase_hint_size()
hint smaller: user.rango_decrease_hint_size()

# Extra hints
hint extra: user.rango_display_extra_hints()
hint more: user.rango_display_excluded_hints()
hint less: user.rango_display_less_hints()
include <user.rango_target>: user.rango_include_extra_selectors(rango_target)
exclude <user.rango_target>: user.rango_exclude_extra_selectors(rango_target)
exclude all: user.rango_exclude_all_hints()
some more: user.rango_include_or_exclude_more_selectors()
some less: user.rango_include_or_exclude_less_selectors()
custom hints save: user.rango_confirm_selectors_customization()
custom hints reset: user.rango_reset_custom_selectors()

# Show and hide hints
hints refresh: user.rango_refresh_hints()
hints (toggle | switch): user.rango_toggle_hints()
hints on [{user.rango_hints_toggle_levels}]:
  user.rango_enable_hints(rango_hints_toggle_levels or "global")
hints off [{user.rango_hints_toggle_levels}]:
  user.rango_disable_hints(rango_hints_toggle_levels or "global")
hints reset {user.rango_hints_toggle_levels}:
  user.rango_reset_toggle_level(rango_hints_toggle_levels)
toggle show: user.rango_display_toggles_status()
labels: user.rango_enable_hints("now")

# Toggle tab hints
[tab] marker (toggle | switch): user.rango_toggle_tab_markers()

# Toggle keyboard clicking
keyboard (toggle | switch): user.rango_toggle_keyboard_clicking()

# Pages
rango open {user.rango_page}: user.rango_open_page_in_new_tab(rango_page)
rango settings: user.rango_open_settings_page()
rango what's new: user.rango_open_whats_new_page()

#  Hint/element references for scripting
mark <user.rango_target> as <user.text>: user.rango_save_reference(rango_target, text)
mark this as <user.text>: user.rango_save_reference_for_active_element(text)
mark show: user.rango_show_references()
mark clear <user.text>: user.rango_remove_reference(text)

# Run action by matching the text of an element
follow <user.text>:
  user.rango_run_action_on_text_matched_element("clickElement", text, true)
button <user.text>:
  user.rango_run_action_on_text_matched_element("clickElement", text, false)

rango explicit: user.rango_force_explicit_clicking()
rango direct: user.rango_force_direct_clicking()
