os: windows
-

#Useful for when you have two screens, with an eye tracker only on the main screen
[windows] switch both:
    key(super-shift-left)
    sleep(60ms)
    key(alt-tab)
    sleep(60ms)
    key(super-shift-left)
