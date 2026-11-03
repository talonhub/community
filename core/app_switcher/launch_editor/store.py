"""The editor's model: launch_applications.json loaded, edited and saved (autosave;
changes made elsewhere load in), the filters and their counts, and spoken forms:
Talon's live ones, clashes between apps, adding new ones."""

import json
import os
import time
from collections import Counter
from talon import cron, registry


NO_EXE = "(no executable)"


FILTERS = [
    ("all", "All"),
    ("enabled", "Enabled"),
    ("disabled", "Disabled"),
    ("forms", "Custom Spoken Form"),
]


def snapshot(entry: dict) -> tuple:
    forms = entry.get("spoken_forms")
    return (bool(entry.get("exclude")), tuple(forms) if forms else None)


class StoreMixin:
    """Editor methods: see the module docstring. Mixed into Editor, whose state they use."""

    def load(self):
        try:
            with open(self.path, "r") as f:
                entries = json.load(f)
            mtime = os.path.getmtime(self.path)
        except Exception as e:
            with self.lock:
                self.message = f"Couldn't read the file: {e}"
            return
        with self.lock:
            self.entries = entries
            self.identifiers = {(e.get("unique_identifier") or "").lower() for e in entries} - {""}
            self.baseline = {i: snapshot(e) for i, e in enumerate(entries)}
            self.mtime = mtime
            self.message = ""
            if self.selected is None or self.selected >= len(entries):
                self.selected = 0 if entries else None
        self.refresh_launch_map()
        print(f"launch_applications_editor: loaded {len(entries)} entries")
        self.window.refresh()

    def save(self):
        with self.lock:
            try:
                if os.path.getmtime(self.path) != self.mtime:
                    # Changed elsewhere since it was loaded; take that version.
                    self.message = "The file changed elsewhere; reloaded it. Redo your last change."
                    cron.after("0ms", self._reload_keep_message)
                    return
                text = json.dumps(self.entries, indent=4)
                tmp = self.path + ".tmp"
                with open(tmp, "w") as f:
                    f.write(text)
                os.replace(tmp, self.path)
                self.mtime = os.path.getmtime(self.path)
                self.baseline = {i: snapshot(e) for i, e in enumerate(self.entries)}
                self.saved_at = time.time()
                # app_switcher rebuilds user.launch from the saved file; read it after.
                cron.after("2s", self.refresh_launch_map)
                self.message = ""
            except Exception as e:
                self.message = f"Couldn't save: {e}"
        print("launch_applications_editor: saved" if not self.message else f"launch_applications_editor: {self.message}")
        self.window.refresh()

    def _reload_keep_message(self):
        message = self.message
        self.load()
        self.message = message

    def autosave(self):
        self.save_job = None
        self.save()

    def poll(self):
        """Load the file again when something else changed it."""
        if not self.showing or self.save_job is not None:
            return
        try:
            mtime = os.path.getmtime(self.path)
        except OSError:
            return
        if mtime != self.mtime and not self.unsaved():
            print("launch_applications_editor: file changed elsewhere, reloading")
            self.load()

    def unsaved(self) -> int:
        return sum(1 for i, e in enumerate(self.entries) if snapshot(e) != self.baseline.get(i))

    def show_test(self, key: str, i: int, e: dict) -> bool:
        if key == "enabled":
            return not e.get("exclude")
        if key == "disabled":
            return bool(e.get("exclude"))
        if key == "forms":
            return bool(e.get("spoken_forms"))
        return True

    def exe_test(self, exe: str | None, e: dict) -> bool:
        return exe is None or (e.get("executable_name") or NO_EXE) == exe

    def query_test(self, query: str, e: dict) -> bool:
        if not query:
            return True
        uid = (e.get("unique_identifier") or "").lower()
        if query in self.identifiers:
            # An identifier (as "Edit launch entry" searches) names exactly one app.
            return uid == query
        hay = " ".join(
            [e.get("display_name") or "", e.get("executable_name") or "", uid, *(e.get("spoken_forms") or [])]
        ).lower()
        return query in hay

    def matches(self, i: int, e: dict, query: str) -> bool:
        return self.show_test(self.filter, i, e) and self.exe_test(self.exe_filter, e) and self.query_test(query, e)

    def counts(self, query: str) -> dict[str, int]:
        scoped = [(i, e) for i, e in enumerate(self.entries) if self.exe_test(self.exe_filter, e) and self.query_test(query, e)]
        return {key: sum(1 for i, e in scoped if self.show_test(key, i, e)) for key, _ in FILTERS}

    def exe_counts(self, query: str) -> list[tuple[str, int]]:
        """Executables with more than one entry in the file (a stable list), each with
        how many entries it would show given the Show filter and search."""
        everywhere = Counter(e.get("executable_name") or NO_EXE for e in self.entries)
        scoped = Counter(
            e.get("executable_name") or NO_EXE
            for i, e in enumerate(self.entries)
            if self.show_test(self.filter, i, e) and self.query_test(query, e)
        )
        return [(exe, scoped.get(exe, 0)) for exe, n in everywhere.most_common() if n >= 2]

    def refresh_launch_map(self):
        try:
            merged = {}
            for mapping in registry.lists.get("user.launch", []):
                merged.update(mapping)
        except Exception as e:
            print(f"launch_applications_editor: couldn't read user.launch: {e!r}")
            return
        auto: dict[str, list[str]] = {}
        for form, uid in merged.items():
            auto.setdefault(str(uid).lower(), []).append(str(form))
        with self.lock:
            self.launch_map = {str(k).lower(): str(v) for k, v in merged.items()}
            self.auto_forms = {uid: sorted(forms, key=lambda f: (len(f), f)) for uid, forms in auto.items()}
        print(f"launch_applications_editor: user.launch has {len(merged)} spoken forms for {len(auto)} apps")
        self.window.refresh()

    def live_forms(self, e: dict) -> list[str]:
        """What Talon answers to for this entry right now (from user.launch)."""
        return self.auto_forms.get((e.get("unique_identifier") or "").lower(), [])

    def form_owner(self, form: str, e: dict) -> str | None:
        """Which other entry already answers to `form`, as a label, or None.

        Stored spoken forms are checked in the editor's current (possibly just edited)
        entries of enabled apps. Forms generated
        from display names come from the live user.launch list, skipping apps that
        now have custom forms (those replace the generated ones) or are disabled."""
        for other in self.entries:
            # Disabled apps' spoken forms aren't registered, so they don't clash.
            if other is not e and not other.get("exclude") and form in (other.get("spoken_forms") or []):
                return other.get("display_name") or "?"
        uid = self.launch_map.get(form)
        mine = (e.get("unique_identifier") or "").lower()
        if uid is None or uid.lower() == mine:
            return None
        for other in self.entries:
            if (other.get("unique_identifier") or "").lower() == uid.lower():
                if other.get("spoken_forms") or other.get("exclude"):
                    return None
                return other.get("display_name") or uid
        return uid

    def add_form(self, e: dict):
        """Add the field's spoken forms; several can be entered at once, comma-separated.

        Forms that clash with another app, or that can't be spoken (digits, symbols),
        are left in the field with a note saying why."""
        new = [" ".join(part.split()).lower() for part in self.new_form.get().split(",")]
        new = [form for form in new if form]
        if not new:
            return
        forms = list(e.get("spoken_forms") or [])
        rejected, notes = [], []
        for form in dict.fromkeys(new):
            if form in forms:
                continue
            if not all(ch.isalpha() or ch in " '-" for ch in form):
                rejected.append(form)
                notes.append(f"“{form}” has digits or symbols; spoken forms must be words.")
                continue
            owner = self.form_owner(form, e)
            if owner:
                rejected.append(form)
                notes.append(f"“{form}” is already used by {owner}.")
                continue
            forms.append(form)
        if len(forms) != len(e.get("spoken_forms") or []):
            e["spoken_forms"] = forms
        self.new_form.set(", ".join(rejected))
        self.form_notice = " ".join(notes)
