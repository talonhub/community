"""Client for the Windows-Hinting RPC pipe (docs/design/named-pipe-rpc.md in Windows-Hinting).

Pure Python + ctypes, no ``talon`` import, so it can be unit-tested outside Talon.
One request per connection: write a JSON line, read a JSON line, close.
"""

import itertools
import json
import os
import sys
import time

PROTOCOL = 1
PIPE_PREFIX = r"\\.\pipe\WindowsHinting-"
MAX_RESPONSE_BYTES = 64 * 1024

ERROR_FILE_NOT_FOUND = 2
ERROR_BROKEN_PIPE = 109
ERROR_SEM_TIMEOUT = 121
ERROR_PIPE_BUSY = 231
ERROR_PIPE_NOT_CONNECTED = 233


class WindowsHintingError(Exception):
    """A failed call. ``code`` is the server's ERR_* code, or a CLIENT_* code."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


class PipeNotFoundError(WindowsHintingError):
    """No Windows-Hinting pipe: the app is not running, or the build predates RPC."""

    def __init__(self, message: str = ""):
        super().__init__("CLIENT_PIPE_NOT_FOUND", message)


_ids = itertools.count(1)


def encode_request(command: str, args=None, request_id: str = None) -> bytes:
    request = {
        "protocol": PROTOCOL,
        "command": command,
        "args": [str(a) for a in (args or [])],
        "id": request_id or f"{os.getpid()}-{next(_ids)}",
    }
    return (json.dumps(request, separators=(",", ":")) + "\n").encode("utf-8")


def decode_response(line: bytes, request_id: str = None) -> dict:
    """Parse one response line; raise WindowsHintingError unless ``ok`` is true."""
    try:
        response = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as e:
        raise WindowsHintingError("CLIENT_BAD_RESPONSE", f"unparseable response: {e}") from e
    if not isinstance(response, dict):
        raise WindowsHintingError("CLIENT_BAD_RESPONSE", "response is not a JSON object")
    if request_id is not None and response.get("id") not in (None, request_id):
        raise WindowsHintingError(
            "CLIENT_BAD_RESPONSE", f"response id {response.get('id')!r} != {request_id!r}"
        )
    if not response.get("ok"):
        raise WindowsHintingError(
            response.get("code") or "CLIENT_BAD_RESPONSE", response.get("message") or ""
        )
    return response


def call(command: str, args=None, timeout_ms: int = 1000, transport_factory=None) -> dict:
    """Send one command and return the response dict (``data`` holds any payload)."""
    request_id = f"{os.getpid()}-{next(_ids)}"
    payload = encode_request(command, args, request_id)
    factory = transport_factory or (lambda t: PipeTransport(pipe_name(), t))
    deadline = time.monotonic() + timeout_ms / 1000
    transport = factory(timeout_ms)
    try:
        transport.write(payload)
        line = transport.read_line(deadline, MAX_RESPONSE_BYTES)
    finally:
        transport.close()
    return decode_response(line, request_id)


def pipe_name() -> str:
    return PIPE_PREFIX + current_user_sid()


# --- Win32 transport -------------------------------------------------------------------

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _adv = ctypes.WinDLL("advapi32", use_last_error=True)

    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3
    SECURITY_SQOS_PRESENT = 0x00100000
    SECURITY_ANONYMOUS = 0x00000000
    TOKEN_QUERY = 0x0008
    TOKEN_USER_CLASS = 1
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    _k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                                 wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    _k32.CreateFileW.restype = wintypes.HANDLE
    _k32.WaitNamedPipeW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD]
    _k32.WaitNamedPipeW.restype = wintypes.BOOL
    _k32.WriteFile.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.DWORD,
                               ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    _k32.WriteFile.restype = wintypes.BOOL
    _k32.ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                              ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    _k32.ReadFile.restype = wintypes.BOOL
    _k32.PeekNamedPipe.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                                   ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD),
                                   ctypes.POINTER(wintypes.DWORD)]
    _k32.PeekNamedPipe.restype = wintypes.BOOL
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]
    _k32.CloseHandle.restype = wintypes.BOOL
    _k32.GetCurrentProcess.restype = wintypes.HANDLE
    _k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _k32.OpenProcess.restype = wintypes.HANDLE
    _k32.GetNamedPipeServerProcessId.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.ULONG)]
    _k32.GetNamedPipeServerProcessId.restype = wintypes.BOOL
    _k32.LocalFree.argtypes = [wintypes.HLOCAL]
    _k32.LocalFree.restype = wintypes.HLOCAL
    _adv.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    _adv.OpenProcessToken.restype = wintypes.BOOL
    _adv.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID,
                                         wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    _adv.GetTokenInformation.restype = wintypes.BOOL
    _adv.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
    _adv.ConvertSidToStringSidW.restype = wintypes.BOOL

    def _winerr(what: str) -> OSError:
        err = ctypes.get_last_error()
        return ctypes.WinError(err, f"{what} failed")

    def _process_user_sid(process) -> str:
        token = wintypes.HANDLE()
        if not _adv.OpenProcessToken(process, TOKEN_QUERY, ctypes.byref(token)):
            raise _winerr("OpenProcessToken")
        try:
            size = wintypes.DWORD()
            _adv.GetTokenInformation(token, TOKEN_USER_CLASS, None, 0, ctypes.byref(size))
            buf = ctypes.create_string_buffer(size.value)
            if not _adv.GetTokenInformation(token, TOKEN_USER_CLASS, buf, size, ctypes.byref(size)):
                raise _winerr("GetTokenInformation")
            # TOKEN_USER starts with SID_AND_ATTRIBUTES, whose first field is the PSID.
            psid = ctypes.cast(buf, ctypes.POINTER(wintypes.LPVOID))[0]
            text = wintypes.LPWSTR()
            if not _adv.ConvertSidToStringSidW(psid, ctypes.byref(text)):
                raise _winerr("ConvertSidToStringSidW")
            try:
                return text.value
            finally:
                _k32.LocalFree(ctypes.cast(text, wintypes.HLOCAL))
        finally:
            _k32.CloseHandle(token)

    _sid_cache = None

    def current_user_sid() -> str:
        global _sid_cache
        if _sid_cache is None:
            _sid_cache = _process_user_sid(_k32.GetCurrentProcess())
        return _sid_cache

    def open_pipe(name: str, timeout_ms: int):
        """Open the pipe with anonymous impersonation, waiting up to timeout_ms if busy."""
        deadline = time.monotonic() + timeout_ms / 1000
        while True:
            handle = _k32.CreateFileW(
                name, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING,
                SECURITY_SQOS_PRESENT | SECURITY_ANONYMOUS, None,
            )
            if handle != INVALID_HANDLE_VALUE:
                return handle
            err = ctypes.get_last_error()
            if err == ERROR_FILE_NOT_FOUND:
                raise PipeNotFoundError(name)
            if err != ERROR_PIPE_BUSY:
                raise WindowsHintingError("CLIENT_IO", f"CreateFileW: {ctypes.FormatError(err)}")
            remaining = int((deadline - time.monotonic()) * 1000)
            if remaining <= 0 or not _k32.WaitNamedPipeW(name, remaining):
                raise WindowsHintingError("CLIENT_TIMEOUT", "pipe busy")

    def verify_server(handle) -> None:
        """Refuse a pipe whose server process runs as a different user (squatter check)."""
        pid = wintypes.ULONG()
        if not _k32.GetNamedPipeServerProcessId(handle, ctypes.byref(pid)):
            raise WindowsHintingError("CLIENT_UNTRUSTED_SERVER", "cannot identify server process")
        process = _k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
        if not process:
            raise WindowsHintingError("CLIENT_UNTRUSTED_SERVER", f"cannot open server pid {pid.value}")
        try:
            server_sid = _process_user_sid(process)
        except OSError as e:
            raise WindowsHintingError("CLIENT_UNTRUSTED_SERVER", str(e)) from e
        finally:
            _k32.CloseHandle(process)
        if server_sid != current_user_sid():
            raise WindowsHintingError("CLIENT_UNTRUSTED_SERVER", f"server runs as {server_sid}")

    class PipeTransport:
        def __init__(self, name: str, timeout_ms: int, verify: bool = True):
            self._handle = open_pipe(name, timeout_ms)
            try:
                if verify:
                    verify_server(self._handle)
            except Exception:
                self.close()
                raise

        def write(self, data: bytes) -> None:
            written = wintypes.DWORD()
            if not _k32.WriteFile(self._handle, data, len(data), ctypes.byref(written), None) \
                    or written.value != len(data):
                raise WindowsHintingError("CLIENT_IO", f"WriteFile: {ctypes.FormatError(ctypes.get_last_error())}")

        def read_line(self, deadline: float, max_bytes: int) -> bytes:
            # PeekNamedPipe polling keeps the handle synchronous while still honouring a deadline.
            data = bytearray()
            buf = ctypes.create_string_buffer(4096)
            avail = wintypes.DWORD()
            read = wintypes.DWORD()
            while b"\n" not in data:
                if not _k32.PeekNamedPipe(self._handle, None, 0, None, ctypes.byref(avail), None):
                    err = ctypes.get_last_error()
                    if err in (ERROR_BROKEN_PIPE, ERROR_PIPE_NOT_CONNECTED):
                        break
                    raise WindowsHintingError("CLIENT_IO", f"PeekNamedPipe: {ctypes.FormatError(err)}")
                if avail.value == 0:
                    if time.monotonic() >= deadline:
                        raise WindowsHintingError("CLIENT_TIMEOUT", "no response before timeout")
                    time.sleep(0.005)
                    continue
                if not _k32.ReadFile(self._handle, buf, min(avail.value, len(buf)), ctypes.byref(read), None):
                    raise WindowsHintingError("CLIENT_IO", f"ReadFile: {ctypes.FormatError(ctypes.get_last_error())}")
                data += buf.raw[: read.value]
                if len(data) > max_bytes:
                    raise WindowsHintingError("CLIENT_BAD_RESPONSE", "response too large")
            line, _, _ = bytes(data).partition(b"\n")
            if not line:
                raise WindowsHintingError("CLIENT_BAD_RESPONSE", "connection closed without a response")
            return line

        def close(self) -> None:
            if self._handle:
                _k32.CloseHandle(self._handle)
                self._handle = None

else:

    def current_user_sid() -> str:
        raise PipeNotFoundError("Windows-Hinting RPC is Windows-only")

    class PipeTransport:
        def __init__(self, name: str, timeout_ms: int, verify: bool = True):
            raise PipeNotFoundError("Windows-Hinting RPC is Windows-only")


# --- helpers shared with windows_hinting.py ---------------------------------------------

SELECT_ACTIONS = ("", "left", "right", "double", "move", "ctrl", "shift")

# Keystroke fallback for builds without RPC: the click-action shortcut keys
# (ClickActionShortcuts defaults in Windows-Hinting).
FALLBACK_ACTION_KEYS = {
    "left": "shift-l",
    "right": "shift-r",
    "double": "shift-d",
    "move": "shift-m",
    "ctrl": "shift-c",
    "shift": "shift-s",
}


def normalize_label(spoken: str) -> str:
    """'a b' (the user.hinting capture) -> 'AB'."""
    return "".join(spoken.split()).upper()
