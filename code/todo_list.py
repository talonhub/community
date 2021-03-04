from talon import Context, actions, ui, Module, app

mod = Module()
mod.tag("todo_list", desc="Tag for enabling generic todo list commands")


@mod.action_class
class Actions:
    def mark_complete():
        """Mark a todo as completed"""
        pass

    def mark_cancelled():
        """Mark a todo as cancelled"""
        pass

    def show_today():
        """Show today"""
        pass

    def show_inbox():
        """Show inbox"""
        pass

    def show_upcoming():
        """Show upcoming"""
        pass

    def show_anytime():
        """Show anytime"""
        pass

    def show_someday():
        """Show someday"""
        pass

    def show_logbook():
        """Show logbook"""
        pass
