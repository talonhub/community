# From splondike
from talon.scripting import global_speech_system
from talon import actions, canvas, ui, ctrl, cron
from talon.types import Rect

display_canvas = False


def _draw(canvas):
    paint = canvas.paint
    paint.textsize = 24
    canvas.clear("ffffff00")
    paint.color = "ffffffff"
    canvas.draw_text(text, canvas.x + 30, canvas.y + 30)


def reposition_canvas():
    x, y = ctrl.mouse_pos()
    print(x, y)
    can.move(x, y)


if display_canvas:
    can = canvas.Canvas.from_rect(Rect(453, 766, 800, 50))
    can.register("draw", _draw)
    can.show()
    can.freeze()

text = ""
# cron.interval("1s", reposition_canvas)
# reposition_canvas()


def hide_canvas():
    can.hide()


def _log(args):
    global text, can
    text = f"\"{' '.join(args['text'])}\""
    can.show()
    can.freeze()
    cron.after("1s", hide_canvas)


if display_canvas:
    global_speech_system.register("phrase", _log)
