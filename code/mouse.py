from talon import ctrl, ui, Module, Context, actions
from talon.engine import engine
from talon_plugins import speech, eye_mouse, eye_zoom_mouse
import platform
import subprocess
import ctypes
import os
import pathlib

key = actions.key
self = actions.self
dragging = False

def show_cursor_helper(show):
    """Show/hide the cursor"""
    ctrl.cursor_visible(show)
    
mod = Module()
@mod.action_class
class Actions:
    def mouse_show_cursor():
        """Shows the cursor"""
        show_cursor_helper(True)
        
    def mouse_hide_cursor():
        """Hides the cursor"""
        show_cursor_helper(False) 
  
    def mouse_wake():
        """Enable control mouse, zoom mouse, and disables cursor"""
        eye_zoom_mouse.zoom_mouse.enable()
        eye_mouse.control_mouse.enable() 
        show_cursor_helper(False)
        
    def mouse_calibrate():
        """Start calibration"""
        eye_mouse.calib_start()
            
    def mouse_toggle_control_mouse():
        """Toggles control mouse"""
        eye_mouse.control_mouse.toggle()

    def mouse_toggle_zoom_mouse():
        """Toggles zoom mouse"""
        if eye_zoom_mouse.zoom_mouse.enabled:
            try:
                eye_zoom_mouse.zoom_mouse.disable()
            except:
                eye_zoom_mouse.zoom_mouse.enabled = False
        else:
            eye_zoom_mouse.zoom_mouse.enable()      
       
    def mouse_cancel_zoom_mouse():
        """Cancel zoom mouse if pending"""
        if eye_zoom_mouse.zoom_mouse.enabled and eye_zoom_mouse.zoom_mouse.state != eye_zoom_mouse.STATE_IDLE:
            eye_zoom_mouse.zoom_mouse.cancel()
    
    def mouse_drag():
        """(TEMPORARY) Press and hold/release button 0 depending on state for dragging"""
        global dragging
        if not dragging:
            dragging = True
            ctrl.mouse_click(button = 0, down = True)
        else:
            dragging = False
            ctrl.mouse_click(up = True)
    
    def mouse_sleep():
        """Disables control mouse, zoom mouse, and re-enables cursor"""
        eye_zoom_mouse.zoom_mouse.disable()
        eye_mouse.control_mouse.disable() 
        show_cursor_helper(True)
