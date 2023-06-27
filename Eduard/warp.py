from talon import actions, Context, Module, ctrl
from talon_plugins import eye_mouse, eye_zoom_mouse
from talon_plugins.eye_mouse import config, toggle_camera_overlay, toggle_control

ctx = Context()
mod = Module()
@mod.action_class
class Actions:

   def kingfisher_click():
        """Activates the eyetracker for a brief second to move the mouse and clicks"""
        pos=ctrl.mouse_pos()
        actions.user.mouse_toggle_control_mouse()
        actions.sleep(0.4) 
        ctrl.mouse_click(0)
        actions.user.mouse_toggle_control_mouse()
        ctrl.mouse_move(pos[0], pos[1])
   def kingfisher_click_stay():
        """Activates the eyetracker for a brief second to move the mouse and clicks"""
        actions.user.mouse_toggle_control_mouse()
        actions.sleep(0.5) 
        ctrl.mouse_click(0)
        actions.user.mouse_toggle_control_mouse()
        
   def warp_mouse():
        """Activates the eyetracker for a brief second to move the mouse"""
        actions.user.mouse_toggle_control_mouse()
        actions.sleep(0.4)
        actions.user.mouse_toggle_control_mouse()

#    def enable_tracker_mouse():
#        """Enables eyetracking"""
#        actions.user.mouse_toggle_control_mouse()
#        actions.user.mouse_toggle_zoom_mouse()
        
#    def disable_tracker_mouse():
#        """Disables eyetracking"""
#        actions.user.mouse_toggle_control_mouse()
#        actions.user.mouse_toggle_zoom_mouse()