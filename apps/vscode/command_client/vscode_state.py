from talon import Context, Module, actions, app, ui, cron, fs

from .command_client import get_communication_dir_path, read_json_with_timeout

mod = Module()

ctx = Context()
mac_ctx = Context()

ctx.matches = r"""
app: vscode
"""
mac_ctx.matches = r"""
os: mac
app: vscode
"""


@mod.action_class
class Actions:
    def trigger_command_server_save_state():
        """Issue keystroke to trigger command server to save state"""
        pass

    def vscode_save_state_debounced():
        """Ask vscode to save state, debouncing.  Only implemented in vscode"""
        pass

    def watch_vscode_state(key: str, callback: callable):
        """Watch a particular vscode state key"""
        # TODO: Handle case where communication dir doesn't exist: how do we
        # start watching after they install extension?
        state_dir = get_state_dir_path().resolve(strict=True)
        state_file_path = state_dir / key

        def on_watch(path, flags):
            if state_file_path.match(path):
                value = read_json_with_timeout(state_file_path)
                callback(value)

        fs.watch(state_file_path, on_watch)

        def unsubscribe():
            fs.unwatch(state_file_path, on_watch)

        value = read_json_with_timeout(state_file_path)
        callback(value)

        return unsubscribe


save_state_job = None


@ctx.action_class("user")
class UserActions:
    def trigger_command_server_save_state():
        actions.key("ctrl-shift-f10")

    def vscode_save_state_debounced():
        global save_state_job

        if save_state_job is not None:
            cron.cancel(save_state_job)

        save_state_job = cron.after(
            "250ms", lambda: actions.user.trigger_command_server_save_state()
        )


@mac_ctx.action_class("user")
class MacUserActions:
    def trigger_command_server_save_state():
        actions.key("cmd-shift-f10")


def get_state_dir_path():
    """Returns directory that is used by command-server for exposing state

    Returns:
        Path: The path to the state dir
    """
    return get_communication_dir_path() / "state"


def on_app_activate(_):
    try:
        actions.user.vscode_save_state_debounced()
    except NotImplementedError:
        pass


app.register("ready", lambda: ui.register("app_activate", on_app_activate))


# - [ ] Add watch file that vscode can use to signal change may have happened
# - [ ] Use command client so that we can actually wait for the state to be updated
# - [x] Add API for client code to watch a key in the map
# - [x] Trigger keypress every time we switch to VSCode application
# - [x] Debounce the cron.after
# - [ ] Bake settings.json terminal fix into code
# - [ ] How do we update in response to keypresses?
#   - For example presssing enter or escape could change the state
#   - Could override insert / key to do a debounced cron.after with update
#   - Or could just trigger on enter / escape somehow