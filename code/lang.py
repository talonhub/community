from talon import Context, actions, ui, Module, registry
from typing import List, Union, Set

mod = Module()
mod.setting('language_private_function_formatter', str)
mod.setting('language_protected_function_formatter', str)
mod.setting('language_public_function_formatter', str)
mod.setting('language_private_variable_formatter', str)
mod.setting('language_protected_variable_formatter', str)
mod.setting('language_public_variable_formatter', str)

ctx = Context()
ctx.settings["user.language_private_function_formatter"] = "SNAKE_CASE"
ctx.settings["user.language_protected_function_formatter"] = "SNAKE_CASE"
ctx.settings["user.language_public_function_formatter"] = "SNAKE_CASE"
ctx.settings["user.language_private_variable_formatter"] = "SNAKE_CASE"
ctx.settings["user.language_protected_variable_formatter"] = "SNAKE_CASE"
ctx.settings["user.language_public_variable_formatter"] = "SNAKE_CASE"

@mod.action_class
class LanguageActions:

    def language_operator_and():
        """languagee_operator_and"""

    def language_operator_or():
        """language_operator_or"""

    def language_operator_assign():
        """language_operator_assign"""

    def language_operator_equal():
        """language_operator_equals"""

    def language_operator_not_equal():
        """language_operator_equals"""

    def language_operator_minus():
        """language_operator_minus"""

    def language_operator_minus_equals():
        """language_operator_minus_equals"""
    
    def language_operator_plus():
        """language_operator_add"""

    def language_operator_plus_equals():
        """language_operator_plus_equals"""

    def language_operator_multiply():
        """language_operator_multiply"""

    def language_operator_multiply_equals():
        """language_operator_multiply_equals"""

    def language_operator_exponent():
        """language_operator_exponent"""

    def language_operator_divide():
        """language_operator_divide"""

    def language_operator_divide_equals():
        """language_operator_divide_equals"""

    def language_operator_modulo():
        """language_operator_mod"""

    def language_operator_modulo_equals():
        """language_operator_mod_equals"""

    def language_operator_greater_than():
        """language_operator_greater_than"""

    def language_operator_greater_than_equals(): 
        """language_operator_greater_than_equals"""

    def language_operator_less_than():
        """language_operator_less_than"""

    def language_operator_less_than_equals(): 
        """language_operator_less_than_equals"""

    def language_bitwise_operator_and():
        """language_bitwise_operator_and"""

    def language_bitwise_operator_and_equals():
        """language_operator_and"""

    def language_bitwise_operator_or(): 
        """language_bitwise_operator_or"""

    def language_bitwise_operator_or_equals(): 
        """language_operator_or_equals"""
    
    def language_bitwise_operator_exlcusive_or(): 
        """language_bitwise_operator_exlcusive_or"""

    def language_bitwise_operator_exlcusive_or_equals(): 
        """language_bitwise_operator_exlcusive_or_equals"""

    def language_bitwise_operator_left_shift(): 
        """language_bitwise_operator_left_shift"""

    def language_bitwise_operator_left_shift_equals(): 
        """language_bitwise_operator_left_shift_equals"""

    def language_bitwise_operator_right_shift(): 
        """language_bitwise_operator_right_shift"""

    def language_bitwise_operator_right_shift_equals(): 
        """language_bitwise_operator_right_shift_equals"""

    def language_self():
        """Inserts the equivalent of "this" in C++ or self in python"""
        
    def language_null():
        """inserts null equivalent"""
        
    def language_is_null():
        """inserts check for == null"""

    def language_is_not_null():
        """inserts check for == null"""

    def language_state_in():
        """Inserts python "in" equivalent"""

    def language_state_if():
        """Inserts if statement"""

    def language_state_else_if():
        """Inserts else if statement"""

    def language_state_else():
        """Inserts else statement"""

    def language_state_switch():
        """Inserts switch statement"""

    def language_state_case():
        """Inserts case statement"""

    def language_state_for():
        """Inserts for statement"""

    def language_state_for_each():
        """Inserts for each equivalent statement"""
    
    def language_state_go_to():
        """inserts go-to statement"""

    def language_state_while():
        """Inserts while statement"""
    
    def language_try_catch():
        """Inserts try/catch. If selection is true, does so around the selecion"""

    def language_private_function():
        """Inserts private function declaration w/o name"""
         #todo: once .talon action definitiones can take parameters, combine with language_private_function_formatter
         #same for all the rest

    def language_private_function_formatter(phrase):
        """Inserts private function name with formatter"""
        actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.language_private_function_formatter"][1].split(" "))

    def language_private_static_function():
        """Inserts private static function"""
        
    def language_protected_function():
        """Inserts protected function declaration w/o name"""

    def language_protected_static_function():
        """Inserts public function"""

    def language_protected_function_formatter(phrase: str):
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.language_protected_function_formatter"][1].split(" ")))
    
    def language_public_function():
        """Inserts public function"""

    def language_public_static_function():
        """Inserts public function"""

    def language_public_function_formatter(phrase: str):
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.language_public_function_formatter"][1].split(" ")))

    def language_private_function_formatter(phrase: str):
        """Inserts private function name with formatter"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.language_private_function_formatter"][1].split(" ")))

    def language_protected_variable_formatter(phrase: str):
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.language_protected_variable_formatter"][1].split(" ")))

    def language_public_variable_formatter():
        """inserts properly formatted private function name"""
        actions.insert(actions.user.formatters_format_text(actions.dictate.parse_words(phrase), registry.settings["user.language_public_variable_formatter"][1].split(" ")))

    def language_comment():
        """Inserts comment at current cursor location"""

    def language_block_comment():
        """Block comment"""

    def language_type_definition():
        """language_type_definition (typedef)"""

    def language_typedef_struct():
        """language_typedef_struct (typedef)"""

    def language_type_class():
        """language_type_class"""

    def language_type_struct():
        """language_type_struct"""

    def language_include():
        """language_include"""

    def language_include_system():
        """language_include_system"""

    def language_include_local():
        """language_include_local"""
    
    def language_import():
        """import/using equivalent"""

    def language_from_import():
        """from import python equivalent"""


    