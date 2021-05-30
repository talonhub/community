# From splondike
from talon.scripting import global_speech_system
from talon import actions, canvas, ui, ctrl, cron, Module, scope
from talon.types import Rect

mod = Module()

# Can be no-overlay, gif-capture, or screenshare
mode = "no-overlay"
# mode = "gif-capture"
# mode = "screenshare"

display_canvas = mode != "no-overlay"

if mode == "gif-capture":
    action_wait = "1s"
    canvas_hide_wait = "1500ms"
elif mode == "screenshare":
    action_wait = "0s"
    canvas_hide_wait = "2000ms"


def _draw(canvas: canvas.Canvas):
    paint = canvas.paint
    paint.textsize = 36
    canvas.clear("ffffff00")
    paint.color = "ffffffff"
    canvas.draw_text(text, canvas.x + 30, canvas.y + 30)


def reposition_canvas():
    x, y = ctrl.mouse_pos()
    print(x, y)
    can.move(x, y)


if display_canvas:
    can = canvas.Canvas.from_rect(Rect(424, 762, 800, 50))
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
    if "command" not in scope.get("mode"):
        return
    text = f"\"{' '.join(args['text'])}\""
    can.show()
    can.freeze()
    actions.sleep(action_wait)
    cron.after(canvas_hide_wait, hide_canvas)


if display_canvas:
    global_speech_system.register("phrase", _log)


@mod.action_class
class Actions:
    def move_overlay():
        """Move the overlay."""
        reposition_canvas()