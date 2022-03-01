import logging

from talon import Context, Module, actions, settings

mod = Module()
# rust specific grammar
mod.list('code_type_modifier', desc='List of type modifiers for active language')
mod.list('code_macros', desc='List of macros for active language')
mod.list('code_trait', desc='List of traits for active language')


@mod.action_class
class Actions:
    def code_operator_structure_dereference():
        """Inserts a reference operator """

    def code_state_implements():
        """Inserts implements block, positioning the cursor appropriately"""

    def code_insert_if_let_some():
        """Inserts if let some block, positioning the cursor appropriately"""

    def code_insert_if_let_error():
        """Inserts if let error block, positioning the cursor appropriately"""

    def code_insert_trait_annotation(type: str):
        """Inserts type annotation for implementor of trait"""

    def code_insert_return_trait(type: str):
        """Inserts a return type for implementor of trait"""

    def code_insert_macro(text: str, selection: str):
        """Inserts a macro and positions the cursor appropriately"""

    def code_insert_macro_array(text: str, selection: str):
        """Inserts a macro array and positions the cursor appropriately"""

    def code_insert_macro_block(text: str, selection: str):
        """Inserts a macro block and positions the cursor appropriately"""

    def code_state_unsafe():
        """Inserts an unsafe block and positions the cursor appropriately"""


ctx = Context()
ctx.matches = r"""
tag: user.rust
"""


# tag: libraries_gui
ctx.lists['user.code_libraries'] = {
    'eye oh': 'std::io',
    'file system': 'std::fs',
    'envy': 'std::env',
    'collections': 'std::collections',
}

# tag: functions_gui
ctx.lists['user.code_functions'] = {
    'drop': 'drop',
    'catch unwind': 'catch_unwind',
}

scalar_types = {
    'eye eight': 'i8',
    'you eight': 'u8',
    'bytes': 'u8',
    'eye sixteen': 'i16',
    'you sixteen': 'u16',
    'eye thirty two': 'i32',
    'you thirty two': 'u32',
    'eye sixty four': 'i64',
    'you sixty four': 'u64',
    'eye one hundred and twenty eight': 'i128',
    'you one hundred and twenty eight': 'u128',
    'eye size': 'isize',
    'you size': 'usize',
    'float thirty two': 'f32',
    'float sixty four': 'f64',
    'boolean': 'bool',
    'character': 'char',
}

compound_types = {
    'tuple': '()',
    'array': '[]',
}

standard_library_types = {
    'box': 'Box',
    'vector': 'Vec',
    'string': 'String',
    'string slice': '&str',
    'os string': 'OsString',
    'os string slice': '&OsStr',
    'see string': 'CString',
    'see string slice': '&CStr',
    'option': 'Option',
    'result': 'Result',
    'hashmap': 'HashMap',
    'hash set': 'HashSet',
    'reference count': 'Rc',
}

standard_sync_types = {
    'arc': 'Arc',
    'barrier': 'Barrier',
    'condition variable': 'Condvar',
    'mutex': 'Mutex',
    'once': 'Once',
    'read write lock': 'RwLock',
    'receiver': 'Receiver',
    'sender': 'Sender',
    'sink sender': 'SyncSender',
}


all_types = {
    **scalar_types,
    **compound_types,
    **standard_library_types,
    **standard_sync_types,
}

# tag: functions
ctx.lists['user.code_type'] = all_types

# rust specific grammar
ctx.lists['user.code_type_modifier'] = {
    'mutable': 'mut ',
    'mute': 'mut ',
    'borrowed': '&',
    'borrowed mutable': '&mut ',
    'borrowed mute': '&mut ',
    'mutable borrowed': '&mut ',
    'mute borrowed': '&mut ',
}


@ctx.capture("user.code_type", rule='[{user.code_type_modifier}]{user.code_type}')
def code_type(m) -> str:
    """Returns a macro name"""
    return ''.join(m)


standard_macros = {
    'macro rules': 'macro_rules!',
    'panic': 'panic!',
    'format': 'format!',
    'concatenate': 'concat!',
    'print': 'print!',
    'print line': 'println!',
    'error print line': 'eprintln!',
    'to do': 'todo!',
    'vector': 'vec!',
}

logging_macros = {
    'debug': 'debug!',
    'info': 'info!',
    'warning': 'warn!',
    'error': 'error!',
}

testing_macros = {
    'assert': 'assert!',
    'assert equal': 'assert_eq!',
    'assert not equal': 'assert_ne!',

}

ctx.lists['user.code_macros'] = {
    **standard_macros,
    **logging_macros,
    **testing_macros,
}

closure_traits = {
    'closure': 'Fn',
    'closure once': 'FnOnce',
    'closure mutable': 'FnMut',
}

ctx.lists['user.code_trait'] = {
    **closure_traits,
}


@ctx.action_class('user')
class UserActions:

    # tag: comment_line

    def code_comment_line_prefix():
        actions.insert('// ')

    # tag: comment_documentation

    def code_comment_documentation():
        actions.insert('/// ')

    def code_comment_documentation_block():
        actions.insert("/**\n\n*/")
        actions.edit.up()

    def code_comment_documentation_inner():
        actions.insert('//! ')

    def code_comment_documentation_block_inner():
        actions.insert("/*!\n\n*/")
        actions.edit.up()

    # tag: imperative

    def code_block():
        actions.auto('{\n\n}')
        actions.edit.left()
        actions.edit.up()
        actions.key('tab')

    def code_state_if():
        actions.insert('if  {  }')
        actions.key('left:5')

    def code_state_else_if():
        actions.insert(' else if  {  }')
        actions.key('left:5')

    def code_state_else():
        actions.insert(' else {  }')
        actions.key('left:2')

    def code_state_switch():
        actions.insert('match  {  }')
        actions.key('left:5')

    def code_state_for():
        actions.insert('for  in  {\n\n}\n')
        actions.key('up:3 end left:6')

    def code_state_for_each():
        actions.insert('for  in  {\n\n}\n')
        actions.key('up:3 end left:6')

    def code_state_while():
        actions.insert('while  {\n\n}\n')
        actions.key('up:3 end left:2')

    def code_state_infinite_loop():
        actions.insert('loop {\n\n}\n')
        actions.edit.up()
        actions.edit.up()

    def code_state_return():
        actions.auto_insert('return ')

    def code_break():
        actions.auto_insert('break;')

    def code_next():
        actions.auto_insert('continue;')

    # tag: object_oriented

    def code_operator_object_accessor():
        actions.auto_insert('.')

    def code_self():
        actions.auto_insert('self')

    def code_define_class():
        actions.auto_insert('struct ')

    # tag: data_bool

    def code_insert_true():
        actions.auto_insert('true')

    def code_insert_false():
        actions.auto_insert('false')

    # tag: data_null

    def code_insert_null():
        actions.auto_insert('None')

    def code_insert_is_null():
        actions.auto_insert('.is_none()')

    def code_insert_is_not_null():
        actions.auto_insert('.is_some()')

    # tag: functions

    def code_default_function(text: str):
        actions.user.code_private_function(text)

    def code_private_function(text: str):
        actions.insert('fn ')
        formatter = settings.get('user.code_private_function_formatter')
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(function_name, None)

    def code_protected_function(text: str):
        actions.insert('pub(crate) fn ')
        formatter = settings.get('user.code_protected_function_formatter')
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(function_name, None)

    def code_public_function(text: str):
        actions.insert('pub fn ')
        formatter = settings.get('user.code_public_function_formatter')
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(function_name, None)

    def code_insert_type_annotation(type: str):
        actions.insert(f': {type}')

    def code_insert_return_type(type: str):
        actions.insert(f' -> {type}')

    # tag: functions_gui

    def code_insert_function(text: str, selection: str):
        code_insert_function_or_macro(text, selection, '(', ')')

    # tag: libraries

    def code_import():
        actions.auto_insert('use ')

    # tag: libraries_gui

    def code_insert_library(text: str, selection: str):
        actions.user.paste(f'use {selection}')

    # tag: operators_array

    def code_operator_subscript():
        actions.insert('[]')
        actions.edit.left()

    # tag: code_operators_assignment

    def code_operator_assignment():
        actions.auto_insert(' = ')

    def code_operator_subtraction_assignment():
        actions.auto_insert(' -= ')

    def code_operator_addition_assignment():
        actions.auto_insert(' += ')

    def code_operator_multiplication_assignment():
        actions.auto_insert(' *= ')

    def code_operator_division_assignment():
        actions.auto_insert(' /= ')

    def code_operator_modulo_assignment():
        actions.auto_insert(' %= ')

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(' &= ')

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(' |= ')

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(' ^= ')

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(' <<= ')

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(' >>= ')

    # tag: operators_bitwise

    def code_operator_bitwise_and():
        actions.auto_insert(' & ')

    def code_operator_bitwise_or():
        actions.auto_insert(' | ')

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(' ^ ')

    def code_operator_bitwise_left_shift():
        actions.auto_insert(' << ')

    def code_operator_bitwise_right_shift():
        actions.auto_insert(' >> ')

    # tag: operators_math

    def code_operator_subtraction():
        actions.auto_insert(' - ')

    def code_operator_addition():
        actions.auto_insert(' + ')

    def code_operator_multiplication():
        actions.auto_insert(' * ')

    def code_operator_exponent():
        actions.auto_insert('.pow()')
        actions.edit.left()

    def code_operator_division():
        actions.auto_insert(' / ')

    def code_operator_modulo():
        actions.auto_insert(' % ')

    def code_operator_equal():
        actions.auto_insert(' == ')

    def code_operator_not_equal():
        actions.auto_insert(' != ')

    def code_operator_greater_than():
        actions.auto_insert(' > ')

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(' >= ')

    def code_operator_less_than():
        actions.auto_insert(' < ')

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(' <= ')

    def code_operator_and():
        actions.auto_insert(' && ')

    def code_operator_or():
        actions.auto_insert(' || ')

    def code_operator_increment():
        actions.insert(' += 1')

    # rust specific grammar

    def code_operator_structure_dereference():
        actions.auto_insert('*')

    def code_insert_if_let_some():
        actions.insert('if let Some() =  {  }')
        actions.key('left:9')

    def code_insert_if_let_error():
        actions.insert('if let Err() =  {  }')
        actions.key('left:9')

    def code_state_implements():
        actions.insert('impl  {\n}\n')
        actions.key('up:2 right:5')

    def code_insert_trait_annotation(type: str):
        actions.insert(f': impl {type}')

    def code_insert_return_trait(type: str):
        actions.insert(f' -> impl {type}')

    def code_insert_macro(text: str, selection: str):
        code_insert_function_or_macro(text, selection, '(', ')')

    def code_insert_macro_array(text: str, selection: str):
        code_insert_function_or_macro(text, selection, '[', ']')

    def code_insert_macro_block(text: str, selection: str):
        code_insert_function_or_macro(text, selection, '{', '}')

    def code_state_unsafe():
        actions.insert('unsafe {\n}\n')
        actions.key('up')


def code_insert_function_or_macro(
        text: str,
        selection: str,
        left_delim: str,
        right_delim: str,
):
    if selection:
        out_text = text + f'{left_delim}{selection}{right_delim}'
    else:
        out_text = text + f'{left_delim}{right_delim}'
    actions.user.paste(out_text)
    actions.edit.left()

