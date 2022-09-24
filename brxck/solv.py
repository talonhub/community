from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("botler_command", desc="Botler commands")
ctx.lists["user.botler_command"] = {
    "diff": "diff",
    "peek": "peek",
    "release": "release",
    "livestage": "livestage",
}

mod.list("solv_repository", desc="Solv repository names")
ctx.lists["user.solv_repository"] = {
    "dapi tasks": "dapi-tasks",
    "dapi": "dapi",
    "jigsaw": "jigsaw",
    "manage": "manage-dev",
    "mapp": "mapp-dev",
    "release": "release",
    "schema": "schema",
    "turbosnails": "turbosnails",
}
