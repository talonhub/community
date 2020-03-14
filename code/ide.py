from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def complete():
         """Trigger auto complete in the ide (intellijsense)"""

    def perfect():
         """Trigger better auto complete in the ide"""

    def smart():
         """Trigger type completion in the ide"""

    def finish():
        """Select auto complete statement"""

    def done():
        """Select auto complete statement"""

    def toggle_tools():
         """Hide all windows"""

    def extract_variable():
        """Trigger extract variable functionality of IDE"""

    def extract_field():
        """Trigger extract field functionality of IDE"""

    def extract_constant():
        """Trigger extract constant functionality of IDE"""

    def extract_parameter():
        """Trigger extract parameter functionality of IDE"""

    def extract_interface():
        """Trigger extract interface functionality of IDE"""

    def extract_method():
        """Trigger extract method functionality of IDE"""

    def refactor_in_line():
        """Trigger inline refactoring method of IDE"""

    def refactor_move():
        """Trigger refactor move functionality of IDE"""

    def refactor_rename():
        """Trigger refactor rename functionality of IDE"""

    def rename_file():
        """Trigger rename file of IDE"""