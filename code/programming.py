from talon import app, Context, Module
from talon.engine import engine

mod = Module()


@mod.action_class
class Actions:
    def code_if():
        """if"""

    def code_else():
        """else"""

    def code_else_if():
        """else_if"""

    def code_switch():
        """switch"""

    def code_case():
        """case"""

    def code_do_loop():
        """do_loop"""

    def code_while_loop():
        """while_loop"""

    def code_for_loop():
        """for_loop"""

    def code_for_each_loop():
        """for_each_loop"""

    def code_to_integer():
        """to_integer"""

    def code_to_float():
        """to_float"""

    def code_to_string():
        """to_string"""

    def code_to_boolean():
        """to_boolean"""

    def code_and():
        """and"""

    def code_or():
        """or"""

    def code_not():
        """not"""

    def code_sysout():
        """sysout"""

    def code_import():
        """import"""

    def code_from():
        """from"""

    def code_block():
        """block"""

    def code_function():
        """function"""

    def code_lambda():
        """lambda"""

    def code_class():
        """class"""

    def code_docstring():
        """docstring"""

    def code_comment():
        """comment"""

    def code_long_comment():
        """long comment"""

    def code_return():
        """return"""

    def code_null():
        """null"""

    def code_true():
        """true"""

    def code_false():
        """false"""
