work <number_small>: user.desktop(number_small)
work (next|right): user.desktop_next()
work (last|left): user.desktop_last()
work show: user.desktop_show()
work send <number_small>: user.window_move_desktop(number_small)
work send (last|left): user.window_move_desktop_left()
work send (next|right): user.window_move_desktop_right()
work carry <number_small>:
  user.window_move_desktop(number_small)
  user.desktop(number_small)
work carry (last|left):
  user.window_move_desktop_left()
  user.desktop_next()
work carry (next|right):
  user.window_move_desktop_right()
  user.desktop_last()
