from talon import app, Context, Module
from talon.engine import engine

mod = Module()
@mod.action_class
class Actions:  
    def password_fill():
        """fill the password"""
        
    def password_show():
        """show the password"""
        
    def password_new():
        """New password"""
       
    def password_duplicate():
       """Duplicate password"""
       
    def password_edit():
        """Edit password"""

    def password_delete():
        """Delete password"""