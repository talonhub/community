from talon import Context, Module, actions, settings

ctx = Context()
ctx.matches = r"""
tag: user.code_object_oriented
"""

mod = Module()

mod.tag(
    "code_object_oriented",
    desc="Tag for enabling basic object oriented programming commands (objects, classes, etc)",
)

mod.list("code_common_method", desc="Commonly invoked method, e.g. 'foo' in '.foo()'")


@ctx.capture("user.code_type", rule="{user.code_type} | class <user.text>")
def code_type(m) -> str:
    """Returns a type, allowing dictated text to be used as a class name"""
    try:
        return m.code_type
    except AttributeError:
        return actions.user.formatted_text(
            m.text, settings.get("user.code_class_formatter")
        )


@mod.action_class
class Actions:
    def code_operator_object_accessor():
        """Inserts the object accessor operator (e.g., Java's "." or PHP's "->)"""

    def code_self():
        """Inserts a reference to the current object (e.g., C++ "this" or Python's "self")"""

    def code_self_accessor():
        """Inserts the object accessor applied to a reference to the current object (e.g., python's "self.")"""
        actions.user.code_self()
        actions.user.code_operator_object_accessor()

    def code_define_class():
        """Starts a class definition (e.g., Java's "class" keyword)"""
        actions.user.insert_snippet_by_name("classDeclaration")

    def code_method(name: str):
        """Inserts a method invocation"""
        actions.user.insert_between(f".{name}(", ")")
