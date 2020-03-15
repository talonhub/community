from talon import cron, ctrl, ui, Module, Context, actions
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
scroll_amount = 0
click_job = None
scroll_job = None
gaze_job = None

def show_cursor_helper(show):
    """Show/hide the cursor"""
    ctrl.cursor_visible(show)
    
def mouse_scroll(amount):
    def scroll():
        global scroll_amount
        if (scroll_amount >= 0) == (amount >= 0):
            scroll_amount += amount
        else:
            scroll_amount = amount
        actions.mouse_scroll(y=int(amount))

    return scroll

def scroll_continuous_helper():
    global scroll_amount
    #print("scroll_continuous_helper")
    if scroll_amount:
        actions.mouse_scroll(by_lines=False, y=int(scroll_amount / 10))

def start_scroll():
    global scroll_job
    scroll_job = cron.interval("60ms", scroll_continuous_helper)
    
def gaze_scroll():
    #print("gaze_scroll")
    windows = ui.windows()
    window = None
    x, y = ctrl.mouse_pos()
    for w in windows:
        if w.rect.contains(x, y):
            window = w.rect
            break
    if window is None:
        #print("no window found!")
        return
        
    midpoint = window.y + window.height / 2
    amount = int(((y - midpoint) / (window.height / 10)) ** 3)
    actions.mouse_scroll(by_lines=False, y=amount)
    
    #print(f"gaze_scroll: {midpoint} {window.height} {amount}")
    
def stop_scroll():
    global scroll_amount, scroll_job, gaze_job
    scroll_amount = 0
    cron.cancel(scroll_job)
    cron.cancel(gaze_job)
    scroll_job = None
    gaze_job = None
    
def start_cursor_scrolling():
    global scroll_job, gaze_job
    stop_scroll()
    gaze_job = cron.interval("60ms", gaze_scroll)


mod = Module()
mod.list('mouse_button',   desc='List of mouse button words to mouse_click index parameter')

@mod.capture
def mouse_index(m) -> int:
    "One mouse button index"
    
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
        
    def mouse_scroll_down():
        """Scrolls down"""
        mouse_scroll(120)()
        
    def mouse_scroll_down_continuous():
        """Scrolls down continuously"""
        mouse_scroll(80)()
        
        if scroll_job is None:
            start_scroll()
        
    def mouse_scroll_up():
        """Scrolls up"""
        mouse_scroll(-120)()
        
    def mouse_scroll_up_continuous():
        """Scrolls up continuously"""
        mouse_scroll(-80)()
        
        if scroll_job is None:
            start_scroll() 

    def mouse_scroll_stop():
        """Stops scrolling"""
        stop_scroll()
        
    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        start_cursor_scrolling()
        
ctx = Context()
ctx.lists['self.mouse_button'] = {
     'righty':  '1',
     'rickle': '1',
     'chiff': '0',
}

@ctx.capture(rule='{self.mouse_button}')
def mouse_index(m) -> int:
    return int(m.mouse_button[0])
    