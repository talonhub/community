# deck.serial: A00SA3232MA4OZ
deck.serial: A00SA3192M9DW0
# 2024-01-07 14:58:00.435  INFO Deck connected: Deck(pid=128, kind=Mk2, serial='A00SA3232MA4OZ', layout=None)
# 2024-01-07 14:58:00.445  INFO Deck connected: Deck(pid=134, kind=Pedal, serial='', layout=None)
# 2024-01-07 14:58:00.453  INFO Deck connected: Deck(pid=128, kind=Mk2, serial='A00SA3192M9DW0', layout=None)
# 2024-01-07 14:58:00.463  INFO Deck connected: Deck(pid=134, kind=Pedal, serial='', layout=None)
-
#images from https://joypixels.com/emoji
deck(default/no 1):
    skip()
deck(default/no 2):
    skip()
deck(default/down-arrow):
    user.deck3()
deck(default/up-arrow):
    user.deck4()
deck(default/no 3):
    skip()
deck(default/no 4):
    skip() 
deck(default/mobile-phone):
    user.deck7()
deck(default/undo):
    user.deck8()
deck(default/redo):
    user.deck9()
deck(default/repeat-button):
    user.deck10()
deck(default/speaking-head):
    user.deck11()
deck(default/no 5):
    skip()
deck(default/studio-microphone):
    user.deck13()
deck(default/zzz):
     user.deck14()
# deck(default/currency-exchange):
#     user.deck14()

# deck(zoom/left):
#     user.deck1()
# deck(zoom/right):
#     user.deck2()
# deck(zoom/double):
#     user.deck3()
# deck(zoom/triple):
#     user.deck4()
# deck(zoom/drag):
#     user.deck5()
# deck(zoom/shift-left):
#     user.deck6()
# deck(zoom):
#     user.deck7()
# deck(zoom):
#     skip()
# deck(zoom):
#     skip()
# deck(zoom):
#     skip()
# deck(zoom/ctrl-left):
#     user.deck11()
# deck(zoom/move):
#     user.deck12()
# deck(zoom):
#     skip()
# deck(zoom):
#     skip()
# # deck(zoom/currency-exchange):
# #     user.deck14()
# deck(zoom):
#     skip(user.deck15)

deck(mouse/triple):
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)
deck(mouse/no):
    skip()
deck(mouse/down-arrow):
    user.deck3()
deck(mouse/up-arrow):
    user.deck4()
deck(mouse/ctrl-left):
    key("ctrl:down")
    mouse_click(0)
    key("ctrl:up")
deck(mouse/double):
    mouse_click(0)
    mouse_click(0)
deck(mouse/shift-left):
    key("shift:down")
    mouse_click(0)
    key("shift:up")
deck(mouse/undo):
    user.deck8()
deck(mouse/redo):
    user.deck9()
deck(mouse/drag):
    user.mouse_drag(0)
deck(mouse/left):
    mouse_click(0)
deck(mouse/right):
    mouse_click(1)
deck(mouse/studio-microphone):
    user.deck13()
deck(mouse/zzz):
     user.deck14()
# deck(mouse/x):
#     skip()
# deck(mouse/y):
#     skip() 
# deck(control/fast-up-button):
#     user.deck7()
# deck(control/mobile-phone):
#     user.deck8()
# deck(control/eye):
#     user.deck12()
# deck(control/studio-microphone):
#     user.deck13()
# deck(control/currency-exchange):
#     user.deck14()
# deck(control/zzz):
#     user.deck15()

# deck(reject/gud 1):
#     user.rejection_move_last(1)
# deck(reject/gud 2):
#     user.rejection_move_last(2)
# # deck(reject/eye):
# #     user.deck12()
# # deck(reject/studio-microphone):
# #     user.deck13()
# # deck(reject/currency-exchange):
# #     user.deck14()
# deck(reject/bad):
#     user.rejection_move_last(3)
# deck(reject/rev):
#     user.rejection_move_last(4)
# deck(reject/zzz):
#     user.deck15()

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
    deck.goto("A00SA3192M9DW0", "default")
deck(scrolling/stop 2):
    user.mouse_scroll_stop()
    deck.goto("A00SA3192M9DW0", "default")
deck(scrolling/stop 3):
    user.mouse_scroll_stop()
    deck.goto("A00SA3192M9DW0", "default")
deck(scrolling/zzz):
    user.mouse_scroll_stop()
    deck.goto("A00SA3192M9DW0", "default")