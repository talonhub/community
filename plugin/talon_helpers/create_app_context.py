import os
import re
from itertools import islice
from pathlib import Path

from talon import Module, actions, app, ui

APPS_DIR = Path(__file__).parent.parent.parent / "apps"

mod = Module()


@mod.action_class
class Actions:
    def talon_create_app_context():
        """Create a new python context file for the current application"""
        active_app = ui.active_app()
        app_name = get_app_name(active_app.name)
        app_dir = APPS_DIR / app_name
        filename = get_filename(app_name)
        talon_file = app_dir / f"{filename}.talon"
        python_file = app_dir / f"{filename}.py"

        talon_context = get_talon_context(app_name)
        python_context = get_python_context(active_app, app_name)

        if not app_dir.is_dir():
            os.mkdir(app_dir)

        create_file(talon_file, talon_context)
        create_file(python_file, python_context)


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
    return f"""app: {app_name}
-

"""


def get_filename(app_name: str) -> str:
    platform = app.platform if app.platform != "windows" else "win"
    return f"{app_name}_{platform}"


def get_app_context(active_app: ui.App) -> str:
    if app.platform == "mac":
        return f"app.bundle: {active_app.bundle}"
    if app.platform == "windows":
        return f"app.exe: {active_app.exe.split(os.path.sep)[-1]}"
    return f"app.name: {active_app.name}"


def get_app_name(text: str, max_len=20) -> str:
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    return "_".join(
        list(islice(pattern.findall(text.replace(".exe", "")), max_len))
    ).lower()


def create_file(path: Path, content: str):
    if path.is_file():
        print(f"Application context file '{path}' already exists")
        return

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
