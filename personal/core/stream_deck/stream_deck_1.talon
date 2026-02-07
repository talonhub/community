# deck.serial: A00SA3232MA4OZ
deck.serial: A00SA3232MA4OZ
# 2024-01-07 14:58:00.435  INFO Deck connected: Deck(pid=128, kind=Mk2, serial='A00SA3232MA4OZ', layout=None)
# 2024-01-07 14:58:00.445  INFO Deck connected: Deck(pid=134, kind=Pedal, serial='', layout=None)
# 2024-01-07 14:58:00.453  INFO Deck connected: Deck(pid=128, kind=Mk2, serial='A00SA3232MA4OZ', layout=None)
# 2024-01-07 14:58:00.463  INFO Deck connected: Deck(pid=134, kind=Pedal, serial='', layout=None)
-
#images from https://joypixels.com/emoji
deck(default/magnifying-glass-tilted-right):
    user.deck1()
deck(default/house-with-garden):
    user.deck2()
deck(default/down-arrow):
    user.deck3()
deck(default/up-arrow):
    user.deck4()
deck(default/stop-sign):
    user.deck5()
deck(default/delivery-truck):
    user.deck6()
deck(default/fast-up-button):
    user.deck7()
deck(default/mobile-phone):
    user.deck8()
deck(default/man-gesturing-no):
    user.deck9()
deck(default/repeat-button):
    user.deck10()
deck(default/speaking-head):
    user.deck11()
deck(default/eye):
    user.deck12()
deck(default/studio-microphone):
    user.deck13()
# deck(default/currency-exchange):
#     user.deck14()
deck(default/zzz):
    user.deck15()


deck(zoom/left):
    user.deck1()
deck(zoom/right):
    user.deck2()
deck(zoom/double):
    user.deck3()
deck(zoom/triple):
    user.deck4()
deck(zoom/drag):
    user.deck5()
deck(zoom/shift-left):
    user.deck6()
# deck(zoom):
#     user.deck7()
# deck(zoom):
#     skip()
# deck(zoom):
#     skip()
# deck(zoom):
#     skip()
deck(zoom/ctrl-left):
    user.deck11()
deck(zoom/move):
    user.deck12()
# deck(zoom):
#     skip()
# deck(zoom):
#     skip()
# # deck(zoom/currency-exchange):
# #     user.deck14()
# deck(zoom):
#     skip(user.deck15)
deck(control/left):
    mouse_click(0)
deck(control/right):
    mouse_click(1)
deck(control/double):
    mouse_click(0)
    mouse_click(0)
deck(control/triple):
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
deck(control/drag):
    user.mouse_drag(0)
deck(control/shift-left):
    key("shift:down")
    mouse_click(0)
    key("shift:up")
deck(control/down-arrow):
    user.deck3()
deck(control/up-arrow):
    user.deck4()
deck(control/man-gesturing-no):
    user.deck9()
deck(control/repeat-button):
    user.deck10()
deck(control/ctrl-left):
    key("ctrl:down")
    mouse_click(0)
    key("ctrl:up")
deck(control/fast-up-button):
    user.deck7()
deck(control/mobile-phone):
    user.deck8()
# deck(control/eye):
#     user.deck12()
# deck(control/studio-microphone):
#     user.deck13()
# deck(control/currency-exchange):
#     user.deck14()
deck(control/zzz):
    user.deck15()

deck(reject/gud 1):
    user.rejection_move_last(1)
deck(reject/gud 2):
    user.rejection_move_last(2)
# deck(reject/eye):
#     user.deck12()
# deck(reject/studio-microphone):
#     user.deck13()
# deck(reject/currency-exchange):
#     user.deck14()
deck(reject/bad):
    user.rejection_move_last(3)
deck(reject/rev):
    user.rejection_move_last(4)
deck(reject/zzz):
    user.deck15()

deck(scrolling/x):
    skip()
deck(scrolling/y):
    skip()
deck(scrolling/down-arrow):
    user.deck3()
deck(scrolling/up-arrow):
    user.deck4()

deck(scrolling/5):
    user.deck5()
deck(scrolling/10):
    user.deck6()
deck(scrolling/25):
    user.deck7()
deck(scrolling/35):
    user.deck8()
deck(scrolling/55):
    user.deck9()
deck(scrolling/100):
    user.deck10()
# deck(scrolling/repeat-button):
#     user.deck10()
# deck(scrolling/speaking-head):
#     user.deck11()
# deck(scrolling/eye):
#     user.deck12()
# deck(scrolling/studio-microphone):
#     user.deck13()
# deck(scrolling/currency-exchange):
#     user.deck14()
deck(scrolling/stop):
    user.mouse_scroll_stop()
    deck.goto("A00SA3232MA4OZ", "default")
deck(scrolling/stop 2):
    user.mouse_scroll_stop()
    deck.goto("A00SA3232MA4OZ", "default")
deck(scrolling/stop 3):
    user.mouse_scroll_stop()
    deck.goto("A00SA3232MA4OZ", "default")
deck(scrolling/zzz):
    user.mouse_scroll_stop()
    deck.goto("A00SA3232MA4OZ", "default")