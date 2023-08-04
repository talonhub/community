from talon import Module, app, actions, ui
from pathlib import Path
from itertools import islice
import os, re

APPS_DIR = Path(__file__).parent.parent.parent / "apps"

mod = Module()


@mod.action_class
class Actions:
    def talon_create_app_context():
        """Create a new python context file for the current application"""
        active_app = ui.active_app()
        app_name = create_name(active_app.name)
        app_dir = APPS_DIR / app_name
        talon_file = app_dir / f"{app_name}.talon"
        python_file = app_dir / f"{app_name}.py"

        if app_dir.is_dir():
            raise OSError(f"Application directory '{app_name}' already exists")

        talon_context = get_talon_context(app_name)
        python_context = get_python_context(active_app, app_name)

        os.mkdir(app_dir)

        with open(talon_file, "w", encoding="utf-8") as file:
            file.write(talon_context)

        with open(python_file, "w", encoding="utf-8") as file:
            file.write(python_context)


def get_python_context(active_app: ui.App, app_name: str) -> str:
    return '''\
from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.{app_name} = r"""
os: {os}
and {app_context}
"""

ctx.matches = r"""
app: {app_name}
"""

# @mod.action_class
# class Actions:
'''.format(
        app_name=app_name,
        os=app.platform,
        app_context=get_app_context(active_app),
    )


def get_talon_context(app_name: str) -> str:
    return """\
app: {app_name}
-

""".format(
        app_name=app_name,
    )


def get_app_context(active_app: ui.App) -> str:
    if app.platform == "mac":
        return f"app.bundle: {active_app.bundle}"
    if app.platform == "windows":
        return f"app.exe: {active_app.exe.split(os.path.sep)[-1]}"
    return f"app.name: {active_app.name}"


def create_name(text: str, max_len=20) -> str:
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    return "_".join(
        list(islice(pattern.findall(text.replace(".exe", "")), max_len))
    ).lower()
