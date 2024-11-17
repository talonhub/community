from talon import Context, Module, actions, grammar, settings, ui
mod = Module()
mod.apps.i_phone_mirroring = """
os: mac
and app.bundle: com.apple.ScreenContinuity
"""
mod.list(
    "phone_applications",
    desc="list of known iPhone applications",
)
ctx = Context()

ctx.lists["user.phone_applications"] = {
    "github": "github", 
    "messages": "messages", 
}