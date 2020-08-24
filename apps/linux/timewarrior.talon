# https://timewarrior.net
os: linux
tag: terminal
-

time (war|warrior): "timew\n"
# Just set a generic timer
time (war|warrior) start now: "timew start\n"
time (war|warrior) start <phrase>: "timew start {phrase}"
time (war|warrior) start <number_small> minutes ago: "timew start {number_small}mins ago "
time (war|warrior) start <number_small> hours ago: "timew start {number_small}hours ago "
time (war|warrior) start: "timew start "
time (war|warrior) stop now: "timew stop\n"
time (war|warrior) stop: "timew stop "
time (war|warrior) stop <number_small> minutes ago: "timew stop {number_small}mins ago "
time (war|warrior) stop <number_small> hours ago: "timew stop {number_small}hours ago "
time (war|warrior) cancel: "timew cancel\n"
time (war|warrior) summary: "timew summary\n"
time (war|warrior) tags: "timew tags\n"

time (war|warrior) extensions: "timew extensions\n"
