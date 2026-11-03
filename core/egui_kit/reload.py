"""Hot reload across several modules: build a tool's live instance only from fresh code.

When a file changes, Talon reloads it and then the modules that import it, but not in
dependency order. A module can be re-run before one of its own (also reloaded)
dependencies and keep the old class or function: e.g. the Talon surface re-runs, builds
the instance from the old Switcher class, and only then switcher.py reloads.

`when_fresh(prefixes, build, tag)` waits for the reloads to settle, checks every loaded
module under `prefixes` for names imported from a sibling that no longer match the
sibling's current ones, touches those modules' files (Talon reloads them, now on top of
fresh dependencies), checks again, and calls `build()` once nothing is stale. `build`
should look its classes up in sys.modules at call time, not use names bound when its
module was loaded.
"""

import os
import sys
import types

from talon import cron

# Attempts per tag before building anyway (a module that can't be refreshed).
MAX_ROUNDS = 4
_STASH = "_talon_egui_kit_reload"


def stale_modules(prefixes: tuple) -> list:
    """Loaded modules under `prefixes` holding a class, function or module from a
    sibling under `prefixes` that isn't the sibling's current one."""
    mods = {name: mod for name, mod in list(sys.modules.items()) if mod is not None and name.startswith(prefixes)}
    stale = []
    for name, mod in mods.items():
        for attr, value in list(vars(mod).items()):
            if attr.startswith("__"):
                continue
            if isinstance(value, types.ModuleType):
                if value.__name__ in mods and mods[value.__name__] is not value:
                    stale.append(mod)
                    break
                continue
            if not isinstance(value, (type, types.FunctionType)):
                continue
            owner = getattr(value, "__module__", None)
            if owner == name or owner not in mods:
                continue
            current = getattr(mods[owner], value.__name__, None)
            if current is not None and current is not value:
                stale.append(mod)
                break
    return stale


def touch(modules: list):
    """Make Talon reload these modules (it watches files' modification times)."""
    for mod in modules:
        path = getattr(mod, "__file__", None)
        if path and os.path.exists(path):
            os.utime(path, None)


def when_fresh(prefixes: tuple, build, tag: str, delay: str = "300ms"):
    """Call `build()` once the modules under `prefixes` are consistent (see the module
    docstring). Repeated calls for a tag (each reload re-runs the caller) keep only the
    latest."""
    state = getattr(sys, _STASH, None)
    if state is None:
        state = {}
        setattr(sys, _STASH, state)
    job = state.get(("job", tag))
    if job is not None:
        cron.cancel(job)

    def check():
        state.pop(("job", tag), None)
        stale = stale_modules(prefixes)
        rounds = state.get(("rounds", tag), 0)
        if stale and rounds < MAX_ROUNDS:
            state[("rounds", tag)] = rounds + 1
            print(f"{tag}: reloading {', '.join(m.__name__.rsplit('.', 1)[-1] for m in stale)} on fresh code")
            touch(stale)
            # Check again once they've reloaded (if they reload the caller too, its new
            # call replaces this one).
            state[("job", tag)] = cron.after("1500ms", check)
            return
        if stale:
            print(f"{tag}: still stale after {rounds} rounds: {[m.__name__ for m in stale]}; building anyway")
        state[("rounds", tag)] = 0
        build()

    state[("job", tag)] = cron.after(delay, check)
