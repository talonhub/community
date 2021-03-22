from talon import Module

mod = Module()
grids_put_one_bottom_left = mod.setting(
    "grids_put_one_bottom_left",
    type=bool,
    default=False,
    desc="""Allows you to switch mouse grid and friends between a computer numpad and a phone numpad (the number one goes on the bottom left or the top left)""",
)
