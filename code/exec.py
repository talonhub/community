import os
import subprocess

from talon import Module, actions, app, ui, settings

mod = Module()

setting_eof_keys = mod.setting(
    "eof_keys",
    type=str,
    default=None,
    desc="Shortcut key(s) for moving to end of file in your default editor, e.g. 'ctrl-end'.",
)

@mod.action_class
class Actions:
    def system_command(cmd: str):
        """execute a command on the system"""
        os.system(cmd)

    def system_command_nb(cmd: str):
        """execute a command on the system without blocking"""
        subprocess.Popen(cmd, shell=True)

    def get_repo_relpath():
        """Get path of the repo containing this file, relative to the talon user folder"""
        return os.path.dirname(os.path.dirname(os.path.relpath(__file__, actions.path.talon_user())))

    def edit_additional_words():
        """execute a command on the system without blocking"""
        repo_dir = actions.user.get_repo_relpath()
        path = os.path.join(repo_dir, 'settings', 'additional_words.csv')
        actions.user.edit_talon_user_csv(path)

    def edit_words_to_replace():
        """execute a command on the system without blocking"""
        repo_dir = actions.user.get_repo_relpath()
        path = os.path.join(repo_dir, 'settings', 'words_to_replace.csv')
        actions.user.edit_talon_user_csv(path)

    def edit_abbreviations():
        """execute a command on the system without blocking"""
        repo_dir = actions.user.get_repo_relpath()
        path = os.path.join(repo_dir, 'settings', 'abbreviate.csv')
        actions.user.edit_talon_user_csv(path)

    def edit_homophones():
        """execute a command on the system without blocking"""
        repo_dir = actions.user.get_repo_relpath()
        path = os.path.join(repo_dir, 'settings', 'homophones.csv')

        abs_path = os.path.join(actions.path.talon_user(), path)
        if not os.path.exists(abs_path):
            # create an empty file
            open(abs_path, 'a').close()

        actions.user.edit_talon_user_csv(path)

    def edit_talon_user_csv(talon_user_file_path: str) -> None:
        """Opens a .csv file under the talon user folder using the default application"""

        if not os.path.relpath(talon_user_file_path):
            print('edit_talon_user_csv: can only open files under the talon user folder!')

        if not talon_user_file_path.endswith(".csv"):
            print('edit_talon_user_csv: can only open .csv files!')

        path = os.path.join(actions.path.talon_user(), talon_user_file_path)

        eof_keys = settings.get('user.csv_eof_keys')

        if app.platform == "windows":
            os.startfile(path, 'open')

            if not eof_keys:
                eof_keys='ctrl-end'
        elif app.platform == "mac":
            ui.launch(path='open', args=[str(path)])

            if not eof_keys:
                eof_keys='cmd-down'
        elif app.platform == "linux":
            ui.launch(path='/usr/bin/xdg-open', args=[str(path)])

            if not eof_keys:
                eof_keys='ctrl-end'
        else:
            raise Exception(f'unknown system: {app.platform}')

        actions.sleep("500ms")
        actions.key(eof_keys)
        actions.sleep("500ms")
        actions.key("enter")
