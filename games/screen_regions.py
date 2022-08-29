from talon import actions, ctrl, ui, cron
from talon.canvas import Canvas, Rect
from math import sqrt

WIDTH = 1920
HEIGHT = 1080
canvas = None

WASD3 = [
    [ ["w","a"], ["w"], ["w","d"]  ],
    [ ["a"],     [],    ["d"]      ],
    [ ["a","s"], ["s"], ["d","s"] ]
]

WASD4 = [
    [ ["w","a"], ["w"], ["w"], ["w","d"]  ],
    [ ["a"],     [],    [],    ["d"]      ],
    [ ["a"],     [],    [],    ["d"]      ],
    [ ["a","s"], ["s"], ["s"], ["d","s"] ]
]

WASD5 = [
    [ ["w","a"], ["w"], ["w"], ["w"], ["w","d"]  ],
    [ ["a"],     [],    [],    [],    ["d"]      ],
    [ ["a"],     [],    [],    [],    ["d"]      ],
    [ ["a"],     [],    [],    [],    ["d"]      ],
    [ ["a","s"], ["s"], ["s"], ["s"], ["d","s"]  ]
]

def _get_splits(matrix):
    """given a two dimensional array (assumes every row has same number of columns), calculate the number of splits"""
    x_splits = len(matrix[0])
    y_splits = len(matrix[1])
    return (x_splits, y_splits)

def _get_index(matrix, width, height, x, y):
    """returns a tuple indexing into matrix based on the pixel coordinates from the screen"""
    x_splits, y_splits = _get_splits(matrix)
    w = width / x_splits
    h = height / y_splits
    j = divmod(x, w)[0]
    i = divmod(y, h)[0]
    return (int(i), int(j))

def _get_from_regions(regions, x, y):
    """returns the element pointed to by pixels provided"""
    i, j = _get_index(regions, WIDTH, HEIGHT, x, y)
    return regions[i][j]

def collect_keys(regions):
    keys = set()
    for i in regions:
        for j in regions:
            keys.update(j)
    return keys

def get_from_regions(regions):
    """returns the element pointed to by the current mouse position"""
    x, y = ctrl.mouse_pos()
    i, j = _get_index(regions, WIDTH, HEIGHT, x, y)
    return regions[i][j]

def nop():
    print("nop")

def hold(*args):
    def op():
        for name in args:
            actions.key(name + ":down")
    return op

def tap(name):
    return lambda: actions.key(name)

def short_hold(k):
    def op():
        actions.key(k + ":down")
        actions.sleep(0.2)
        actions.key(k + ":up")
    return op

def hide_overlay():
    global canvas
    if canvas:
        canvas.close()
        canvas = None

def show_overlay(regions):
    global canvas
    hide_overlay()
    x_splits, y_splits = _get_splits(regions)
    w = WIDTH / x_splits
    h = HEIGHT / y_splits
    def on_draw(c):
        c.paint.stroke_width = 5
        c.paint.color = "FF69B4"
        for n in range(0, x_splits):
            for m in range(0, y_splits):
                x = n * w
                y = m * h
                key = _get_from_regions(regions, x + w / 2, y + h / 2)
                #if len(key) > 0:
                c.paint.style = c.paint.Style.STROKE
                c.draw_rect(Rect(x,y,w,h))
                c.paint.typeface = "arial"
                c.paint.style = c.paint.Style.FILL
                c.paint.textsize = round(h / 2)
                text = ",".join(key)
                rect = c.paint.measure_text(text)[1]
                xt = x + w / 2 - rect.x - rect.width / 2
                yt = y + h / 2 + rect.height / 2
                c.draw_text(text, xt, yt)
        #cron.after("10s", canvas.close)
    canvas = Canvas.from_rect(ui.screens()[0].rect)
    canvas.register("draw", on_draw)
    canvas.freeze()
