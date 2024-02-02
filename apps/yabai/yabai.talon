os: mac
user.running: yabai
-

win {user.yabai_dir}: user.yabai("window --focus {yabai_dir}")

win swap {user.yabai_selector}: user.yabai("window --swap {yabai_selector}")

win (warp | move) {user.yabai_dir}: user.yabai("window --warp {yabai_dir}")

win put {user.yabai_dir}: user.yabai("window --put {yabai_dir}")

win grow {user.arrow_key}: user.yabai_win_resize("{arrow_key}", 100)

win shrink {user.arrow_key}: user.yabai_win_resize("{arrow_key}", -100)

win screen: user.yabai("window --display recent")

win space <number_small>: user.yabai("window --space {number_small}")

win space {user.yabai_selector}: user.yabai("window --space {yabai_selector}")

# Requires disabling system integrity protection :(
# space <number_small>:
#   user.yabai("space --focus {number_small}")

# space {user.yabai_selector}:
#   user.yabai("space --focus {yabai_selector}")

space mirror: user.yabai("space --mirror y-axis")

space mirror vert: user.yabai("space --mirror x-axis")

space balance: user.yabai("space --balance y-axis")

space balance vert: user.yabai("space --balance x-axis")

space rotate: user.yabai("space --rotate 90")

screen (switch | swap): user.yabai("display --focus recent")
