# Window Tweak

## Description

A [Talon](https://talonvoice.com/) module for moving and resizing windows using voice commands.

For example, the spoken command '`window move east`' will start moving the current window toward the right of the screen. A dialog box pops up showing the verbal command to use to stop the motion, e.g. '`window stop`', and also provides a button for that purpose. The window will automatically stop moving when it reaches the edge of the current screen.

There are similar commands, '`window stretch east`' and '`window shrink east`', for resizing the current window.

If you change your mind, the '`window revert`' command restores the previous position/size of the current window.

In addition to the four cardinal directions - `North, South, East, West` - and the four ordinal directions - `Northeast (NE), Southeast (SE), Southwest (SW), Northwest (NW)` - we also have '`in`' and '`out`', for moving in toward the center of the screen and out away from the center of the screen, respectively.

Alternatively, you can use the mouse pointer to indicate the distance and direciton of the move or resize operation, e.g. '`window stretch diagonal to pointer`'.

There are also commands that let you place or size windows more precisely. For example, you can say '`window move east twenty percent`' to move the current window toward the right of the screen by an amount equal to twenty percent of the window size. Or, you can specify the amount in pixels, rather than as a percentage - '`window move east 293 pixels`'.

This is just a sample, the complete set of commands can be found in the '`window_tweak.talon`' file.

There are some demo videos, just be aware that the commands have changed slightly since the recordings were made. For example, the commands in the video use the term '`win`' instead of '`window`', and there are other slight differences.

 * [Talon Window Tweak Demo](https://youtu.be/q4gm839KhqY)
 * [Supplemental Talon Window Tweak Demo](https://youtu.be/EyMvwUyZN5k)

# Usage

Just download this code into your Talon user folder somewhere.

## Settings

The `settings.talon` file provides switches for controlling the speed of window move/resize operations, among other things. See the comments in that file for more information.

# Bugs

See https://github.com/codecat555/window-tweak/issues.

### Talon issues

* In addition to the issues described below, there are some quirks described at the top of the .py files found in this repo.

* Talon may sometimes fail to send an event notifying of a change in window size or position (https://github.com/talonvoice/talon/issues/470).

* On macs, Talon will complain when part of a window is moved off the visible screen. The error reported is `ValueError: screen not found containing point`. See https://github.com/knausj85/knausj_talon/pull/771#issuecomment-1066181341.

# Other Applications

You can easily `define your own voice commands` using the actions defined in the window_tweak.py file.

Further, you can use the code in compass_control.py to `drive applications other than changing windows`. That module doesn't really know anything about windows, per se, it just manipulates rectangles. It can be applied to any application where you need to move and resize objects within a rectangular frame. So, it could be used for moving pieces around on a game board or arranging panes within a parent window, for example. The simple path to getting started on this would be to copy the window_tweak.py file and then customize it for your application.
