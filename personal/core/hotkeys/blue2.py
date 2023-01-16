from talon import ui, Module, Context, registry, actions, imgui, cron, app

mod = Module()
ctx_zoom_mouse_enabled_use_pedal = Context()
ctx_zoom_mouse_enabled_use_pedal.matches = r"""
not user.running: Optikey Mouse
and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_pedal
"""


ctx_zoom_mouse_triggered_use_pedal = Context()
ctx_zoom_mouse_triggered_use_pedal.matches = r"""
tag: talon_plugins.eye_zoom_mouse.zoom_mouse_enabled
and tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
#and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_pedal
"""


@mod.action_class
class Actions:
    def blue2_s1():
        """document string goes here"""

    def blue2_s2():
        """document string goes here"""
        if app.platform == "mac":
            # actions.key("ctrl-f")
            actions.user.homerow_search("")
        elif app.platform == "windows":
            actions.key("ctrl-m")

    def blue2_s3():
        """document string goes here"""
        # actions.user.mouse_scroll_down()
        actions.mouse_scroll(20)

    def blue2_s4():
        """document string goes here"""
        # print('scroll up')
        # actions.user.mouse_scroll_up()
        actions.mouse_scroll(-20)

    def blue2_s5():
        """document string goes here"""

    def blue2_s6():
        """document"""

    def blue2_s7():
        """document string goes here"""
        actions.tracking.control_zoom_toggle()

    def blue2_s8():
        """document string goes here"""
        actions.user.microphone_toggle()
    


@ctx_zoom_mouse_enabled_use_pedal.action_class("user")
class WindowsZoomMouseInactiveActions:
    def blue2_s1():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def blue2_s2():
        """document string goes here"""
        if app.platform == "mac":
            # actions.key("cmd-shift-space")
            actions.user.homerow_search("")
        elif app.platform == "windows":
            actions.key("ctrl-m")

    def blue2_s3():
        """document string goes here"""
        actions.mouse_scroll(-20)

    def blue2_s4():
        """document string goes here"""
        # print('scroll up')
        actions.mouse_scroll(20)

    def blue2_s5():
        """document string goes here"""
        # actions.user.system_task_view()
        actions.user.system_switcher()

    def blue2_s6():
        """document"""
        actions.user.system_last_application()

    def blue2_s7():
        """document string goes here"""
        actions.tracking.control_zoom_toggle()

    def blue2_s8():
        """document string goes here"""
        actions.user.microphone_toggle()


@ctx_zoom_mouse_triggered_use_pedal.action_class("user")
class WindowsZoomMouseActiveActions:
    def blue2_s1():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def blue2_s2():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.right_click()

    def blue2_s3():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.double_click()

    def blue2_s4():
        """document string goes here"""
        print("triple")
        actions.talon_plugins.eye_zoom_mouse.triple_click()

    def blue2_s5():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_drag()

    def blue2_s6():
        """document"""
        actions.talon_plugins.eye_zoom_mouse.mouse_move()

    def blue2_s7():
        """document string goes here"""

    def blue2_s8():
        """document string goes here"""
