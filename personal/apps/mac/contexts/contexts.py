from talon import ui, Module, Context, registry, actions, imgui, cron

mod = Module()
mod.apps.contexts = """
os: mac
and app.bundle: com.contextsformac.Contexts
"""