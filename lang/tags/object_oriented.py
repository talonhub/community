from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag(
    "code_object_oriented",
    desc="Tag for enabling basic object oriented programming commands (objects, classes, etc)",
)

mod.list("code_common_method", desc="Commonly invoked method, e.g. 'foo' in '.foo()'")


@mod.action_class
class Actions:
    def code_operator_object_accessor():
        """Inserts the object accessor operator (e.g., Java's "." or PHP's "->)"""

    def code_self():
        """Inserts a reference to the current object (e.g., C++ "this" or Python's "self")"""

    def code_define_class():
        """Starts a class definition (e.g., Java's "class" keyword)"""
        actions.user.insert_snippet_by_name("classDeclaration")

    def code_method(name: str):
        """Inserts a method invocation"""
        actions.user.insert_between(f".{name}(", ")")
