os: mac
user.running: amethyst
-

gem cycle [next]:
    key("alt-shift-space")
    # Cycle layout forward

gem cycle last:
    # Cycle layout backwards
    key("ctrl-alt-shift-space")

gem shrink:
    # Shrink the main pane
    key("alt-shift-h")

gem grow:
    # Expand the main pane
    key("alt-shift-l")

gem swap (last | left):
    # Swap focused window counter clockwise
    key("ctrl-alt-shift-j")

gem swap [(next | right)]:
    # Swap focused window clockwise
    key("ctrl-alt-shift-k")

gem main:
    # Swap focused window with main window
    key("alt-shift-enter")

gem more:
    # Increase main pane count
    key("alt-shift-,")

gem less:
    # Decrease main pane count
    key("alt-shift-.")

gem last:
    # Move focus counter clockwise
    key("alt-shift-j")

gem next:
    # Move focus clockwise
    key("alt-shift-k")

gem reload:
    # Force windows to be reevaluated
    key("alt-shift-z")

gem restart:
    # Relaunch Amethyst
    key("ctrl-alt-shift-z")

screen last:
    # Move focus to counter clockwise screen
    key("alt-shift-p")

screen next:
    # Move focus to clockwise screen
    key("alt-shift-n")

screen send (last | left):
    # Swap focused window to counter clockwise screen
    key("ctrl-alt-shift-h")

screen send (next | right):
    # Swap focused window to clockwise screen
    key("ctrl-alt-shift-l")

screen one:
    # Focus Screen 1
    key("alt-shift-w")

screen send one:
    # Throw focused window to screen 1
    key("ctrl-alt-shift-w")

screen two:
    # Focus Screen 2
    key("alt-shift-e")

screen send two:
    # Throw focused window to screen 2
    key("ctrl-alt-shift-e")

screen three:
    # Focus Screen 3
    key("alt-shift-r")

screen send three:
    # Throw focused window to screen 3
    key("ctrl-alt-shift-r")

screen four:
    # Focus Screen 4
    key("alt-shift-q")

screen send four:
    # Throw focused window to screen 4
    key("ctrl-alt-shift-q")
