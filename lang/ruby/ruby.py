from talon import Context, actions, settings

ctx = Context()
ctx.matches = r"""
mode: user.ruby
mode: command
and code.language: ruby
"""

@ctx.action_class("user")
class UserActions:
    def code_default_function(text: str):
        """Inserts function definition"""

        result = "def {}".format(
            actions.user.formatted_text(
                text,
                settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
