from talon import ctrl, ui, Module, Context, actions
from talon.engine import engine
from talon_plugins import speech, eye_mouse, eye_zoom_mouse
import platform
import subprocess
import win32gui
import win32con
import ctypes
import os
import winreg
import pathlib

key = actions.key
self = actions.self

default_cursor = {
"AppStarting": "%SystemRoot%\\Cursors\\aero_working.ani",
"Arrow": "%SystemRoot%\\Cursors\\aero_arrow.cur",
"Hand": "%SystemRoot%\\Cursors\\aero_link.cur",
"Help": "%SystemRoot%\\Cursors\\aero_helpsel.cur",
"No": "%SystemRoot%\\Cursors\\aero_unavail.cur",
"NWPen": "%SystemRoot%\\Cursors\\aero_pen.cur",
"Person": "%SystemRoot%\\Cursors\\aero_person.cur",
"Pin": "%SystemRoot%\\Cursors\\aero_pin.cur",
"SizeAll": "%SystemRoot%\\Cursors\\aero_move.cur",
"SizeNESW": "%SystemRoot%\\Cursors\\aero_nesw.cur",
"SizeNS": "%SystemRoot%\\Cursors\\aero_ns.cur",
"SizeNWSE": "%SystemRoot%\\Cursors\\aero_nwse.cur",
"SizeWE": "%SystemRoot%\\Cursors\\aero_ew.cur",
"UpArrow": "%SystemRoot%\Cursors\\aero_up.cur",
"Wait": '%SystemRoot%\\Cursors\\aero_busy.ani',
"Crosshair": "",
"IBeam":"",
}

#todo figure out why notepad++ still shows the cursor sometimes.
hidden_cursor = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Resources\HiddenCursor.cur")

def show_cursor_helper(show):
    """Show/hide the cursor"""
    if "Windows-10" in platform.platform(terse=True):
        try:
            Registrykey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\Cursors", 0, winreg.KEY_WRITE)

            for value_name, value in default_cursor.items():   
                if show: 
                    winreg.SetValueEx(Registrykey, value_name, 0, winreg.REG_EXPAND_SZ, value)
                else:
                    winreg.SetValueEx(Registrykey, value_name, 0, winreg.REG_EXPAND_SZ, hidden_cursor)
                        
            winreg.CloseKey(Registrykey)

            ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETCURSORS, 0, None, 0)
            
        except WindowsError:
            print("Unable to show_cursor({})".format(str(show)))
    else:
        ctrl.cursor_visible(show)
            
mod = Module()
@mod.action_class
class Actions:
    def show_cursor():
        """Shows the cursor"""
        show_cursor_helper(True)
        
    def hide_cursor():
        """Hides the cursor"""
        show_cursor_helper(False) 
  
    def wake():
        """Enable control mouse, zoom mouse, and disables cursor"""
        eye_zoom_mouse.zoom_mouse.enable()
        eye_mouse.control_mouse.enable() 
        show_cursor_helper(False)
        #use_mic("Microphone (d:vice MMA-A)")
        
    def calibrate():
        """Start calibration"""
        eye_mouse.calib_start()
            
    def toggle_control_mouse():
        """Toggles control mouse"""
        eye_mouse.control_mouse.toggle()

    def toggle_zoom_mouse():
        """Toggles zoom mouse"""
        if eye_zoom_mouse.zoom_mouse.enabled:
            try:
                eye_zoom_mouse.zoom_mouse.disable()
            except:
                eye_zoom_mouse.zoom_mouse.enabled = False
        else:
            eye_zoom_mouse.zoom_mouse.enable()      
       
    def cancel_zoom_mouse():
        """Cancel zoom mouse if pending"""
        if eye_zoom_mouse.zoom_mouse.enabled and eye_zoom_mouse.zoom_mouse.state != eye_zoom_mouse.STATE_IDLE:
            eye_zoom_mouse.zoom_mouse.cancel()
        
    def sleep():
        """Disables control mouse, zoom mouse, and re-enables cursor"""
        eye_zoom_mouse.zoom_mouse.disable()
        eye_mouse.control_mouse.disable() 
        show_cursor_helper(True)
