from talon import Context, actions, ui, Module

mod = Module()
@mod.action_class
class LangActions:
    def state_if(): 
        """inserts if statement"""

    def state_elif():
        """Inserts else if statement"""

    def state_else():
        """Inserts else statement"""

    def state_switch():
        """Inserts switch statement"""
    
    def state_case():
        """Inserts case statement"""

    def state_for():
        """Inserts for statement"""
    
    def state_go_to():
        """inserts go-to statement"""


    def state_while():
        """Inserts while statement"""
    
    def try_catch():
        """Inserts try/catch. If selection is true, does so around the selecion"""

    def private_function(m: str):
        """Inserts private function"""

    def protected_function():
        """Inserts protected function"""

    def public_function():
        """Inserts public function"""

    def comment_here():
        """Inserts comment at current cursor location"""

    def comment_begin_line():
        """Inserts comment at the beginning of the line"""

    def block_comment():
        """Block comments selection"""


    