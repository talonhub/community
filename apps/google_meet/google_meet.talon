app: Google Meet

-

# Google Meet is a Desktop version of Meet.
# Its a "Progressice Web App" which is installable on the desktop.
# Installation instructions are found at https://support.google.com/meet/answer/10708569?hl=en

tag(): browser

# not a lot of keyboard short cuts are available.
# so you probably want to use something like the
# vimium extension for more controls.
([toggle] mute | unmute): key(super-d)
toggle (video | camera): key(super-e)
(raise | lower | toggle) hand: key(ctrl-super-h)
