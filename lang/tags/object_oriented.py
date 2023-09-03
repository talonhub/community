from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag(
    "code_object_oriented",
    desc="Tag for enabling basic object oriented programming commands (objects, classes, etc)",
)

mod.list(
    "code_self",
    desc="Reference to the current object (e.g. C++ `this` or Python `self`)",
)

mod.list(
    "code_operator_object_accessor",
    desc="An object accessor operator (e.g. Java `.` or PHP `->`)",
)

ctx.lists["self.code_operator_object_accessor"] = {
    "dot": ".",
}


@mod.action_class
class Actions:
    def code_define_class():
        """Starts a class definition (e.g., Java's "class" keyword)"""
