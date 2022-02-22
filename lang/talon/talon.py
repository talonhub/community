from talon import Module, Context, actions, ui, imgui, clip, settings, registry, app

mod = Module()
ctx = Context()


ctx_talon_lists = Context()

# restrict all the talon_* lists to when the user.talon_populate_lists tag 
# is active to prevent them from being active in contexts where they are not wanted.
# Do not enable this tag with dragon, as it will be unusable.
# with conformer, the latency increase may also be unacceptable depending on your cpu
# see https://github.com/knausj85/knausj_talon/issues/600
ctx_talon_lists.matches = r"""
tag: user.talon_populate_lists
"""

mod.tag("talon_python", "Tag to activate talon-specific python commands")
mod.tag("talon_populate_lists", "Tag to activate talon-specific lists of actions, scopes, modes etcetera. Do not use this tag with dragon")
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
tag: user.talon
"""
ctx.lists["user.code_functions"] = {
    "insert": "insert",
    "key": "key",
    "print": "print",
    "repeat": "repeat",
}


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
        ctx_talon_lists.lists[
            f"user.talon_{thing}"
        ] = actions.user.create_spoken_forms_from_list(
            l.keys(), generate_subsequences=False
        )
        # print(
        #     "List: {} \n {}".format(thing, str(ctx_talon_lists.lists[f"user.talon_{thing}"]))
        # )


def on_ready():
    # print("on_ready")
    on_update_decls(registry.decls)
    registry.register("update_decls", on_update_decls)


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

    def code_comment_line_prefix():
        actions.auto_insert("#")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()
