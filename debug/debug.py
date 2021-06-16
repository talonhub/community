from talon import Context, Module, registry

ctx = Context()
mod = Module()

@mod.action_class
class module_actions:
    def debug_active_context():
        """dump out the active contexts"""
        print(registry.active_contexts())

