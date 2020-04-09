from talon import Context, actions, ui, Module, registry
from typing import List, Union, Set

mod = Module()
mod.setting('lang_private_function_formatter', 'str')
mod.setting('lang_protected_function_formatter', 'str')
mod.setting('lang_public_function_formatter', 'str')
mod.setting('lang_private_variable_formatter', 'str')
mod.setting('lang_protected_variable_formatter', 'str')
mod.setting('lang_public_variable_formatter', 'str')

ctx = Context()
ctx.settings["user.lang_private_function_formatter"] = "SNAKE_CASE"
ctx.settings["user.lang_protected_function_formatter"] = "SNAKE_CASE"
ctx.settings["user.lang_public_function_formatter"] = "SNAKE_CASE"
ctx.settings["user.lang_private_variable_formatter"] = "SNAKE_CASE"
ctx.settings["user.lang_protected_variable_formatter"] = "SNAKE_CASE"
ctx.settings["user.lang_public_variable_formatter"] = "SNAKE_CASE"

@mod.action_class
class LangActions:
    def lang_operator_and():
        """lange_operator_and"""

    def lang_operator_or():
        """lang_operator_or"""

    def lang_operator_assign():
        """lang_operator_assign"""
        actions.insert(" = ")

    def lang_operator_equal():
        """lang_operator_equals"""

    def lang_operator_not_equal():
        """lang_operator_equals"""

    def lang_operator_minus():
        """lang_operator_minus"""
        actions.insert(" - ")

    def lang_operator_minus_equals():
        """lang_operator_minus_equals"""
        actions.insert(" -= ")
    
    def lang_operator_plus():
        """lang_operator_add"""
        actions.insert(" + ")

    def lang_operator_plus_equals():
        """lang_operator_plus_equals"""
        actions.insert(" += ")

    def lang_operator_multiply():
        """lang_operator_multiply"""
        actions.insert(" * ")

    def lang_operator_multiply_equals():
        """lang_operator_multiply_equals"""
        actions.insert(" * ")

    def lang_operator_exponent():
        """lang_operator_exponent"""

    def lang_operator_divide():
        """lang_operator_divide"""
        actions.insert(" / ")

    def lang_operator_divide_equals():
        """lang_operator_divide_equals"""
        actions.insert(" /= ")

    def lang_operator_modulo():
        """lang_operator_mod"""
        actions.insert(" % ")

    def lang_operator_modulo_equals():
        """lang_operator_mod_equals"""
        actions.insert(" %= ")

    def lang_operator_greater_than():
        """lang_operator_greater_than"""
        actions.insert(" > ")

    def lang_operator_greater_than_equals(): 
        """lang_operator_greater_than_equals"""
        actions.insert(" >= ")

    def lang_operator_less_than():
        """lang_operator_less_than"""
        actions.insert(" < ")

    def lang_operator_less_than_equals(): 
        """lang_operator_less_than_equals"""
        actions.insert(" <= ")

    def lang_bitwise_operator_and():
        """lang_bitwise_operator_and"""
        actions.insert(" & ")

    def lang_operator_and_equals():
        """lang_operator_and"""
        actions.insert(" &= ")

    def lang_bitwise_operator_or(): 
        """lang_bitwise_operator_or"""
        actions.insert(" | ")

    def lang_bitwise_operator_or_equals(): 
        """lang_operator_or_equals"""
        actions.insert(" |= ")
    
    def lang_bitwise_operator_exlcusive_or(): 
        """lang_bitwise_operator_exlcusive_or"""
        actions.insert(" ^ ")

    def lang_bitwise_operator_exlcusive_or_equals(): 
        """lang_bitwise_operator_exlcusive_or_equals"""

    def lang_bitwise_operator_left_shift(): 
        """lang_bitwise_operator_left_shift"""

    def lang_bitwise_operator_left_shift_equals(): 
        """lang_bitwise_operator_left_shift_equals"""

    def lang_bitwise_operator_right_shift(): 
        """lang_bitwise_operator_right_shift"""

    def lang_bitwise_operator_right_shift_equals(): 
        """lang_bitwise_operator_right_shift_equals"""

    def lang_self():
        """Inserts the equivalent of "this" in C++ or self in python"""
        
    def lang_null():
        """inserts null equivalent"""
        
    def lang_is_null():
        """inserts check for == null"""

    def lang_is_not_null():
        """inserts check for == null"""

    def lang_state_in():
        """Inserts python "in" equivalent"""

    def lang_state_if():
        """Inserts if statement"""

    def lang_state_else_if():
        """Inserts else if statement"""

    def lang_state_else():
        """Inserts else statement"""

    def lang_state_switch():
        """Inserts switch statement"""

    def lang_state_case():
        """Inserts case statement"""

    def lang_state_for():
        """Inserts for statement"""

    def lang_state_for_each():
        """Inserts for each equivalent statement"""
    
    def lang_state_go_to():
        """inserts go-to statement"""

    def lang_state_while():
        """Inserts while statement"""
    
    def lang_try_catch():
        """Inserts try/catch. If selection is true, does so around the selecion"""

    def lang_private_function():
        """Inserts private function declaration w/o name"""

    def lang_private_static_function():
        """Inserts private static function"""

    def lang_private_function_formatter(phrase):
        """Inserts private function name with formatter"""
        actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.lang_private_function_formatter"][1].split(" "))

    def lang_protected_function():
        """Inserts protected function declaration w/o name"""

    def lang_protected_static_function():
        """Inserts public function"""

    def lang_protected_function_formatter(phrase: str):
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.lang_protected_function_formatter"][1].split(" ")))
    
    def lang_public_function():
        """Inserts public function"""

    def lang_public_static_function():
        """Inserts public function"""

    def lang_public_function_formatter(phrase: str):
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.lang_public_function_formatter"][1].split(" ")))

    def lang_private_function_formatter(phrase: str):
        """Inserts private function name with formatter"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.lang_private_function_formatter"][1].split(" ")))

    def lang_protected_variable_formatter(phrase: str):
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.lang_protected_variable_formatter"][1].split(" ")))

    def lang_public_variable_formatter():
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.lang_public_variable_formatter"][1].split(" ")))

    def lang_comment_here():
        """Inserts comment at current cursor location"""

    def lang_comment_begin_line():
        """Inserts comment at the beginning of the line"""

    def lang_block_comment():
        """Block comments selection"""

    def lang_type_definition():
        """lang_type_definition (typedef)"""

    def lang_typedef_struct():
        """lang_typedef_struct (typedef)"""

    def lang_type_class():
        """lang_type_class"""

    def lang_type_struct():
        """lang_type_struct"""

    def lang_include():
        """lang_include"""

    def lang_include_system():
        """lang_include_system"""

    def lang_include_local():
        """lang_include_local"""
    
    def lang_import():
        """import/using equivalent"""

    def lang_from_import():
        """from import python equivalent"""

    