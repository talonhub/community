from talon import Context, Module, actions, app, registry

mod = Module()
ctx_talon = Context()
ctx_talon_python = Context()
ctx_talon_lists = Context()

# restrict all the talon_* lists to when the user.talon_populate_lists tag
# is active to prevent them from being active in contexts where they are not wanted.
# Do not enable this tag with dragon, as it will be unusable.
# with conformer, the latency increase may also be unacceptable depending on your cpu
# see https://github.com/talonhub/community/issues/600
ctx_talon_lists.matches = r"""
tag: user.talon_populate_lists
"""

mod.tag("talon_python", "Tag to activate talon-specific python commands")
mod.tag(
    "talon_populate_lists",
    "Tag to activate talon-specific lists of actions, scopes, modes etcetera. Do not use this tag with dragon",
)
mod.list("talon_actions")
mod.list("talon_lists")
mod.list("talon_captures")
mod.list("talon_apps")
mod.list("talon_tags")
mod.list("talon_modes")
mod.list("talon_settings")
mod.list("talon_scopes")
mod.list("talon_modes")

ctx_talon.matches = r"""
code.language: talon
"""

ctx_talon_python.matches = r"""
tag: user.talon_python
"""


def on_update_decls(decls):
    # todo modes?
    for thing in [
        "actions",
        "lists",
        "captures",
        "tags",
        "apps",
        "settings",
        "scopes",
        "modes",
    ]:
        l = getattr(decls, thing)
        ctx_talon_lists.lists[f"user.talon_{thing}"] = (
            actions.user.create_spoken_forms_from_list(
                l.keys(), generate_subsequences=False
            )
        )
        # print(
        #     "List: {} \n {}".format(thing, str(ctx_talon_lists.lists[f"user.talon_{thing}"]))
        # )


def on_ready():
    # print("on_ready")
    on_update_decls(registry.decls)
    registry.register("update_decls", on_update_decls)


app.register("ready", on_ready)


@mod.action_class
class Actions:
    def talon_code_insert_action_call(text: str, selection: str):
        """inserts talon-specific action call"""
        actions.user.code_insert_function(text, selection)

    def talon_code_enable_tag(tag: str):
        """enables tag in either python or talon files"""

    def talon_code_enable_setting(setting: str):
        """asserts setting in either python or talon files"""


@ctx_talon.action_class("user")
class TalonActions:
    def talon_code_enable_tag(tag: str):
        """enables tag in either python or talon files"""
        actions.user.paste(f"tag(): {tag}")

    def talon_code_enable_setting(setting: str):
        """asserts setting in either python or talon files"""
        actions.user.paste(f"{setting} = ")


@ctx_talon_python.action_class("user")
class TalonPythonActions:
    def talon_code_insert_action_call(text: str, selection: str):
        text = f"actions.{text}({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def talon_code_enable_tag(tag: str):
        """enables tag in either python or talon files"""
        actions.user.paste(f'ctx.tags = ["{tag}"]')
        if not tag:
            actions.edit.left()
            actions.edit.left()

    def talon_code_enable_setting(setting: str):
        """asserts setting in either python or talon files"""
        if not setting:
            actions.user.insert_between('ctx.settings["', '"] = ')
        else:
            actions.user.paste(f'ctx.settings["{setting}"] = ')


@ctx_talon.action_class("user")
class UserActions:
    def code_operator_and():
        actions.auto_insert(" and ")

    def code_operator_or():
        actions.auto_insert(" or ")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_comment_line_prefix():
        actions.auto_insert("#")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()
