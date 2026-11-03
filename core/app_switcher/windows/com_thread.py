"""Run COM work on one thread of our own.

COM must be initialized on the thread that uses it, but initializing it on Talon's
threads (action, cron, event threads) fixes their apartment model, and Talon's own COM
use on those threads can then fail and abort the process. So all COM calls of the app
switcher and the thumbnail switcher (shell names and icons, installed apps, window
properties, virtual desktops) go through this single apartment-threaded thread.
"""

import ctypes
import functools
import queue
import sys
import threading
from concurrent.futures import Future

COINIT_APARTMENTTHREADED = 0x2
TIMEOUT_SECONDS = 5.0


class ComThread:
    # Bumped when the interface changes, so a hot reload replaces an older thread.
    VERSION = 3

    def __init__(self):
        self.requests: queue.Queue = queue.Queue()
        self.thread = threading.Thread(target=self._run, name="thumbnail switcher COM", daemon=True)
        self.thread.start()

    def _run(self):
        ctypes.windll.ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)
        while True:
            fn, future = self.requests.get()
            if fn is None:
                return
            try:
                future.set_result(fn())
            except BaseException as e:
                future.set_exception(e)

    def call(self, fn, *args, timeout: float = TIMEOUT_SECONDS, **kwargs):
        if threading.current_thread() is self.thread:
            return fn(*args, **kwargs)
        future: Future = Future()
        self.requests.put((functools.partial(fn, *args, **kwargs), future))
        return future.result(timeout)


# One thread for the life of Talon, kept across hot reloads.
_STASH = "_talon_thumbnail_switcher_com_thread"


def _worker() -> ComThread:
    worker = getattr(sys, _STASH, None)
    if worker is not None and getattr(worker, "VERSION", 1) != ComThread.VERSION:
        # Left from before a reload with a different interface: let it finish and stop.
        worker.requests.put((None, None))
        worker = None
    if worker is None or not worker.thread.is_alive():
        worker = ComThread()
        setattr(sys, _STASH, worker)
    return worker


def on_com_thread(fn=None, *, timeout: float = TIMEOUT_SECONDS):
    """Decorator: always run `fn` on the COM thread, waiting up to `timeout` seconds
    for its result. Use as @on_com_thread or @on_com_thread(timeout=60)."""

    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return _worker().call(fn, *args, timeout=timeout, **kwargs)

        return wrapper

    return decorate(fn) if fn is not None else decorate
