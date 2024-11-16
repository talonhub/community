from talon import Context, Module, actions, grammar, settings, ui
mod = Module()
mod.apps.i_phone_mirroring = """
os: mac
and app.bundle: com.apple.ScreenContinuity
"""