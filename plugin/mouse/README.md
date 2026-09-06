# Mouse

## Continuous Scrolling

You can start continuous scrolling by saying "wheel upper" or "wheel downer" and stop by saying "wheel stop". Saying "here" after one of the scrolling commands first moves the cursor to the middle of the window. A number between 1 and 99 can be dictated at the end of a scrolling command to set the scrolling speed. Dictating a continuous scrolling command in the same direction twice stops the scrolling.

During continuous scrolling, you can dictate a number between 0 and 99 to change the scrolling speed. The resulting speed is the user.mouse_continuous_scroll_amount setting multiplied by the number you dictated divided by the user.mouse_continuous_scroll_speed_quotient setting (which defaults to 10). With default settings, dictating 5 gives you half speed and dictating 20 gives you double speed. Note: Because the scrolling speed has to be an integer number, changing the speed by a small amount like 1 might not change how fast scrolling actually happens depending on your settings. The final scrolling speed is chosen by rounding and enforcing a minimum speed of 1.
