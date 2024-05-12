from talon import Module, settings, actions

mod = Module()

@mod.action_class
class Actions:
    def say(text: str):
        """poor man's dictation"""
        if settings.get("user.context_sensitive_dictation"):
            actions.user.dictation_insert(text)
        else:
            actions.insert(text)
            
        

    
