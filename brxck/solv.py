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
    "dappy tasks": "dapi-tasks",
    "dappy": "dapi",
    "mapp": "mapp-dev",
    "release": "release",
    "schema": "schema",
    "turbo provider": "turbo-provider",
    "turbo consumer": "turbo-consumer",
}

# Linear magic words
mod.list("linear_keyword", desc="Linear magic words")
ctx.lists["user.linear_keyword"] = {
    "close": "close",
    "closes": "closes",
    "closed": "closed",
    "closing": "closing",
    "fix": "fix",
    "fixes": "fixes",
    "fixed": "fixed",
    "fixing": "fixing",
    "resolve": "resolve",
    "resolves": "resolves",
    "resolved": "resolved",
    "resolving": "resolving",
    "complete": "complete",
    "completes": "completes",
    "completed": "completed",
    "completing": "completing",
    "ref": "ref",
    "references": "references",
    "part of": "part of",
    "related to": "related to",
    "contributes to": "contributes to",
    "towards": "towards",
}
