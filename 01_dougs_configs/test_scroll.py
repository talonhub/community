import threading
from talon import Module

class Scroller:
    def __init__(self):
        self.count = 0
        self.job = None
        self.lock = threading.RLock()

    def scroll(self, count: int):
        with self.lock:
            self.count += int(count)
            cron.cancel(self.job)
            self.tick()
            self.job = cron.interval('16ms', self.tick)

    def tick(self):
        with self.lock:
            if self.count == 0:
                self.cancel()
                return
            amount = settings.get('amount')
            if count < 0:
                amount = -amount
                self.count += 1
            else:
                self.count -= 1
            ctrl.mouse_scroll(y=int(amount))

    def cancel(self):
        with self.lock:
            cron.cancel(self.job)
            self.job = None

scroller = Scroller() 
mod = Module()

@mod.action_class
class Actions:
    def smooth_scroll():
        """Scrolls smoothly"""
        scroller.scroll(1)