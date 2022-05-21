# written by timo, based on mousegrid written by timo and cleaned up a lot by aegis, heavily heavily edited by Tara 
from talon import Module, Context, app, actions, canvas, screen, settings, ui, ctrl, cron, registry
from talon.skia import Shader, Color, Paint, Rect
from talon.types.point import Point2d
from talon_plugins import eye_mouse, eye_zoom_mouse
from typing import Union

import math, time, string

import typing

def hx(v: int) -> str:
    return '{:02x}'.format(v)

mod = Module()

mod.tag("full_mouse_grid_showing", desc="Tag indicates whether the full mouse grid is showing")
mod.tag("full_mouse_grid_enabled", desc="Tag enables the full mouse grid commands.")
mod.list("mg_point_of_compass", desc="point of compass for full mouse grid")

mod.mode("full_mouse_grid", desc="indicate the full mouse grid is active")

setting_letters_background_color = mod.setting(
    "full_mouse_grid_letters_background_color",
    type=str,
    default="000000",
    desc="set the background color of the small letters in the full mouse grid",
)

setting_row_highlighter = mod.setting(
    "full_mouse_grid_row_highlighter",
    type=str,
    default="ff0000",
    desc="set the color of the row to highlight",
)

setting_large_number_color = mod.setting(
    "full_mouse_grid_large_number_color",
    type=str,
    default="00ffff",
    desc="sets the color of the large number label in the superblock",
)

setting_small_letters_color = mod.setting(
    "full_mouse_grid_small_letters_color",
    type=str,
    default="ffff55",
    desc="sets the color of the small letters label in the superblock",
)

setting_superblock_background_color = mod.setting(
    "full_mouse_grid_superblock_background_color",
    type=str,
    default="ff55ff",
    desc="sets the background color of the superblock",
)

setting_superblock_stroke_color = mod.setting(
    "full_mouse_grid_superblock_stroke_color",
    type=str,
    default="ffffff",
    desc="sets the background color of the superblock",
)

setting_field_size = mod.setting(
    "full_mouse_grid_field_size",
    type=str,
    default="32",
    desc="sets the default size of the small grid blocks",
)

setting_superblock_transparency = mod.setting(
    "full_mouse_grid_superblock_transparency",
    type=str,
    default="0x22",
    desc="sets the transparency of the superblocks",
)

setting_label_transparency = mod.setting(
    "full_mouse_grid_label_transparency",
    type=str,
    default="0x99",
    desc="sets the transparency of the labels",
)

dense_grid_startup_mode = mod.setting(
    "full_mouse_grid_startup_mode",
    type=str,
    default="phonetic",
    desc="determines which mode the grid will be in each time the grid is reopened.",
)

setting_dense_grid_font = mod.setting(
    "full_mouse_grid_font",
    type=str,
    default="arial rounded mt",
    desc="determines the default font",
)


ctx = Context()

ctx.matches = r"""
tag: user.full_mouse_grid_enabled
"""

# stolen from the race car, this should probably go in a central spot somewhere
direction_name_steps = [
        "east", "east south east", "south east", "south south east",
        "south", "south south west", "south west", "west south west",
        "west", "west north west", "north west", "north north west",
        "north", "north north east", "north east", "east north east"]

direction_vectors = [Point2d(0, 0) for i in range(len(direction_name_steps))]

direction_vectors[0]  = Point2d(1, 0)
direction_vectors[4]  = Point2d(0, 1)
direction_vectors[8]  = Point2d(-1, 0)
direction_vectors[12] = Point2d(0, -1)

for i in [2, 6, 10, 14]:
    direction_vectors[i] = direction_vectors[(i - 2) % len(direction_vectors)] + direction_vectors[(i + 2) % len(direction_vectors)]

for i in [1, 3, 5, 7, 9, 11, 13, 15]:
    direction_vectors[i] = (direction_vectors[(i - 1) % len(direction_vectors)] + direction_vectors[(i + 1) % len(direction_vectors)]) / 2

ctx.lists["self.mg_point_of_compass"] = direction_name_steps

print(ctx.lists["self.mg_point_of_compass"])

letters = string.ascii_lowercase ## where the letters come from.  :0#

class MouseSnapMillion:
    def __init__(self):
        self.screen = None
        self.rect = None 
        self.history = []
        self.img = None
        self.mcanvas = None
        self.active = False
        self.was_control_mouse_active = False
        self.was_zoom_mouse_active = False
        self.columns = 0
        self.rows = 0

        self.label_transparency = 0x99
        self.bg_transparency = 0x22

        self.saved_label_transparency = 0x99 
        self.saved_bg_transparency = 0x22
        self.field_size = 20 

        self.superblocks = []

        self.default_superblock = 0

        self.rulers = False
        self.checkers = False
        self.pattern = ""

        self.input_so_far = ""

    def add_partial_input(self, letter: str):
        
        # this logic swaps around which superblock is selected. 
        if letter.isdigit():
            print("user inputted a number, switching superblock")
            self.default_superblock = int(letter) - 1
            if self.mcanvas:
                self.mcanvas.freeze()
                print("updating graphics")
            return

        #this logic collects letters.  you can only collect up to two letters. 
        self.input_so_far += letter
        print("input so far: " + self.input_so_far)
        if len(self.input_so_far) >= 2:
            self.jump(self.input_so_far, self.default_superblock )
            self.input_so_far = ""

            # this next line fixes a bug where a tag was not deactivated and a mode was not being switched properly.  However, I think this stuff might be best properly stached in the object's close functionality, because it is triggered when you close the grid. 

            # actions.user.full_grid_close()

        if self.mcanvas:
            self.mcanvas.freeze()
            print("updating graphics")

    def adjust_bg_transparency(self, amount: int):
        self.bg_transparency += amount
        if self.bg_transparency < 0: self.bg_transparency = 0
        if self.bg_transparency > 255: self.bg_transparency = 255
        if self.mcanvas:
            self.mcanvas.freeze()

    def adjust_label_transparency(self, amount: int):
        self.label_transparency += amount
        if self.label_transparency < 0: self.label_transparency = 0
        if self.label_transparency > 255: self.label_transparency = 255
        if self.mcanvas:
            self.mcanvas.freeze()

    def set_bg_transparency(self, amount: int):
        self.bg_transparency = amount
        if self.bg_transparency < 0: self.label_transparency = 0
        if self.bg_transparency > 255: self.label_transparency = 255
        if self.mcanvas:
            self.mcanvas.freeze()

    def set_label_transparency(self, amount: int):
        self.label_transparency = amount
        if self.label_transparency < 0: self.label_transparency = 0
        if self.label_transparency > 255: self.label_transparency = 255
        if self.mcanvas:
            self.mcanvas.freeze()

    def adjust_field_size(self, amount: int):


        self.field_size += amount
        if self.field_size < 5: self.field_size = 5
        # columns and rows depend on field size and window size, but it doesn't recalculate automatically. I should fix that.

        self.columns = int(self.rect.width  // self.field_size)
        self.rows    = int(self.rect.height // self.field_size)
        self.superblocks = []

        self.show()

        if self.mcanvas:
            self.mcanvas.freeze()

    def setup(self, *, rect: Rect = None, screen_num: int = None):
        # get informaition on number and size of screens 

        screens = ui.screens()
        # each if block here might set the rect to None to indicate failure
        # rect is information on the height and width of the canvas.  
        if rect is not None:
            try:
                screen = ui.screen_containing(*rect.center)
            except Exception:
                rect = None

        # 
        if rect is None and screen_num is not None:
            screen = screens[screen_num % len(screens)]
            rect = screen.rect

        # rect determines which screen to draw on. 
        # if there is no rectangle to draw on canvas
            # get the first screen
            # set the rect to the area of the first screen.  
        if rect is None:
            screen = screens[0]
            rect = screen.rect

        # store the current rectangle we are drawing on
        self.rect = rect.copy()

        # store the current screen we are drawing on. 
        self.screen = screen

        #leftover code from the mousegrid, currently unused. 
        self.img = None


        # set the field size
        self.field_size = int(setting_field_size.get())

        # use the field size to calculate how many rows and how many columns there are set how many columns and how may rows there are.

        self.columns =  int(self.rect.width  // self.field_size)
        self.rows    =  int(self.rect.height // self.field_size)

        # set the label transparency 
        self.label_transparency = int(setting_label_transparency.get(), 16)
        
        # set the background transparency
        self.bg_transparency = int(setting_superblock_transparency.get(), 16)

        self.history = []

        self.active = False

        self.was_control_mouse_active = False
        self.was_zoom_mouse_active = False

        ## This is messy stuff, but below this line it's all variables used as storage.

        self.superblocks = []

        self.default_superblock = 0

        self.rulers = False
        self.checkers = False
        self.pattern = "phonetic"

        self.input_so_far = ""

                # close the old canvas, if one exists, and open a new one.  
        if self.mcanvas is not None:
            self.mcanvas.close()
        self.mcanvas = canvas.Canvas.from_screen(screen)
        if self.active:
            self.mcanvas.register("draw", self.draw)
            self.mcanvas.freeze()

    def show(self):
        if self.active:
            return
        # noinspection PyUnresolvedReferences
        if eye_zoom_mouse.zoom_mouse.enabled:
            self.was_zoom_mouse_active = True
            eye_zoom_mouse.toggle_zoom_mouse(False)
        if eye_mouse.control_mouse.enabled:
            self.was_control_mouse_active = True
            eye_mouse.control_mouse.toggle()

        self.bg_transparency = self.saved_bg_transparency
        self.label_transparency = self.saved_label_transparency
        
        self.mcanvas.register("draw", self.draw)
        self.mcanvas.freeze()
        self.active = True

        # actions.user.full_mouse_grid_help_overlay_show()

    def hide(self):

        self.saved_label_transparency = self.label_transparency 
        self.saved_bg_transparency = self.bg_transparency

        self.bg_transparency = 0x00
        self.label_transparency = 0x00
        if(self.mcanvas):
                self.mcanvas.freeze()

    def close(self):
        if not self.active:
            return
        self.hide()
        self.mcanvas.unregister("draw", self.draw)
        #self.mcanvas.close()
        #self.mcanvas = None
        self.img = None
        self.input_so_far = ""

        # actions.user.mouse_grid_help_overlay_close()

        self.active = False
        if self.was_control_mouse_active and not eye_mouse.control_mouse.enabled:
            eye_mouse.control_mouse.toggle()
        if self.was_zoom_mouse_active and not eye_zoom_mouse.zoom_mouse.enabled:
            eye_zoom_mouse.toggle_zoom_mouse(True)

        self.was_zoom_mouse_active = False
        self.was_control_mouse_active = False



    def draw(self, canvas):
        paint = canvas.paint
        print("*********i'm drawing with a field size of " + str(self.field_size))
        #self.field_size = int(setting_field_size.get())

        # for other-screen or individual-window grids
        canvas.translate(self.rect.x, self.rect.y)
        canvas.clip_rect(Rect(-self.field_size * 2, -self.field_size * 2, self.rect.width + self.field_size * 4, self.rect.height + self.field_size * 4))

        crosswidth = 6

        def draw_crosses():
            for row in range(1, self.rows):
                for col in range(1, self.columns):
                    cx = self.field_size * col
                    cy = self.field_size * row

                    canvas.save()
                    canvas.translate(0.5, 0.5)

                    canvas.draw_line(cx - crosswidth + 0.5, cy, cx + crosswidth - 0.5, cy)
                    canvas.draw_line(cx, cy + 0.5, cx, cy + crosswidth - 0.5)
                    canvas.draw_line(cx, cy - crosswidth + 0.5, cx, cy - 0.5)

                    canvas.restore()

        def draw_superblock():

            superblock_size = len(letters) * self.field_size

            colors = ["000055", "665566", "554444", "888855", "aa55aa", "55cccc"] * 100
            num = 1

            self.superblocks = []

            skipped_superblock = self.default_superblock + 1

            if int(self.rect.height) // superblock_size == 0 and int(self.rect.width) // superblock_size == 0:
                skipped_superblock = 1

            for row in range(0, int(self.rect.height) // superblock_size + 1):
                for col in range(0, int(self.rect.width) // superblock_size + 1):
                    canvas.paint.color = colors[(row + col) % len(colors)] + hx(self.bg_transparency)

                    #canvas.paint.color = "ffffff"
                    canvas.paint.style = Paint.Style.FILL
                    blockrect = Rect(
                            col * superblock_size,
                            row * superblock_size,
                            superblock_size,
                            superblock_size)
                    blockrect.right = min(blockrect.right, self.rect.width)
                    blockrect.bot = min(blockrect.bot, self.rect.height)
                    canvas.draw_rect(blockrect)

                    if skipped_superblock != num:

                        #attempt to change backround color on the superblock chosen 

                        #canvas.paint.color = colors[(row + col) % len(colors)] + hx(self.bg_transparency)

                        canvas.paint.color = setting_superblock_background_color.get() + hx(self.bg_transparency)
                        canvas.paint.style = Paint.Style.FILL
                        blockrect = Rect(
                                col * superblock_size,
                                row * superblock_size,
                                superblock_size,
                                superblock_size)
                        blockrect.right = min(blockrect.right, self.rect.width)
                        blockrect.bot = min(blockrect.bot, self.rect.height)
                        canvas.draw_rect(blockrect)

                        canvas.paint.color = setting_superblock_stroke_color.get() + hx(self.bg_transparency)
                        canvas.paint.style = Paint.Style.STROKE
                        canvas.paint.stroke_width = 5
                        blockrect = Rect(
                                col * superblock_size,
                                row * superblock_size,
                                superblock_size,
                                superblock_size)
                        blockrect.right = min(blockrect.right, self.rect.width)
                        blockrect.bot = min(blockrect.bot, self.rect.height)
                        canvas.draw_rect(blockrect)

                        #drawing the big number in the background

                        canvas.paint.style = Paint.Style.FILL
                        canvas.paint.textsize = int(superblock_size)
                        text_rect = canvas.paint.measure_text(str(num))[1]
                        #text_rect.center = blockrect.center
                        text_rect.x = blockrect.x
                        text_rect.y = blockrect.y
                        canvas.paint.color = setting_large_number_color.get() + hx(self.bg_transparency)
                        canvas.draw_text(
                                str(num),
                                text_rect.x,
                                text_rect.y + text_rect.height
                                )

                    self.superblocks.append(blockrect.copy())

                    num += 1


        def draw_text(): 

            canvas.paint.text_align = canvas.paint.TextAlign.CENTER
            canvas.paint.textsize = 17
            canvas.paint.typeface = setting_dense_grid_font.get()
            #canvas.paint.typeface = "arial rounded mt"

            skip_it = False

            for row in range(0, self.rows + 1):
                for col in range(0, self.columns + 1):

                    if self.pattern == "checkers":
                        if ( row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                            skip_it = True
                        else:
                            skip_it = False

                    if self.pattern == "frame" or self.pattern == "phonetic":
                        if ( row % 26 == 0) or (col % 26 == 0):
                            skip_it = False
                        else:
                            skip_it = True

                    #draw the highlighter

                    base_rect = self.superblocks[self.default_superblock].copy()
                    #print(base_rect)

                    if row >= (base_rect.y / self.field_size) and row <= (base_rect.y / self.field_size + len(letters)) and col >= (base_rect.x /self.field_size) and col <=  (base_rect.x / self.field_size + len(letters))  :
                        within_selected_superblock = True

                        if within_selected_superblock and len(self.input_so_far) == 1 and self.input_so_far.startswith(letters[row % len(letters)]):
                            skip_it = False


                    if not (skip_it):
                        draw_letters(row,col)


        def draw_letters(row, col):
            #get letters
            text_string = f"{letters[row % len(letters)]}{letters[col % len(letters)]}" #gets a letter from the alphabet of the form 'ab' or 'DA'
            # this the measure text is the box around the text.  
            canvas.paint.textsize = int(self.field_size * 3 / 5)
            #canvas.paint.textsize = int(field_size*4/5)
            text_rect = canvas.paint.measure_text(text_string)[1] #find out how many characters long the text is?

            background_rect = text_rect.copy()
            background_rect.center = Point2d(
                col * self.field_size + self.field_size / 2,
                row * self.field_size + self.field_size / 2,
            )  #I think this re-centers the point?  
            background_rect = background_rect.inset(-4)

            # remove distracting letters from frame mode frames. 
            if self.pattern == "frame":
                if(letters[row % len(letters)] == 'a'):

                    text_string = f"{letters[col % len(letters)]}" #gets a letter from the alphabet of the form 'ab' or 'DA'
                    # this the measure text is the box around the text.  
                    canvas.paint.textsize = int(self.field_size * 3 / 5)
                    #canvas.paint.textsize = int(field_size*4/5)
                    text_rect = canvas.paint.measure_text(text_string)[1] #find out how many characters long the text is?
                    background_rect = text_rect.copy()
                    background_rect.center = Point2d(
                        col * self.field_size + self.field_size / 2,
                        row * self.field_size + self.field_size / 2,
                    )  #I think this re-centers the point?  
                    background_rect = background_rect.inset(-4) 
                elif(letters[col % len(letters)] == 'a'):
                    text_string = f"{letters[row % len(letters)]}"

                    canvas.paint.textsize = int(self.field_size * 3 / 5)
                    #canvas.paint.textsize = int(field_size*4/5)
                    text_rect = canvas.paint.measure_text(text_string)[1] #10find out how many characters long the text is?

                    background_rect = text_rect.copy()
                    background_rect.center = Point2d(
                        col * self.field_size + self.field_size / 2,
                        row * self.field_size + self.field_size / 2,
                    )  #I think this re-centers the point?  
                    background_rect = background_rect.inset(-4)

            elif self.pattern == "phonetic":
                if(letters[row % len(letters)] == 'a'):

                    text_string = f"{letters[col % len(letters)]}" #gets a letter from the alphabet of the form 'ab' or 'DA'
                    # this the measure text is the box around the text.  
                    canvas.paint.textsize = int(self.field_size * 3 / 5)
                    #canvas.paint.textsize = int(field_size*4/5)
                    text_rect = canvas.paint.measure_text(text_string)[1] #find out how many characters long the text is?
                    background_rect = text_rect.copy()
                    background_rect.center = Point2d(
                        col * self.field_size + self.field_size / 2,
                        row * self.field_size + self.field_size / 2,
                    )  #I think this re-centers the point?  
                    background_rect = background_rect.inset(-4) 
                elif(letters[col % len(letters)] == 'a'):
                    

                    text_string = f"{list(registry.lists['user.letter'][0].keys())[row%len(letters)]}" #gets the phonetic words currently being used
                    
                    canvas.paint.textsize = int(self.field_size * 3 / 5)
                    #canvas.paint.textsize = int(field_size*4/5)
                    text_rect = canvas.paint.measure_text(text_string)[1] #10find out how many characters long the text is?

                    background_rect = text_rect.copy()
                    background_rect.center = Point2d(
                        col * self.field_size + self.field_size / 2,
                        row * self.field_size + self.field_size / 2,
                    )  #I think this re-centers the point?  
                    background_rect = background_rect.inset(-4) 

            if not (self.input_so_far.startswith(letters[row % len(letters)]) or
                    len(self.input_so_far) > 1 and self.input_so_far.endswith(letters[col % len(letters)])):
                canvas.paint.color = setting_letters_background_color.get() + hx(self.label_transparency)
                canvas.paint.style = Paint.Style.FILL
                canvas.draw_rect(background_rect)
                canvas.paint.color = setting_small_letters_color.get() +hx(self.label_transparency)
                #paint.style = Paint.Style.STROKE
                canvas.draw_text(
                    text_string,
                    col * self.field_size + self.field_size / 2,
                    row * self.field_size + self.field_size / 2 + text_rect.height / 2
                )

            # sees if the background schould be highlighted
            elif (self.input_so_far.startswith(letters[row % len(letters)]) or
                    len(self.input_so_far) > 1 and self.input_so_far.endswith(letters[col % len(letters)])):
                #draw columns of phonetic words

                phonetic_word = list(registry.lists['user.letter'][0].keys())[col%len(letters)]
                letter_list = list(phonetic_word)
                for index, letter in enumerate(letter_list):
                    if index == 0: 
                        canvas.paint.color = setting_row_highlighter.get() + hx(self.label_transparency) #check if someone has said a letter and highlight a row, or check if two letters have been said and highlight a column
            #colors it the ordinary background. 
                        text_string = f"{letter}" # gets a letter from the alphabet of the form 'ab' or 'DA'
                # this the measure text is the box around the text.  
                        canvas.paint.textsize = int(self.field_size * 3 / 5)
                    #canvas.paint.textsize = int(field_size*4/5)
                        text_rect = canvas.paint.measure_text(text_string)[1] #find out how many characters long the text is?

                        background_rect = text_rect.copy()
                        background_rect.center = Point2d(
                            col * self.field_size + self.field_size / 2,
                            row * self.field_size + (self.field_size / 2 + text_rect.height / 2) * (index +1 ) 
                        )  #I think this re-centers the point?  
                        background_rect = background_rect.inset(-4) 
                        canvas.draw_rect(background_rect)
                        canvas.paint.color = setting_small_letters_color.get() +hx(self.label_transparency)
                        #paint.style = Paint.Style.STROKE
                        canvas.draw_text(
                            text_string,
                            col * self.field_size + (self.field_size / 2),
                            row * self.field_size + (self.field_size / 2 + text_rect.height / 2) * (index + 1)
                        )
          
                    elif self.pattern == 'phonetic':
                        canvas.paint.color = setting_letters_background_color.get() + hx(self.label_transparency)
                        text_string = f"{letter}" # gets a letter from the alphabet of the form 'ab' or 'DA'
                # this the measure text is the box around the text.  
                        canvas.paint.textsize = int(self.field_size * 3 / 5)
                    #canvas.paint.textsize = int(field_size*4/5)
                        text_rect = canvas.paint.measure_text(text_string)[1] #find out how many characters long the text is?

                        background_rect = text_rect.copy()
                        background_rect.center = Point2d(
                            col * self.field_size + self.field_size / 2,
                            row * self.field_size + (self.field_size / 2 + text_rect.height / 2) * (index +1 ) 
                        )  #I think this re-centers the point?  
                        background_rect = background_rect.inset(-4) 
                        canvas.draw_rect(background_rect)
                        canvas.paint.color = setting_small_letters_color.get() +hx(self.label_transparency)
                        #paint.style = Paint.Style.STROKE
                        canvas.draw_text(
                            text_string,
                            col * self.field_size + (self.field_size / 2),
                            row * self.field_size + (self.field_size / 2 + text_rect.height / 2) * (index + 1)
                        )



        def draw_rulers():
            for (x_pos, align) in [(-3, canvas.paint.TextAlign.RIGHT), (self.rect.width + 3, canvas.paint.TextAlign.LEFT)]:
                canvas.paint.text_align = align
                canvas.paint.textsize = 17
                canvas.paint.color = "ffffffff"

                for row in range(0, self.rows + 1):
                    text_string = letters[row % len(letters)] + "_"
                    text_rect = canvas.paint.measure_text(text_string)[1]
                    background_rect = text_rect.copy()
                    background_rect.x = x_pos
                    background_rect.y = row * self.field_size + self.field_size / 2 + text_rect.height / 2
                    canvas.draw_text(
                        text_string,
                        background_rect.x,
                        background_rect.y
                    )

            for y_pos in [-3, self.rect.height + 3 + 17]:
                canvas.paint.text_align = canvas.paint.TextAlign.CENTER
                canvas.paint.textsize = 17
                canvas.paint.color = "ffffffff"
                for col in range(0, self.columns + 1):
                    text_string = "_" + letters[col % len(letters)]
                    text_rect = canvas.paint.measure_text(text_string)[1]
                    background_rect = text_rect.copy()
                    background_rect.x = col * self.field_size + self.field_size / 2
                    background_rect.y = y_pos
                    canvas.draw_text(
                        text_string,
                        background_rect.x,
                        background_rect.y
                    )
                    

        #paint.color = "00ff004f"
        #draw_crosses()
        paint.color = "ffffffff"

        #paint.stroke_width = 1
        #paint.color = "ff0000ff"
        draw_superblock()
        draw_text()

        if self.rulers:
            draw_rulers()

        # draw_grid(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        # paint.textsize += 12 - self.count * 3
        # draw_text(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def calc_narrow(self, which, rect):
        rect = rect.copy()
        # bdr = narrow_expansion.get()
        row = int(which - 1) // 3
        col = int(which - 1) % 3
        if settings["user.grids_put_one_bottom_left"]:
            row = 2 - row
        rect.x += int(col * rect.width // 3) - bdr
        rect.y += int(row * rect.height // 3) - bdr
        rect.width = (rect.width // 3) + bdr * 2
        rect.height = (rect.height // 3) + bdr * 2
        return rect

    def narrow(self, which, move=True):
        if which < 1 or which > 9:
            return
        self.save_state()
        rect = self.calc_narrow(which, self.rect)
        # check count so we don't bother zooming in _too_ far
        if self.count < 5:
            self.rect = rect.copy()
            self.count += 1
        if move:
            ctrl.mouse_move(*rect.center)
        if self.count >= 2:
            self.update_screenshot()
        else:
            self.mcanvas.freeze()

    def jump(self, spoken_letters, number = -1, compasspoint = None):
        
        base_rect = self.superblocks[number].copy()
        base_rect.x += self.rect.x
        base_rect.y += self.rect.y
        #spoken_letters = spoken_letters.upper()

        x_idx = letters.index(spoken_letters[1])
        y_idx = letters.index(spoken_letters[0])

        if compasspoint != None:
            index = direction_name_step.index(compasspoint)
            point = direction_vectors[index]
            
        else:
            point = Point2d(0,0)  

        ctrl.mouse_move(
            point.x + base_rect.x + x_idx * self.field_size + self.field_size / 2,
            point.y + base_rect.y + y_idx * self.field_size + self.field_size / 2)

        self.input_so_far = ""

        if self.mcanvas:
            self.mcanvas.freeze()

    def turn_on_checkers(self):
        self.pattern = "checkers"
        if self.mcanvas:
            self.mcanvas.freeze()

    def turn_on_frame(self):
        self.pattern = "frame"
        if self.mcanvas:
            self.mcanvas.freeze()

    def turn_on_full(self):
        self.pattern = "none"
        if self.mcanvas:
            self.mcanvas.freeze()

    def turn_on_phonetic(self):
        self.pattern = "phonetic"
        if self.mcanvas:
            self.mcanvas.freeze()

    def toggle_rulers(self):
        self.rulers = not self.rulers
        if self.mcanvas:
            self.mcanvas.freeze()

mg = MouseSnapMillion()

def full_mouse_grid_mode_enable():
    actions.mode.enable("user.full_mouse_grid")
    actions.mode.disable("command")

def full_mouse_grid_mode_disable():
    actions.mode.disable("user.full_mouse_grid")
    actions.mode.enable("command")

@mod.action_class
class GridActions:
    def full_grid_activate():
        """Show mouse grid"""
        
        #rect = screen.rect
        if mg.mcanvas == None:
            print("setting up")
            mg.setup()
            mg.turn_on_frame()
        elif mg.rect != ui.screens()[0].rect:
            mg.setup()
            mg.turn_on_frame()

        mg.show()

        ctx.tags = ["user.full_mouse_grid_showing"]
        print("==== SHOWING GRID NAO ====")

    def full_grid_place_window():
        """Places the grid on the currently active window"""
        if mg.mcanvas == None: 
            mg.setup(rect=ui.active_window().rect)
        else:
            mg.setup(rect=ui.active_window().rect)
        mg.show()
        ctx.tags = ["user.full_mouse_grid_showing"]
        print("==== SHOWING GRID NAO ====")
        #full_mouse_grid_mode_enable()

    def full_grid_select_screen(screen: int):
        """Brings up mouse grid"""
        
        screen_num = screen
        if mg.mcanvas == None:
            print("setting up")
            mg.setup(screen_num=screen - 1)
        elif mg.rect != ui.screens()[screen_num-1].rect:
            mg.setup(rect = ui.screens()[screen_num-1].rect)

        mg.show()

        ctx.tags = ["user.full_mouse_grid_showing"]
        print("==== SHOWING GRID NAO Screen ====")
        #full_mouse_grid_mode_enable()

    #def grid_narrow_list(digit_list: typing.List[str]):
        #"""Choose fields multiple times in a row"""
        #for d in digit_list:
            #actions.user.grid_narrow(int(d))

    #def grid_narrow(digit: Union[int, str]):
        #"""Choose a field of the grid and narrow the selection down"""
        #mg.narrow(int(digit))

    #def grid_go_back():
        #"""Sets the grid state back to what it was before the last command"""
        #mg.go_back()



    def full_grid_close():
        """Close the active grid"""
        print(mg.mcanvas)
        ctx.tags = []
        mg.close()

        print("==== NO MORE GRID FOR YOU MY FRIEND ====")
        #full_mouse_grid_mode_disable()

    def full_grid_checkers():
        """Show or hide every other label box so more of the underlying screen content is visible"""
        mg.turn_on_checkers()

    def full_grid_frame():
        """Show or hide rulers all around the window"""
        mg.turn_on_frame()

    def full_grid_full():
        """toggle full mouse grid on"""
        mg.turn_on_full()

    def full_grid_phonetic():
        """toggle phonetic mouse grid on"""
        mg.turn_on_phonetic()

    def full_grid_rulers_toggle():
        """Show or hide rulers all around the window"""
        mg.toggle_rulers()
         

    def full_grid_adjust_bg_transparency(amount: int) -> int:
        """Increase or decrease the opacity of the background of the full mouse grid (also returns new value)"""
        mg.adjust_bg_transparency(amount)
        return mg.bg_transparency

    def full_grid_adjust_label_transparency(amount: int) -> int:
        """Increase or decrease the opacity of the labels behind text for the full mouse grid (also returns new value)"""
        mg.adjust_label_transparency(amount)
        return mg.label_transparency


    def full_grid_adjust_size(amount: int):
        """increase or decrease size of everything"""
        mg.adjust_field_size(amount)


    def full_grid_input_partial(letter: str):
        """Input one letter to highlight a row or column"""
        mg.add_partial_input(str(letter))

    def full_grid_input_horizontal(letter:str):
        """This command is for if you chose the wrong row and you want to choose a different row before choosing a column"""
        mg.input_so_far = ""
        mg.add_partial_input(str(letter))


