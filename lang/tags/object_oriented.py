from talon import Module

mod = Module()

mod.tag(
    "code_object_oriented",
    desc="Tag for enabling basic object oriented programming commands (objects, classes, etc)",
)

mod.list(
    "code_self",
    desc="Reference to the current object (e.g. C++ `this` or Python `self`)",
)


@mod.action_class
class Actions:
    def code_operator_object_accessor():
        """Inserts the object accessor operator (e.g., Java's "." or PHP's "->)"""

    def code_define_class():
        """Starts a class definition (e.g., Java's "class" keyword)"""
