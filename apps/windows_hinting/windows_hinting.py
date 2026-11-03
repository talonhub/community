from talon import Context, Module, actions, app, ui

from .windows_hinting_pipe import (
    FALLBACK_ACTION_KEYS,
    SELECT_ACTIONS,
    PipeNotFoundError,
    WindowsHintingError,
    call,
    normalize_label,
)

mod = Module()
ctx = Context()
ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""

@ctx_win.capture("user.hinting_double", rule="<user.letter> (twice | second)")
def hinting_double(m) -> str:
    return f"{m.letter} {m.letter}"

@ctx_win.capture("user.hinting", rule="<user.letter> | <user.letter> <user.letter> | <user.hinting_double> ")
def hinting(m) -> str:
    return " ".join(m)

is_window_hinting_active = False
@mod.scope
def scope():
    return {"windows_hinting_active": f"{is_window_hinting_active}"}

def on_title(win):
    global is_window_hinting_active
    if win.app.name in ("Windows-Hinting", "Windows-Hinting.exe"):
        print(f"Window title: {win.title}")
        if "[Active]" in win.title:
            is_window_hinting_active = True
        else:
            is_window_hinting_active = False

        scope.update()

def on_ready():
    ui.register("win_title", on_title)

app.register("ready", on_ready)


# --- RPC (Windows-Hinting docs/design/named-pipe-rpc.md) ---------------------------------

# Toggling waits for the hint scan, which Windows-Hinting caps at ScanTimeoutMs (2.5 s).
TOGGLE_TIMEOUT_MS = 5000
COMMAND_TIMEOUT_MS = 2000

# Server refusals worth surfacing to the user rather than just logging.
NOTIFY_CODES = ("ERR_ELEVATED_TARGET", "ERR_LABEL_NOT_FOUND", "ERR_NOT_ACTIVE")

NO_PIPE = object()
_warned_no_pipe = False


def _rpc(command: str, args=(), timeout_ms: int = COMMAND_TIMEOUT_MS):
    """Call the RPC pipe. Returns the response dict, None if the call failed (already
    logged), or NO_PIPE when there is no pipe (Windows-Hinting not running, or a build
    without RPC) so the caller can fall back to keystrokes."""
    global _warned_no_pipe
    try:
        response = call(command, list(args), timeout_ms)
    except PipeNotFoundError:
        if not _warned_no_pipe:
            print("windows_hinting: RPC pipe not found; falling back to keystrokes")
            _warned_no_pipe = True
        return NO_PIPE
    except WindowsHintingError as e:
        print(f"windows_hinting: {command} {list(args)} failed: {e}")
        if e.code in NOTIFY_CODES:
            app.notify("Windows-Hinting", e.message or e.code)
        return None
    _warned_no_pipe = False
    return response


@mod.action_class
class Actions:
    def windows_hinting_toggle():
        """Toggle Windows-Hinting hints for the foreground window"""
        if _rpc("toggle", timeout_ms=TOGGLE_TIMEOUT_MS) is NO_PIPE:
            actions.key("ctrl-alt-h")

    def windows_hinting_toggle_taskbar():
        """Toggle Windows-Hinting hints for the taskbar"""
        if _rpc("toggle_taskbar", timeout_ms=TOGGLE_TIMEOUT_MS) is NO_PIPE:
            actions.key("ctrl-alt-t")

    def windows_hinting_select(label: str, action: str = ""):
        """Activate the Windows-Hinting hint with this label (letters, spaces ignored).
        action: '' (default activation), left, right, double, move, ctrl or shift"""
        if action not in SELECT_ACTIONS:
            raise ValueError(f"windows_hinting_select: unknown action {action!r}")
        label = normalize_label(label)
        args = [label, action] if action else [label]
        if _rpc("select", args) is NO_PIPE:
            if action:
                actions.key(FALLBACK_ACTION_KEYS[action])
                actions.sleep("100ms")
            actions.key(" ".join(label.lower()))
            actions.key("enter")

    def windows_hinting_deactivate():
        """Hide Windows-Hinting hints"""
        if _rpc("deactivate") is NO_PIPE:
            actions.key("escape")

    def windows_hinting_status() -> dict:
        """Windows-Hinting session state: active, source, mode, pendingAction, hintCount"""
        response = _rpc("status")
        return response.get("data", {}) if isinstance(response, dict) else {}
