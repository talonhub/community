from talon import Context, actions, settings

ctx = Context()
ctx.matches = r"""
tag: user.ruby
"""

@ctx.action_class('user')
class UserActions:
    def code_operator_lambda(): actions.auto_insert('->')
    def code_operator_subscript():
        actions.insert('[]')
        actions.key('left')
    def code_operator_assignment(): actions.auto_insert(' = ')
    def code_operator_subtraction(): actions.auto_insert(' - ')
    def code_operator_subtraction_assignment(): actions.auto_insert(' -= ')
    def code_operator_addition(): actions.auto_insert(' + ')
    def code_operator_addition_assignment(): actions.auto_insert(' += ')
    def code_operator_multiplication(): actions.auto_insert(' * ')
    def code_operator_multiplication_assignment(): actions.auto_insert(' *= ')
    def code_operator_exponent(): actions.auto_insert(' ** ')
    def code_operator_division(): actions.auto_insert(' / ')
    def code_operator_division_assignment(): actions.auto_insert(' /= ')
    def code_operator_modulo(): actions.auto_insert(' % ')
    def code_operator_modulo_assignment(): actions.auto_insert(' %= ')
    def code_operator_equal(): actions.auto_insert(' == ')
    def code_operator_not_equal(): actions.auto_insert(' != ')
    def code_operator_greater_than(): actions.auto_insert(' > ')
    def code_operator_greater_than_or_equal_to(): actions.auto_insert(' >= ')
    def code_operator_less_than(): actions.auto_insert(' < ')
    def code_operator_less_than_or_equal_to(): actions.auto_insert(' <= ')
    def code_operator_and(): actions.auto_insert(' && ')
    def code_operator_or(): actions.auto_insert(' || ')
    def code_operator_bitwise_and(): actions.auto_insert(' & ')
    def code_operator_bitwise_and_assignment(): actions.auto_insert(' &= ')
    def code_operator_bitwise_or(): actions.auto_insert(' | ')
    def code_operator_bitwise_or_assignment(): actions.auto_insert(' |= ')
    def code_operator_bitwise_exclusive_or(): actions.auto_insert(' ^ ')
    def code_operator_bitwise_exclusive_or_assignment(): actions.auto_insert(' ^= ')
    def code_operator_bitwise_left_shift(): actions.auto_insert(' << ')
    def code_operator_bitwise_left_shift_assignment(): actions.auto_insert(' <<= ')
    def code_operator_bitwise_right_shift(): actions.auto_insert(' >> ')
    def code_operator_bitwise_right_shift_assignment(): actions.auto_insert(' >>= ')
    def code_self(): actions.auto_insert('self')
    def code_operator_object_accessor(): actions.auto_insert('.')
    def code_insert_null(): actions.auto_insert('nil')
    def code_insert_is_null(): actions.auto_insert('.nil?')
    # Technically .present? is provided by Rails
    def code_insert_is_not_null(): actions.auto_insert('.present?')
    def code_state_do():
        actions.insert('do ')
    def code_state_if():
        actions.insert('if ')
    def code_state_else_if():
        actions.insert('elsif ')
    def code_state_else():
        actions.insert('else')
        actions.key('enter')
    def code_state_switch():
        actions.insert('case ')
    def code_state_case():
        actions.insert('when ')
    def code_state_for_each():
        actions.insert('.each do ||')
        actions.key('left')
    def code_define_class(): actions.auto_insert('class ')
    def code_import():
        actions.auto_insert('require ""')
        actions.key('left')
    def code_comment_line_prefix(): actions.auto_insert('# ')
    def code_state_return():
        actions.insert('return ')
    def code_insert_true(): actions.auto_insert('true')
    def code_insert_false(): actions.auto_insert('false')
    def code_comment_documentation():
        actions.insert('##')
        actions.key('enter')
        actions.key('space')
        ### Extra non-standard things
    def code_default_function(text: str):
        """Inserts function definition"""

        result = "def {}".format(
            actions.user.formatted_text(
                text,
                settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
