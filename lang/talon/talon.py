from talon import Module, Context, actions, ui, imgui, clip, settings, registry, app

mod = Module()
ctx = Context()
ctx_global = Context()
mod.tag("talon_python", "Tag to activate talon-specific python commands")
mod.list("talon_actions")
mod.list("talon_lists")
mod.list("talon_captures")
mod.list("talon_apps")
mod.list("talon_tags")
mod.list("talon_modes")
mod.list("talon_settings")
mod.list("talon_scopes")
mod.list("talon_modes")

ctx.matches = r"""
mode: user.talon
mode: user.auto_lang 
and code.language: talon
"""
ctx.lists["user.code_functions"] = {
    "insert": "insert",
    "key": "key",
    "print": "print",
    "repeat": "repeat",
}


def update_lists(decls):
    # print("update_lists")
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
        ctx_global.lists[
            f"user.talon_{thing}"
        ] = actions.user.create_spoken_forms_from_list(
            l.keys(), generate_subsequences=False
        )
        # print(
        #     "List: {} \n {}".format(thing, str(ctx_global.lists[f"user.talon_{thing}"]))
        # )


def on_ready():
    # print("on_ready")
    update_lists(registry.decls)
    registry.register("update_decls", update_lists)


app.register("ready", on_ready)


@ctx.action_class("user")
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

    def code_comment():
        actions.auto_insert("#")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()
