# While windows are marked in the thumbnail switcher: the marked bar's buttons, by
# their labels. Anchored, so they only work said on their own.
os: windows
tag: user.thumbnail_switcher_marked
-
^close$: user.thumbnail_switcher_marked_button("close")
^minimize$: user.thumbnail_switcher_marked_button("minimize")
^restore$: user.thumbnail_switcher_marked_button("restore")
# Snap with one window marked, layout with several (the bar shows the one that applies;
# the other says so). "snap layout" is the old name of layout.
^snap$: user.thumbnail_switcher_marked_button("snap")
^layout$: user.thumbnail_switcher_marked_button("layout")
^snap layout$: user.thumbnail_switcher_marked_button("layout")
^move to desktop$: user.thumbnail_switcher_marked_button("move to desktop")
^move to screen$: user.thumbnail_switcher_marked_button("move to screen")
^clear$: user.thumbnail_switcher_marked_button("clear")
