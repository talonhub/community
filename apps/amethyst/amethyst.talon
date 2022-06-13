os: mac
user.running: amethyst
-
win cycle [next]:
  key("alt-shift-space")
  # Cycle layout forward
 
win cycle last:
  # Cycle layout backwards
  key("ctrl-alt-shift-space")
 
win shrink:
  # Shrink the main pane
  key("alt-shift-h")
 
win grow:
  # Expand the main pane
  key("alt-shift-l")

win swap (last|left):
  # Swap focused window counter clockwise
  key("ctrl-alt-shift-j")

win swap [(next|right)]:
  # Swap focused window clockwise
  key("ctrl-alt-shift-k")
  
win main:
  # Swap focused window with main window
  key("alt-shift-enter")
 
win more:
  # Increase main pane count
  key("alt-shift-,")
 
win less:
  # Decrease main pane count
  key("alt-shift-.")
 
win last:
  # Move focus counter clockwise
  key("alt-shift-j")
 
win next:
  # Move focus clockwise
  key("alt-shift-k")
 
screen last:
  # Move focus to counter clockwise screen
  key("alt-shift-p")
 
screen next:
  # Move focus to clockwise screen
  key("alt-shift-n")
 
screen swap last:
  # Swap focused window to counter clockwise screen
  key("ctrl-alt-shift-h")
 
screen swap next:
  # Swap focused window to clockwise screen
  key("ctrl-alt-shift-l")
 
win reload:
  # Force windows to be reevaluated
  key("alt-shift-z")
 
win restart:
  # Relaunch Amethyst
  key("ctrl-alt-shift-z")
 
screen one:
  # Focus Screen 1
  key("alt-shift-w")
 
screen send one:
  # Throw focused window to screen'too' 1
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
 
win float:
  # Toggle float for focused window
  key("alt-shift-t")
 
win show:
  # Display current layout
  key("alt-shift-i")
 
win switch:
  # Toggle global tiling
  key("ctrl-alt-shift-t")
  
win tall:
   # Select tall-right layout
   key("ctrl-alt-shift-a")
 
win tall left:
  # Select tall layout
  key("alt-shift-a")
 
win wide:
  # Select wide layout
  key("alt-shift-s")
 
win column:
  # Select 3column right layout
  key("alt-shift-f")

win center:
  # Select 3column middle layout
  key("ctrl-alt-shift-f")
 
win full [screen]:
  # Select fullscreen layout
  key("alt-shift-d")

win float all:
  # Select floating layout
  key("alt-shift-b")
 
# win column:
  # Select column layout
 
# win row:
  # Select row layout

# win widescreen tall:
  # Select widescreen-tall layout
 
# win bsp:
  # Select bsp layout
