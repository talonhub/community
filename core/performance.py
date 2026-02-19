from talon import Context, Module, actions, app, imgui, ui, resource, canvas, ctrl, settings, cron
import time

mod = Module()

start = None
end = None

@mod.action_class
class Actions:
    def performance_start():
        """start perf counter"""
        global start, end
        start = time.perf_counter()

    def performance_end():
        """end perf counter"""
        global start, end
        end = time.perf_counter()
        print(f"Execution time: {ui.active_app().name} {end - start:.6f} seconds")


