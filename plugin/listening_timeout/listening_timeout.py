import time

from talon import Module, Context,  actions, cron, speech_system, ui, settings, app
from talon.canvas import Canvas

canvas: Canvas = None
mod = Module()
ctx = Context()
mod.setting("listening_timeout_minutes", int, default=-1, desc="After X mintues, disable speech recognition")
mod.setting("listening_timeout_show_notification", bool, default=True, desc="After the timeout expires, display a fullscreen notification")

@mod.action_class
class UserActions:
    def listening_timeout_expired():
        """Action called when the listening timeout expires"""
        actions.speech.disable()

        if settings.get("user.listening_timeout_show_notification"):
            show_notification()

@ctx.action_class("speech")
class SpeechActions:
    def enable():
        global last_phrase_time
        actions.next()
        start_timeout_job(calculate_timeout())
        last_phrase_time = time.perf_counter()
    
    def disable():
        stop_timeout_job()
        actions.next()
    
last_phrase_time = None
timeout_job = None

def start_timeout_job(timeout):
    global timeout_job
    cron.cancel(timeout_job)

    if timeout > 0:
        timeout_job = cron.after(f"{timeout}s", check_timeout)

def stop_timeout_job():
    global timeout_job
    cron.cancel(timeout_job)
    timeout_job = None

def calculate_timeout():
    return settings.get("user.listening_timeout_minutes") * 60

def check_timeout():
    global last_phrase_time, timeout_job
    timeout = calculate_timeout()
    if time.perf_counter() - last_phrase_time > timeout:
        actions.user.listening_timeout_expired()
        stop_timeout_job()
    elif timeout > 0:
        start_timeout_job(timeout)

def post_phrase(e):
    global last_phrase_time, timeout_job
    last_phrase_time = time.perf_counter()
    timeout = calculate_timeout()

    if timeout > 0:
        if actions.speech.enabled():
            start_timeout_job(timeout)
    else:
        stop_timeout_job()

def show_notification():
    def on_draw(c):
        c.paint.typeface = "Arial"
        c.paint.textsize = round(min(c.width, c.height) / 5)
        text = "sleep mode"
        rect = c.paint.measure_text(text)[1]
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        y = c.y + c.height / 2 + rect.height / 2

        c.paint.style = c.paint.Style.FILL
        c.paint.color = "eeeeee"
        c.draw_text(text, x, y)

        c.paint.style = c.paint.Style.STROKE
        c.paint.color = "000000"
        c.draw_text(text, x, y)

        cron.after("1s", canvas.close)

    screen = ui.main_screen()
    canvas = Canvas.from_rect(screen.rect)
    canvas.register("draw", on_draw)
    canvas.freeze()

def on_ready():
    global last_phrase_time
    last_phrase_time = time.perf_counter()

    # in case talon starts up with speech enabled,
    # let's attempt to respect the timeout
    if actions.speech.enabled():
        start_timeout_job(calculate_timeout())

    speech_system.register("post:phrase", post_phrase)

app.register("ready", on_ready)

