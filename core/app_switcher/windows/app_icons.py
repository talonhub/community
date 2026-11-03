"""App icons, found once and kept: the shared icon cache of the app switcher's tools.

An icon is named by its *source*: a shell parsing name, i.e. a file path (an .exe, an
.msc console, a shortcut, an image) or shell:AppsFolder\\<AppUserModelID>, at a size
(snapped up to 32, 64 or 128 pixels).

  * get(source, size, on_ready) never blocks: it returns the icon if it is cached, else
    None and queues a fetch; `on_ready(icon)` runs (on the fetch thread) when it lands.
    For drawing code: ask every frame, redraw when on_ready says so.
  * fetch(source, size) blocks until the icon is found (cached or fetched), for code
    already off the UI thread or that has always fetched synchronously.

Icons are kept in memory and on disk (%APPDATA%\\talon\\cache\\app_icons\\, a compressed
file per size), so a restart shows them at once. Apps rarely change their icons, but
updates can: an icon loaded from disk is fetched again in the background once per
session and replaced if it changed. Icons unused for PRUNE_DAYS are dropped.

One fetch thread feeds the COM thread one icon at a time, most recent requests first
(the rows on screen), so other COM work waits at most one icon (~20-30 ms). Its state
survives hot reloads (stashed on sys); a reloaded module's thread replaces the old one.
"""

import json
import os
import struct
import sys
import threading
import time
import zlib
from collections import OrderedDict

from talon import app

SIZES = (32, 64, 128)
PRUNE_DAYS = 60
# Seconds between finishing the queue and writing the disk cache.
SAVE_DELAY = 3.0
MAGIC = b"TALONICONS1"
_STASH = "_talon_app_icons_state"
# A cached miss: the shell has no icon for the source (fetching again won't help until
# the next session's revalidation).
_MISSING = object()


def apps_folder(app_id: str) -> str:
    """The icon source of an installed app, by its Apps folder id (AppUserModelID or
    the shell's generated id): what launch_applications.json calls unique_identifier."""
    return f"shell:AppsFolder\\{app_id}"


def snap(size: int) -> int:
    """The cache size for a wanted size: the smallest of SIZES at least as big."""
    return next((s for s in SIZES if s >= size), SIZES[-1])


def default_dir() -> str:
    return os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "talon", "cache", "app_icons")


class _State:
    """Everything that outlives a reload of this module."""

    # Bumped when the fields change, so a reload replaces an older state (the disk
    # cache keeps the icons).
    VERSION = 1

    def __init__(self):
        self.lock = threading.Lock()
        self.wake = threading.Condition(self.lock)
        # (source key, size, thumbnail) -> [icon or _MISSING, fetched_at, last_used, revalidated]
        self.icons: OrderedDict = OrderedDict()
        self.loaded_sizes: set[int] = set()
        self.dir = default_dir()
        self.dirty = False
        self.last_change = 0.0
        # Pending fetches, most recent last: key -> callbacks; revalidations separately.
        self.queue: OrderedDict = OrderedDict()
        self.revalidate: OrderedDict = OrderedDict()
        self.in_flight = None
        self.generation = 0
        self.worker: threading.Thread | None = None
        self.worker_generation = None
        self.stats = {"fetched": 0, "from_disk": 0, "hits": 0, "misses": 0, "revalidated": 0, "changed": 0}


def _state() -> _State:
    state = getattr(sys, _STASH, None)
    if state is None or getattr(state, "VERSION", 0) != _State.VERSION:
        if state is not None:
            with state.lock:
                state.generation += 1  # its thread stops
                state.wake.notify_all()
        state = _State()
        setattr(sys, _STASH, state)
    return state


def _key(source: str, size: int, thumbnail: bool) -> tuple:
    return (source.lower(), snap(size), bool(thumbnail))


# --- the public interface ---


def peek(source: str, size: int, thumbnail: bool = False):
    """The cached icon, or None (missing or not fetched yet); never queues a fetch."""
    if not source or app.platform != "windows":
        return None
    state = _state()
    key = _key(source, size, thumbnail)
    with state.lock:
        _load_disk(state, key[1])
        record = state.icons.get(key)
        if record is None:
            return None
        record[2] = time.time()
        return None if record[0] is _MISSING else record[0]


def get(source: str, size: int, on_ready=None, thumbnail: bool = False):
    """The icon if cached; else None, and a fetch is queued (most recent first) whose
    result goes to `on_ready(icon)` (called on the fetch thread, icon possibly None)."""
    if not source or app.platform != "windows":
        return None
    state = _state()
    key = _key(source, size, thumbnail)
    with state.lock:
        _load_disk(state, key[1])
        record = state.icons.get(key)
        if record is not None:
            state.stats["hits"] += 1
            record[2] = time.time()
            if not record[3] and key not in state.revalidate:
                # From disk and not checked this session: check it when the queue is idle.
                state.revalidate[key] = (source, on_ready)
                _ensure_worker(state)
                state.wake.notify()
            return None if record[0] is _MISSING else record[0]
        state.stats["misses"] += 1
        callbacks = state.queue.pop(key, None)
        if callbacks is None:
            callbacks = [source]
        if on_ready is not None and on_ready not in callbacks[1:]:
            callbacks.append(on_ready)
        # Re-inserted at the end: the newest requests are fetched first.
        state.queue[key] = callbacks
        _ensure_worker(state)
        state.wake.notify()
    return None


def fetch(source: str, size: int, thumbnail: bool = False):
    """The icon, fetched now if it isn't cached (blocks for a shell lookup)."""
    if not source or app.platform != "windows":
        return None
    state = _state()
    key = _key(source, size, thumbnail)
    with state.lock:
        _load_disk(state, key[1])
        record = state.icons.get(key)
        if record is not None:
            state.stats["hits"] += 1
            record[2] = time.time()
            return None if record[0] is _MISSING else record[0]
    icon = _shell_fetch(source, key[1], thumbnail)
    with state.lock:
        _store(state, key, icon, revalidated=True)
        _ensure_worker(state)  # for the delayed save
        state.wake.notify()
    return icon


def cancel(on_ready):
    """Forget queued fetches that only `on_ready` wanted (e.g. a closed window's)."""
    state = _state()
    with state.lock:
        for key in [k for k, cbs in state.queue.items() if on_ready in cbs[1:]]:
            callbacks = state.queue[key]
            callbacks.remove(on_ready)
            if len(callbacks) == 1:
                del state.queue[key]


def stats() -> dict:
    state = _state()
    with state.lock:
        return dict(state.stats, cached=len(state.icons), queued=len(state.queue), revalidating=len(state.revalidate), dir=state.dir)


def set_cache_dir(path: str, clear_memory: bool = True):
    """Use another disk cache directory (tests); optionally forget what's in memory."""
    state = _state()
    with state.lock:
        if state.dirty:
            _save(state)
        state.dir = path
        if clear_memory:
            state.icons.clear()
            state.loaded_sizes.clear()
            state.queue.clear()
            state.revalidate.clear()


def save_now():
    state = _state()
    with state.lock:
        if state.dirty:
            _save(state)


# --- fetching ---


def _shell_fetch(source: str, size: int, thumbnail: bool):
    from .shell_icons import shell_pixels

    try:
        return shell_pixels(source, size, thumbnail=thumbnail)
    except Exception as e:
        print(f"app_icons: {source!r} at {size}: {e!r}")
        return None


def _store(state: _State, key: tuple, icon, revalidated: bool):
    """Record a fetched icon (lock held). Returns whether it changed."""
    now = time.time()
    record = state.icons.get(key)
    value = icon if icon is not None else _MISSING
    changed = record is None or _pixels(record[0]) != _pixels(value)
    if record is None:
        state.icons[key] = [value, now, now, revalidated]
    else:
        if changed:
            record[0] = value
            record[1] = now
        record[3] = record[3] or revalidated
    if changed:
        state.dirty = True
        state.last_change = now
    return changed


def _pixels(value):
    return None if value is _MISSING else (value.width, value.height, value.rgba)


def _ensure_worker(state: _State):
    """Start this module's fetch thread if it isn't running (lock held)."""
    if state.worker is not None and state.worker.is_alive() and state.worker_generation == _GENERATION:
        return
    state.generation += 1
    state.worker_generation = _GENERATION
    generation = state.generation
    state.worker = threading.Thread(target=_run, args=(state, generation), name="app icons", daemon=True)
    state.worker.start()


def _run(state: _State, generation: int):
    while True:
        with state.lock:
            while True:
                if state.generation != generation:
                    return  # replaced (a reload)
                if state.queue:
                    key, callbacks = state.queue.popitem(last=True)
                    source, callbacks = callbacks[0], callbacks[1:]
                    revalidating = False
                    break
                if state.revalidate:
                    key, (source, callback) = state.revalidate.popitem(last=True)
                    callbacks = [callback] if callback is not None else []
                    revalidating = True
                    break
                if state.dirty and time.time() - state.last_change >= SAVE_DELAY:
                    snapshot = _snapshot(state)
                    state.lock.release()
                    try:
                        _write(snapshot)
                    finally:
                        state.lock.acquire()
                    continue
                state.wake.wait(SAVE_DELAY if state.dirty else 30.0)
            state.in_flight = key
        icon = _shell_fetch(source, key[1], key[2])
        with state.lock:
            state.in_flight = None
            changed = _store(state, key, icon, revalidated=True)
            state.stats["revalidated" if revalidating else "fetched"] += 1
            if revalidating and changed:
                state.stats["changed"] += 1
            notify = [cb for cb in callbacks if cb is not None] if (changed or not revalidating) else []
        for callback in notify:
            try:
                callback(icon)
            except Exception as e:
                print(f"app_icons: callback for {source!r} failed: {e!r}")


# --- the disk cache: one file per size ---
#
# MAGIC, then a zlib stream of: a 4-byte length, a JSON index
# [[source, thumbnail, width, height, fetched_at, last_used, offset, length], ...]
# (width 0 for a cached miss), then the RGBA pixels back to back.


def _path(state: _State, size: int) -> str:
    return os.path.join(state.dir, f"icons_{size}.bin")


def _load_disk(state: _State, size: int):
    """Load a size's file into memory the first time it's needed (lock held)."""
    if size in state.loaded_sizes:
        return
    state.loaded_sizes.add(size)
    try:
        with open(_path(state, size), "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        return
    except OSError as e:
        print(f"app_icons: reading the {size}px cache: {e!r}")
        return
    try:
        if not raw.startswith(MAGIC):
            raise ValueError("not an icon cache")
        data = zlib.decompress(raw[len(MAGIC):])
        (n,) = struct.unpack_from("<I", data, 0)
        index = json.loads(data[4 : 4 + n])
        blobs = memoryview(data)[4 + n :]
    except Exception as e:
        print(f"app_icons: the {size}px cache is unreadable, ignoring it: {e!r}")
        return
    from .shell_icons import Icon

    cutoff = time.time() - PRUNE_DAYS * 86400
    for source, thumbnail, width, height, fetched_at, last_used, offset, length in index:
        key = (source, size, bool(thumbnail))
        if key in state.icons or last_used < cutoff:
            continue
        value = Icon(width, height, bytes(blobs[offset : offset + length])) if width else _MISSING
        state.icons[key] = [value, fetched_at, last_used, False]
        state.stats["from_disk"] += 1


def _snapshot(state: _State) -> list:
    """What to write, per size (lock held); drops long-unused icons and clears `dirty`."""
    cutoff = time.time() - PRUNE_DAYS * 86400
    files = []
    for size in sorted(state.loaded_sizes | {k[1] for k in state.icons}):
        index, blobs, offset = [], [], 0
        for (source, s, thumbnail), (value, fetched_at, last_used, _rev) in list(state.icons.items()):
            if s != size:
                continue
            if last_used < cutoff:
                del state.icons[(source, s, thumbnail)]
                continue
            if value is _MISSING:
                index.append([source, thumbnail, 0, 0, fetched_at, last_used, offset, 0])
                continue
            index.append([source, thumbnail, value.width, value.height, fetched_at, last_used, offset, len(value.rgba)])
            blobs.append(value.rgba)
            offset += len(value.rgba)
        files.append((state.dir, _path(state, size), index, blobs))
    state.dirty = False
    return files


def _write(files: list):
    """Write a snapshot's files (no lock needed): compressed, replaced atomically."""
    for directory, path, index, blobs in files:
        try:
            os.makedirs(directory, exist_ok=True)
            header = json.dumps(index).encode("utf-8")
            payload = struct.pack("<I", len(header)) + header + b"".join(blobs)
            tmp = path + ".tmp"
            with open(tmp, "wb") as f:
                f.write(MAGIC + zlib.compress(payload, 6))
            os.replace(tmp, path)
        except OSError as e:
            print(f"app_icons: writing {path}: {e!r}")


def _save(state: _State):
    """Write the cache now (lock held; for tests and switching directories)."""
    _write(_snapshot(state))


# Each load of this module is a new generation; the stashed state's thread from an
# older load stops and a new one starts on the next request.
_GENERATION = object()
