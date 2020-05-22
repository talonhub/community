
snap left: user.win_grid("left")
snap right: user.win_grid("right")
snap top: user.win_grid("top")
snap bottom: user.win_grid("bottom")

# Thirds and two thirds of the screen

snap center third: user.win_grid("snap center third")
snap left third: user.win_grid("left third")
snap right third: user.win_grid("right third")
snap left two thirds: user.win_grid("left two thirds")
snap right two thirds: user.win_grid("right two thirds")

# Quarters of the screen

snap top left: user.win_grid("snap top left")
snap top right: user.win_grid("top right")
snap bottom left: user.win_grid("bottom left")
snap bottom right: user.win_grid("bottom right")

# Third-of-the-screen versions of top quarters

snap top left third: user.win_grid("snap top left third")
snap top right third: user.win_grid("top right third")
snap top left two thirds: user.win_grid("top left two thirds")
snap top right two thirds: user.win_grid("top right two thirds")
snap top center third: user.win_grid("top center third")

# Third-of-the-screen versions of bottom quarters

snap bottom left third: user.win_grid("snap bottom left third")
snap bottom right third: user.win_grid("bottom right third")
snap bottom left two thirds: user.win_grid("bottom left two thirds")
snap bottom right two thirds: user.win_grid("bottom right two thirds")
snap bottom center third: user.win_grid("bottom center third")
snap center: user.win_grid("center")
snap (fullscreen | screen | window): user.win_grid("fullscreen")

snap next: user.win_grid("snap next")
snap last: user.win_grid("last")
snap window [move] next screen: user.win_grid("window next screen")
snap window [move] preev screen: user.win_grid("window prev screen")
