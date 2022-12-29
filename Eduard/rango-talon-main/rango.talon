tag: browser
-
settings():
  user.rango_start_with_direct_clicking = 1

# Click
click <user.rango_target>:
  user.rango_command_with_target("clickElement", rango_target)

# Open in a new tab
blank <user.rango_target>:
  user.rango_command_with_target("openInNewTab", rango_target)
stash <user.rango_target>:
  user.rango_command_with_target("openInBackgroundTab", rango_target)

# Close tabs
tab close other: user.rango_command_without_target("closeOtherTabsInWindow")
tab close left: user.rango_command_without_target("closeTabsToTheLeftInWindow")
tab close right: user.rango_command_without_target("closeTabsToTheRightInWindow")
tab close first [<number_small>]:
  user.rango_command_without_target("closeTabsLeftEndInWindow", number_small or 1)
tab close final [<number_small>]:
  user.rango_command_without_target("closeTabsRightEndInWindow", number_small or 1)
tab close previous [<number_small>]:
  user.rango_command_without_target("closePreviousTabsInWindow", number_small or 1)
tab close next [<number_small>]:
  user.rango_command_without_target("closeNextTabsInWindow", number_small or 1)

# Clone tab
tab clone: user.rango_command_without_target("cloneCurrentTab")

# Hover
hover <user.rango_target>:
  user.rango_command_with_target("hoverElement", rango_target)
dismiss: user.rango_command_without_target("unhoverAll")

# Show link address
show <user.rango_target>:
  user.rango_command_with_target("showLink", rango_target)

# Scroll
upper: user.rango_command_without_target("scrollUpPage")
tiny up: user.rango_command_without_target("scrollUpPage", 0.2)
downer: user.rango_command_without_target("scrollDownPage")
tiny down: user.rango_command_without_target("scrollDownPage", 0.2)
upper <user.rango_target>:
  user.rango_command_with_target("scrollUpAtElement", rango_target)
tiny up <user.rango_target>:
  user.rango_command_with_target("scrollUpAtElement", rango_target, 0.2)
downer <user.rango_target>:
  user.rango_command_with_target("scrollDownAtElement", rango_target)
tiny down <user.rango_target>:
  user.rango_command_with_target("scrollDownAtElement", rango_target, 0.2)
up again: user.rango_command_without_target("scrollUpAtElement")
down again: user.rango_command_without_target("scrollDownAtElement")
crown <user.rango_target>:
  user.rango_command_with_target("scrollElementToTop", rango_target)
bottom <user.rango_target>:
  user.rango_command_with_target("scrollElementToBottom", rango_target)
center <user.rango_target>:
  user.rango_command_with_target("scrollElementToCenter", rango_target)

# Copy target information
copy [link] <user.rango_target>:
  user.rango_command_with_target("copyLink", rango_target)
copy mark <user.rango_target>:
  user.rango_command_with_target("copyMarkdownLink", rango_target)
copy text <user.rango_target>:
  user.rango_command_with_target("copyElementTextContent", rango_target)

# Copy current url information
copy page {user.rango_page_location_property}:
  user.rango_command_without_target("copyLocationProperty", rango_page_location_property)
copy mark address:
  user.rango_command_without_target("copyCurrentTabMarkdownUrl")

# Modify hints appearance
hint bigger: user.rango_command_without_target("increaseHintSize")
hint smaller: user.rango_command_without_target("decreaseHintSize")
hint {user.rango_hint_styles}: 
  user.rango_command_without_target("setHintStyle", user.rango_hint_styles)
hint weight {user.rango_hint_weights}:
  user.rango_command_without_target("setHintWeight", user.rango_hint_weights)

# Exclude or include single letter hints
hint exclude singles: user.rango_command_without_target("excludeSingleLetterHints")
hint include singles: user.rango_command_without_target("includeSingleLetterHints")

# Show and hide hints
hints refresh: user.rango_command_without_target("refreshHints")
hints toggle: user.rango_command_without_target("toggleHints")
hints on [{user.rango_hints_toggle_levels}]: 
  user.rango_command_without_target("enableHints", rango_hints_toggle_levels or "global")
hints off [{user.rango_hints_toggle_levels}]: 
  user.rango_command_without_target("disableHints", rango_hints_toggle_levels or "global")
hints reset {user.rango_hints_toggle_levels}: 
  user.rango_command_without_target("resetToggleLevel", rango_hints_toggle_levels)

# Toggle keyboard clicking
keyboard toggle: user.rango_command_without_target("toggleKeyboardClicking")

# Enable or disable showing the url in the title
address in title on: user.rango_command_without_target("enableUrlInTitle")
address in title off: user.rango_command_without_target("disableUrlInTitle")

# Switch modes
rango explicit:  user.rango_disable_direct_clicking()
rango direct:  user.rango_enable_direct_clicking()
