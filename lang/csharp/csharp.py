from talon import Context, Module, actions, imgui, settings, ui

ctx = Context()
ctx.matches = r"""
mode: user.csharp
mode: user.auto_lang
and code.language: csharp
"""
ctx.lists["user.code_functions"] = {
    "integer": "int.TryParse",
    "print": "Console.WriteLine",
    "string": ".ToString",
}


@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():           actions.auto_insert('*')
    def code_operator_address_of():            actions.auto_insert('&')
    def code_operator_structure_dereference(): actions.auto_insert('->')
    def code_operator_lambda():                actions.auto_insert('=>')
    def code_operator_subscript():
        actions.insert('[]')
        actions.key('left')
    def code_operator_assignment():                      actions.auto_insert(' = ')
    def code_operator_subtraction():                     actions.auto_insert(' - ')
    def code_operator_subtraction_assignment():          actions.auto_insert(' -= ')
    def code_operator_addition():                        actions.auto_insert(' + ')
    def code_operator_addition_assignment():             actions.auto_insert(' += ')
    def code_operator_multiplication():                  actions.auto_insert(' * ')
    def code_operator_multiplication_assignment():       actions.auto_insert(' *= ')
    #action(user.code_operator_exponent): " ** "
    def code_operator_division():                        actions.auto_insert(' / ')
    def code_operator_division_assignment():             actions.auto_insert(' /= ')
    def code_operator_modulo():                          actions.auto_insert(' % ')
    def code_operator_modulo_assignment():               actions.auto_insert(' %= ')
    def code_operator_equal():                           actions.auto_insert(' == ')
    def code_operator_not_equal():                       actions.auto_insert(' != ')
    def code_operator_greater_than():                    actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to():        actions.auto_insert(' >= ')
    def code_operator_less_than():                       actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to():           actions.auto_insert(' <= ')
    def code_operator_and():                             actions.auto_insert(' && ')
    def code_operator_or():                              actions.auto_insert(' || ')
    def code_operator_bitwise_and():                     actions.auto_insert(' & ')
    def code_operator_bitwise_and_assignment():          actions.auto_insert(' &= ')
    def code_operator_bitwise_or():                      actions.auto_insert(' | ')
    def code_operator_bitwise_or_assignment():           actions.auto_insert(' |= ')
    def code_operator_bitwise_exclusive_or():            actions.auto_insert(' ^ ')
    def code_operator_bitwise_exclusive_or_assignment(): actions.auto_insert(' ^= ')
    def code_operator_bitwise_left_shift():              actions.auto_insert(' << ')
    def code_operator_bitwise_left_shift_assignment():   actions.auto_insert(' <<= ')
    def code_operator_bitwise_right_shift():             actions.auto_insert(' >> ')
    def code_operator_bitwise_right_shift_assignment():  actions.auto_insert(' >>= ')
    def code_block():
        actions.insert('{}')
        actions.key('left enter enter up tab')
    def code_self():        actions.auto_insert('this')
    def code_null():        actions.auto_insert('null')
    def code_is_null():     actions.auto_insert(' == null ')
    def code_is_not_null(): actions.auto_insert(' != null')
    def code_state_if():
        actions.insert('if()')
        actions.key('left')
    def code_state_else_if():
        actions.insert('else if()')
        actions.key('left')
    def code_state_else():
        actions.insert('else\n{\n}\n')
        actions.key('up')
    def code_state_switch():
        actions.insert('switch()')
        actions.edit.left()
    def code_state_case():
        actions.insert('case \nbreak;')
        actions.edit.up()
    def code_state_for(): actions.auto_insert('for ')
    def code_state_for_each():
        actions.insert('foreach() ')
        actions.key('left')
        actions.edit.word_left()
        actions.key('space')
        actions.edit.left()
    def code_state_go_to(): actions.auto_insert('go to ')
    def code_state_while():
        actions.insert('while()')
        actions.edit.left()
    def code_state_return():   actions.auto_insert('return ')
    def code_break():          actions.auto_insert('break;')
    def code_next():           actions.auto_insert('continue;')
    def code_true():           actions.auto_insert('true')
    def code_false():          actions.auto_insert('false')
    
    #action(user.code_type_definition): "typedef "
    #action(user.code_typedef_struct):
    #    insert("typedef struct")
    #    insert("{{\n\n}}")
    #    edit.up()
    #    key(tab)
    def code_type_class():     actions.auto_insert('class ')
    def code_import():         actions.auto_insert('using  ')
    def code_from_import():    actions.auto_insert('using ')
    def code_include():        actions.insert('using ')
    def code_include_system(): actions.insert('using ')
    def code_include_local():  actions.insert('using ')
    def code_comment():        actions.auto_insert('//')
    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "private static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_function(text: str):
        result = "private void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_protected_static_function(text: str):
        result = "protected static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_protected_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_function(text: str):
        result = "public void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_public_static_function(text: str):
        result = "public static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)
