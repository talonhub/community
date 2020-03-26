# From https://github.com/talonvoice/examples/blob/master/noise.py
import time

from talon import ctrl
from talon import tap
from talon import noise
from talon.track.geom import Point2d

class NoiseModel:
    def __init__(self):
        self.hiss_start = 0
        self.hiss_last = 0
        self.button = 0
        self.mouse_origin = Point2d(0, 0)
        self.mouse_last = Point2d(0, 0)
        self.dragging = False

        tap.register(tap.MMOVE, self.on_move)
        noise.register('pop', self.on_pop)

    def on_move(self, typ, e):
        if typ != tap.MMOVE: return
        self.mouse_last = pos = Point2d(e.x, e.y)
        if self.hiss_start and not self.dragging:
            if (pos - self.mouse_origin).len() > 10:
                self.dragging = True
                self.button = 0
                x, y = self.mouse_origin.x, self.mouse_origin.y
                ctrl.mouse(x, y)
                ctrl.mouse_click(pos = (x, y), button=0, down=True)

    def on_pop(self, noise):
        now = time.time()
        ctrl.mouse_click(button=0, hold=16000)

model = NoiseModel()
