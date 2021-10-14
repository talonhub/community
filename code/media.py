from talon import actions, Module, Context, app

mod = Module()

@mod.action_class
class Actions:
    def play_pause():
        """Plays or pauses media"""
        if app.platform == "windows":
          actions.key("play_pause")
        else:
          actions.key("play")
