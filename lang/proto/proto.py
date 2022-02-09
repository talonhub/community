from talon import Module, Context, actions, ui, imgui, settings

mod = Module()

ctx = Context()
ctx.matches = r'''
mode: user.protobuf
mode: user.auto_lang
and code.language: protobuf
'''

ctx.lists['user.code_type'] = {
    'string': 'string',
    'bytes': 'bytes',
    'you 64': 'uint64',
    'you 32': 'uint32',
    'eye 64': 'int64',
    'eye 32': 'int32',
    'sin 64': 'sint64',
    'sin 32': 'sint32',
    'fixed 64': 'fixed64',
    'fixed 32': 'fixed32',
    'asfixed 64': 'sfixed64',
    'asfixed 32': 'sfixed32',
    'boolean': 'bool',
    'double': 'double',
    'float': 'float',
}

@mod.capture(rule='[repeated] type {user.code_type}')
def code_insert_type(match) -> str:
    '''Returns type'''
    t = getattr(match, 'code_type')
    if len(match) == 2:
        return f'{t} '
    else:
        return f'repeated {t} '
