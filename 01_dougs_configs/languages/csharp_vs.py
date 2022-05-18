
from talon import Context, Module, actions, settings

ctx = Context()
mod = Module()
ctx.matches = r"""
tag: user.csharp
"""
ctx.tags = ["user.code_operators", "user.code_generic", "user.code_functions_gui"]

# Primitive Types
csharp_primitive_types = {
    "bool": "bool",
    "byte": "byte",
    "es byte": "sbyte",
    "char": "char",
    "decimal": "decimal",
    "double": "double",
    "float": "float",
    "int": "int",
    "you int": "uint",
    "en int": "nint",
    "en you int": "nuint",
    "long": "long",
    "you long": "ulong",
    "short": "short",
    "you short": "ushort",
    "object": "object",
    "string": "string",
    "dynamic": "dynamic",

}

ctx.lists["user.code_type"] = csharp_primitive_types



# Java Modifies
csharp_exceptions = {
    "exception": "Exception",
    "access violation exception": "AccessViolationException",
    "aggregate exception": "AggregateException",
    "application exception": "ApplicationException",
    "argument exception": "ArgumentException",
    "argument null exception": "ArgumentNullException",
    "argument out of range exception": "ArgumentOutOfRangeException",
    "out of range exception": "ArgumentOutOfRangeException",
    "arithmetic exception": "ArithmeticException",
    "array type mismatch exception": "ArrayTypeMismatchException",
    "data miss aligned exception": "DataMisalignedException",
    "divide by zero exception": "DivideByZeroException",
    "format exception": "FormatException",
    "index out of range exception": "IndexOutOfRangeException",
    "in valid operation exception": "InvalidOperationException",
    "not implemented exception": "NotImplementedException",
    "not supported exception": "NotSupportedException",
    "final": "final",
    "final": "final",
    "final": "final",
}

mod.list("csharp_exceptions", desc="C# Modifiers")
ctx.lists["self.csharp_exceptions"] = csharp_exceptions