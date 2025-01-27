# Laying Out Windows

The `layout` command allows you to lay out multiple windows around the screen in prearranged configurations. With a single command you can arrange multiple windows and if you repeat the same command it will rotate them. Here are some example arrangements:

Halves: Split the screen into two halves. The first window goes to the left half and the second goes to the right.
Thirds: Split the screen into thirds, arranging from left to right. 
Clock: Arrange one window on the left half, and split the right from top to bottom.

When arranging windows if you specify nothing it will arrange in order of windows from top to bottom-in other words, the most recent three windows that you have interacted with will be snapped into the arrangement. If you want more control you can specify windows by saying an application name or using an ordinal such as 'second' to refer to the second window from the top of the window manager (the second most recently used window). If you want to skip a particular position when arranging windows, you can use the word 'gap' to skip a position. You can also use the word 'all' to refer to the rest of the windows available filling up all available slots. Here are some examples:

1. `layout clock`: Arrange the most recent three windows in a clockwise layout
2. `layout halves chrome slack`: Arrange chrome and slack in a split screen.
3. `layout halves gap slack`: Arrange slack on the right (skipping the first placement, which would have been on the left)
4. `layout clock second all`: Move these second from the top window to the first position, rearranging all other windows accordingly.

If you repeat any of these commands without interacting with the window using the mouse, it will rotate the arrangement.