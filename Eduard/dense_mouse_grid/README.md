This is the "dense mouse grid". It fills the screen with fields that can be reached with two letters and a number.

To use this, put the folder dense_mouse_grid anywhere in the talon user directory. This assumes that 1. you have Talon installed, and 2. you are using the knausj talon repository detailed in the [installation instructions here](https://talonvoice.com/docs/index.html#getting-started)

![image](https://user-images.githubusercontent.com/1163925/130808333-219a48b3-650c-4d4c-9a99-d9909011132d.png)

![Video Demonstration of Playing Dominion Using The Dense Mouse Grid](https://youtu.be/ookc134jPNQ)



then use these voice commands:

* `alphabet soup` to show the grid. 
* `alphabet win` to put the grid over the active window
* `alphabet screen <number>` to put the grid over a different screen from the first one

# Basic usage in Frame Mode

The grid will appear in frame mode.  Frame mode 'frames' each of the large blocks with letters to indicate row and column.  Saying a coordinate in the following manner: 

**two**

This will select the first block, make the large number two disappear, and remove the color overlay to show that this block is the actively selected block. 

**cap**

This will select row C.  A red row will appear with all of the letters in row c. 

**drum**

This will select column 'd' and move the mouse pointer to coordinate '2 C D'

**touch** will click the mouse pointer.  


It is not necessary to have pauses between the coordinates.  You can say 

'2 Cap Drum' and it will move the mouse pointer to coordinate 2 C D, without showing all the helper graphics.

# Other Modes

If frame mode does not suit you, there are two other modes that can be used to show the coordinates.  

'alphabet checkers' turns on checker mode, which overlays the coordiantes in a checker pattern. This can be visually confusing, but it splits the difference between being able to immediately see the coordinate and being able to see the contents of your screen.  

![](https://gist.githubusercontent.com/timo/b3429ede632f0eb9cac0eb142746dc3b/raw/ebf6185ded98d1ff960047c351d45c6618906891/screenshot.png)

'alphabet full' shows every possible coordinate. 

![](https://gist.githubusercontent.com/timo/b3429ede632f0eb9cac0eb142746dc3b/raw/1bbb642824ba7a8dcb2c5d1710460bd7ecd28c0e/screenshot.png)

'alphabet frame' switches back to the default frame mode.



# Using the Linked Commands

When the screen is showing you can select fields using your alphabet words and a number for the field:

* `cap whale one` selects field CW in the top left field
* `one drum gust` selects field DG in the top left field
* `three vest near` selects field VN in whatever field has number 3


# using just alphabet coordinates


When you already have a number block selected, you can simply say 'bat cap' and it will select coordiante 'bat cap'

By default, the grid stays up.  You can turn off the grid by saying 'grid close.'
