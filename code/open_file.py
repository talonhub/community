# Actions for opening files in appropriate applications.
from talon import Module, Context, actions, ui, app
import os

# path to knausj root directory
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.join(REPO_DIR, 'settings')

mod = Module()
ctx = Context()

mod.list('talon_settings_csv', desc="Absolute paths to talon user settings csv files.")
_csvs = {
    x: os.path.join(SETTINGS_DIR, '_'.join(x.split()) + ".csv")
    for x in ["file extensions", "search engines", "system paths",
              "websites", "words to replace", "additional words"]
}
_csvs.update({
    "homophones": os.path.join(REPO_DIR, 'code', 'homophones.csv'),
})
ctx.lists['self.talon_settings_csv'] = _csvs

@mod.action_class
class ModuleActions:
    def open_file(path: str, directory: str = None):
        """Opens a file in the appropriate application for its type. If the path is relative, opens in the given directory (defaults to user's home directory)."""
        # if the path is relative, directory is relevant.
        if not os.path.isabs(path):
            directory = directory or actions.path.user_home()
            path = os.path.join(directory, path)
        if not os.path.exists(path):
            app.notify(f"No file found at {path}")
            raise FileNotFoundError(path)
        if app.platform == "windows":
            os.startfile(path, 'open')
        elif app.platform == "mac":
            ui.launch(path="open", args=[path])
        elif app.platform == "linux":
            ui.launch(path='/usr/bin/xdg-open', args=[path])
        else:
            raise Exception(f'unknown platform: {app.platform}')
        actions.sleep('500ms')
