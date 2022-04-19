app: chrome
-
component: user.figma_component()
detach: user.figma_detach()
insert: user.figma_insert_component()

group: user.figma_group()
group out: user.figma_group_out()
frame: user.figma_frame_that()

set left: user.figma_set_left()
set right: user.figma_set_right()
set (up | top): user.figma_set_top()
set (down | bottom): user.figma_set_bottom()
set (center | horizontal): user.figma_set_horizontal()
set (middle | vertical): user.figma_set_vertical()

text center: user.figma_text_center()
text left: user.figma_text_left()
text right: user.figma_text_right()

tidy horizontal: user.figma_tidy_horizontal()
tidy vertical: user.figma_tidy_vertical()
tidy up: user.figma_tidy_up()

send back: user.figma_send_back()
send front: user.figma_send_front()
send up: user.figma_send_up()
send down: user.figma_send_down()

(hide | show): user.figma_hide()

auto: user.figma_autolayout_add()
auto out: user.figma_autolayout_remove()

toggle side: user.figma_toggle_ui()
search: user.figma_quick_actions()

move: user.figma_move()
use frame: user.figma_frame()
pen: user.figma_pen()
pencil: user.figma_pencil()
text: user.figma_text()
square: user.figma_rectangle()
circle: user.figma_ellipse()
line: user.figma_line()
arrow: user.figma_arrow()
ad comment: user.figma_comment()
color: user.figma_pick_color()
slice: user.figma_slice()
rulers: user.figma_rulers()

# Zooming in and out
zoom in |: user.figma_zoom_in()
zoom out: user.figma_zoom_out()

zout [<number>]: 
    key('-')
    repeat(number - 1)

zoon [<number>]:
    key('+')
    repeat(number - 1)

(zoom | zoo) (for | fall | full): user.figma_zoom_hundred()
(zoom | zoo) fit: user.figma_zoom_fit()
(zoom | zoo) select: user.figma_zoom_selection()
(zoom | zoo) pre: user.figma_zoom_previous_frame()
(zoom | zoo) next: user.figma_zoom_next_frame()

down page: user.figma_previous_page()
up page: user.figma_next_page()

be: user.figma_find_previous_frame()
as: user.figma_find_next_frame()

place image: user.figma_place_image()
paste here: user.figma_paste_here()
place here: user.figma_paste_replace()
deep: user.figma_deep_select()
(layer menu | laymen): user.figma_layer_menu_select()

rename: user.figma_rename()

style copy: user.figma_style_copy()
style paste: user.figma_style_paste()

run plugin: user.figma_run_plugin()

collapse: user.figma_collapse()

remove: user.figma_remove()

panel design: user.figma_paneldesign()
panel proto: user.figma_panelprototype()
panel inspect: user.figma_panelinspect()

# FigJam - Join + New Shape
joins:
    key("cmd-return")