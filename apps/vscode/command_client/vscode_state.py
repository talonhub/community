from collections import defaultdict
from dataclasses import dataclass
from talon import Context, Module, actions, app, ui, cron, fs

from .command_client import get_communication_dir_path, read_json_with_timeout

mod = Module()

ctx = Context()
global_ctx = Context()
mac_ctx = Context()

ctx.matches = r"""
app: vscode
and tag: user.vscode_command_server
"""
mac_ctx.matches = r"""
os: mac
app: vscode
and tag: user.vscode_command_server
"""


@dataclass
class Listener:
    callback: callable


listeners: defaultdict[str, list[Listener]] = defaultdict(list)


@mod.action_class
class Actions:
    def trigger_command_server_update_core_state():
        """Issue keystroke to trigger command server to save state"""
        pass

    def vscode_update_client_state_debounced():
        """Ask vscode to save state, debouncing.  Only implemented in vscode"""
        pass

    def vscode_update_client_state_and_wait():
        """Ask vscode to save state and wait for update to complete.  Only implemented in vscode"""
        pass

    def watch_vscode_state(key: str, callback: callable):
        """Watch a particular vscode state key"""
        # TODO: Handle case where communication dir doesn't exist: how do we
        # start watching after they install extension?
        global listeners
        listener = Listener(callback)
        listeners[key].append(listener)

        def unsubscribe():
            listeners[key].remove(listener)

        try:
            actions.user.vscode_update_client_state_debounced()
        except NotImplementedError:
            pass

        return unsubscribe


@global_ctx.action_class("user")
class UserActions:
    def trigger_command_server_update_core_state():
        pass

    def vscode_update_client_state_debounced():
        pass

    def vscode_update_client_state_and_wait():
        pass


save_state_job = None


@ctx.action_class("user")
class UserActions:
    def trigger_command_server_update_core_state():
        actions.key("ctrl-shift-f10")

    def vscode_update_client_state_debounced():
        global save_state_job

        if save_state_job is not None:
            cron.cancel(save_state_job)

        save_state_job = cron.after(
            "25ms",
            lambda: actions.user.vscode_update_client_state_and_wait(),
        )

    def vscode_update_client_state_and_wait():
        global listeners

        actions.user.trigger_command_server_update_core_state()

        result = actions.user.vscode_get(
            "command-server.getState", [{"key": key} for key in listeners.keys()]
        )
        for key, value in result.items():
            for listener in listeners[key]:
                listener.callback(value["newValue"])


@mac_ctx.action_class("user")
class MacUserActions:
    def trigger_command_server_update_core_state():
        actions.key("cmd-shift-f10")


def get_state_updated_signal_path():
    return get_communication_dir_path() / "stateUpdatedSignal"


def on_ready():
    ui.register(
        "app_activate", lambda _: actions.user.vscode_update_client_state_debounced()
    )
    path = get_state_updated_signal_path().resolve()
    fs.watch(
        path,
        lambda _1, _2: actions.user.vscode_update_client_state_debounced(),
    )


app.register("ready", on_ready)


# - [ ] Add watch file that vscode can use to signal change may have happened
# - [ ] Bake settings.json terminal fix into code
# - [ ] How do we update in response to keypresses?
#   - For example presssing enter or escape could change the state
#   - Could override insert / key to do a debounced cron.after with update
#   - Or could just trigger on enter / escape somehow
# - [x] Use command client so that we can actually wait for the state to be updated
# - [x] Add API for client code to watch a key in the map
# - [x] Trigger keypress every time we switch to VSCode application
# - [x] Debounce the cron.after