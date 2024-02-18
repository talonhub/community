import os
import re
from itertools import islice
from pathlib import Path

from talon import Module, actions, app, ui

APPS_DIR = Path(__file__).parent.parent.parent / "apps"

mod = Module()


@mod.action_class
class Actions:
    def talon_create_app_context(platform_suffix: str = None):
        """Create a new directory with talon and python context files for the current application"""
        active_app = ui.active_app()
        app_name = get_app_name(active_app.name)
        app_dir = APPS_DIR / app_name
        talon_file = app_dir / f"{app_name}.talon"
        python_file = app_dir / f"{get_platform_filename(app_name, platform_suffix)}.py"

        talon_context = get_talon_context(app_name)
        python_context = get_python_context(active_app, app_name)

        if not app_dir.is_dir():
            os.mkdir(app_dir)

        talon_file_created = create_file(talon_file, talon_context)
        python_file_created = create_file(python_file, python_context)

        if talon_file_created or python_file_created:
            actions.user.file_manager_open_directory(str(app_dir))


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
os: {os}
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


def get_platform_filename(app_name: str, platform_suffix: str = None) -> str:
    if platform_suffix:
        return f"{app_name}_{platform_suffix}"
    return app_name


def get_app_context(active_app: ui.App) -> str:
    if app.platform == "mac":
        return f"app.bundle: {active_app.bundle}"
    if app.platform == "windows":
        executable = os.path.basename(active_app.exe)
        return f"app.exe: /^{re.escape(executable.lower())}$/i"
    return f"app.name: {active_app.name}"


def get_app_name(text: str, max_len=20) -> str:
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    return "_".join(
        list(islice(pattern.findall(text.removesuffix(".exe")), max_len))
    ).lower()


def create_file(path: Path, content: str) -> bool:
    if path.is_file():
        actions.app.notify(f"Application context file '{path}' already exists")
        return False

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return True
