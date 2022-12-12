app: Final Cut Pro
app: Final Cut Pro Trial
-
# ----------------------
# GENERAL
# ----------------------



# ----------------------
# FILE COMMANDS
# ----------------------
new project:
    key(cmd-n)

new event:
    key(alt-e)

new compound:
    key(alt-g)

import media:
    key(cmd-i)

export project:
    key(cmd-e)

reveal browser:
    key(shift-f)

reveal project:
    key(alt-shift-f)

reveal finder:
    key(cmd-shift-r)



# ----------------------
# TIMELINE
# ----------------------

# Play the timeline and stop
(play | stop):
    key(space)

# Turn off the clip and on
(clip on | clip off):
    key(v)

# Above the timeline
insert above: 
    key(q)

# Into the timeline
insert timeline:
    key(w)

# End of the timeline
insert end:
    key(e)

# Mark in and out the point
mark in:
    key(i)

mark out:
    key(o)

# Reposition or overwritre
reposition:
    key(p)

# Play backwards
play backward:
    key(j)

# Play at a high speed
play speed:
    key(l)

# Previous/next start of clip
(previous | next) start:
    key(;)

# Zoom tool
zoom:
    key(z)

# Snapping tool
snap:
    key("n")

# Mark timeline/club
mark it:
    key(m)



# ----------------------
# MARKING
# ----------------------

# Set range start
range start:
    key(i)

# Set range end
range end:
    key(o)

# Set clip range
range end:
    key(x)

# Browser Filter: Show all clips
show all clips:
    key(ctrl-c)

# 
est:
    key(f)

# 
est:
    key(f)

# 
test:
    key(f)

# 
test:
    key(f)

# 
test:
    key(f)

# 
test:
    key(f)


# ----------------------
# EDITING
# ----------------------

# Skim timeline
skim:
    key(s)

# Duplicate
duce:
    key(cmd-d)

# Select tool
(select | move):
    key(a)

# Trim tool
trim:
    key(t)

# Position toll
position:
    key(p)

# Range tool
range:
    key(b)

# Hand tool
hand:
    key(h)

# Blade tool
blade:
    key(b)

# Blade at playhead
cut here:
    key(cmd-b)

# Blade All
cut all:
    key(cmd-shift-b)

# Trim start
trim start:
    key(alt-[)

# Trim end
trim end:
    key(alt-])

# Trim to playhead
trim playhead:
    key(alt-\)

# Zoom out
zout [<number>]: 
    key('cmd--')
    repeat(number - 1)

# Zoom in
zoon [<number>]:
    key('cmd-=')

# Zoom to fit
(scan | scale | zoom to fit):
    key("shift-z")

# Add basic title
add title:
    key(ctrl-t)

# Add a lower third title
add lower third:
    key(ctrl-shift-t)

# Volume across all
volume across all:
    key(cmd-l)

# Expand audio
expand audio:
    key(ctrl-s)

# Collapse audio
collapse audio:
    key(ctrl-shift-s)



# ----------------------
# ORGANIZATION
# ----------------------

# New event
new event:
    key(alt-n)

# New folder
new folder:
    key(cmd-shift-n)

# Clip in browser
clip in browser:
    key(shift-f)

# Project in browser
project in browser:
    key(alt-shift-cmd-f)

# Sync event clips 
sync event clips:
    key(alt-cmd-g)



# ----------------------
# EFFECTS
# ----------------------

# Create two second hold segment
second hold:
    key(shift-h)

# Open re time editor
retime editor:
    key(cmd-r)

# Remove all effects from selection
(remove fx | dellfix):
    key(alt-cmd-x)

# Remove attributes from selection
(remove | dellz) (attributes | bute):
    key(shift-cmd-x)

# Navigate to the previous text item
(navigate | nav | go) previous text:
    key(alt-shift-tab)

# Paste attributes or settings
paste (attributes | bute):
    key(cmd-shift-v)

# Paste effects to selection
(paste fx | pafix):
    key(alt-cmd-v)

# Balance color corrections on or off
color correct (on | off):
    key(cmd-alt-b)

# Reset controls (color board pane)
reset controls:
    key(alt-delete)

# 
test:
    key(f)

# 
test:
    key(f)