# Test plan: shared window/app identity for app_switcher and the thumbnail switcher

Covers the refactor that moves shared Windows logic into `core/app_switcher/windows/`:

| Module | Contents | Used by |
|--------|----------|---------|
| `com_thread.py` | The single COM (STA) thread; moved from `thumbnails/` | both |
| `virtual_desktops.py` | Virtual desktop COM; moved from `thumbnails/` (the window filter needs it) | both |
| `window_filter.py` | Alt+Tab rule (styles + DWM cloak state, other desktops allowed) | both (replaces `is_window_valid`'s size heuristic) |
| `shell_com.py` | GUID / PROPERTYKEY / PROPVARIANT, vtable calls, shell item names and properties, shortcut targets | both |
| `shell_apps.py` | One cached scan of shell:AppsFolder and the Start-menu shortcuts, on the COM thread | launch list, name lookups |
| `app_identity.py` | `resolve(hwnd)`: the taskbar's name and grouping key for a window (cached) | both |

Everything runs in Talon through the REPL (`repl.bat`), with throwaway windows only. No
voice commands; actions are called directly. Talon isn't restarted or woken.

## 0. Baseline (before any change)

Saved to the scratchpad `baseline/` folder:
- `user.running` and `user.launch` contents, `INSTALLED_APPLICATIONS_LIST`
- the switcher's name, grouping key and icon hash for every open window
- `apps_folder_names()` and `shortcut_names_by_id()` (the switcher's indexes)
- taskbar button labels (UI Automation on `Shell_TrayWnd`)
- `update_running_list()` timing

## 1. After every step

- **T1.1** Files reload without errors in talon.log (`[~]` lines, no Traceback).
- **T1.2** No COM on Talon threads: every COM entry point is decorated `@on_com_thread`, or
  only reached from one; checked with a grep for `CoCreateInstance` / `SHCreateItem` /
  `SHGetPropertyStoreForWindow` outside COM-thread functions. Talon doesn't crash.
- **T1.3** Smoke: the switcher opens (all windows, apps strip) and the running list rebuilds.

## 2. Thumbnail switcher

- **T2.1** Same name, key and icon as the baseline for every open window (differences
  must be intended fixes).
- **T2.2** Index equality: `apps_folder_names()` and `shortcut_names_by_id()` equal the
  baseline.
- **T2.3** AppsFolder sweep: switcher name vs the taskbar for cheap, safe apps that are
  opened and closed again: Notepad, Paint, Calculator, Command Prompt (conhost), Git Bash,
  IDLE (if installed), Snipping Tool, MMC Services and Event Viewer. Earlier 51-app
  results are the reference.
- **T2.4** PWAs (Slack, Gmail) named and iconed as on the taskbar if running (not
  launched by the test).
- **T2.5** Regression: grid/list/apps strip open; `app:`, `desk:`, `screen:` filters;
  `window thumbs <app>` (`thumbnail_switcher_show_application`) including community's
  MMC entries; marks; per-item and header close buttons (on throwaway windows).

## 3. app_switcher

- **T3.1** `user.running` vs the taskbar: every running taskbar button has a spoken form;
  minimized apps are present; cloaked hosts (TextInputHost, SearchHost, Shell Experience
  Host, suspended Calculator) are absent; File Explorer is present.
- **T3.2** Focus via the action `user.switcher_focus(<value>)` for: a normal app, File
  Explorer, Paint, Command Prompt, Git Bash, IDLE (if installed), each MMC console
  separately, Calculator (UWP), a PWA if running. Focus is verified with
  `ui.active_window()`. Only throwaway windows are focused, apart from Explorer/VS Code,
  which are only focused (never changed).
- **T3.3** json overrides honoured: VS Code is reachable as "coder" (its spoken-form
  override); an Application with only a `display_name` override uses it.
- **T3.4** Launch list unchanged: `INSTALLED_APPLICATIONS_LIST` and `user.launch` equal
  the baseline.
- **T3.5** `get_running_app(name)` still answers for app names, exe names and AUMIDs
  (used by `switcher_launch` to focus instead of relaunching).
- **T3.6** Exclusions file guard: reloading with no `running_applications_exclusions.csv`
  logs no error; with an exclusion file containing `EXE=notepad.exe` (temporary),
  Notepad is excluded; file removed again.

## 4. Performance

- **T4.1** `update_running_list()` with about 15 windows: under 200 ms warm (cached
  identities), under 1 s cold.
- **T4.2** No `[watchdog] "ui_event"` warnings in talon.log during the test run.

## Pass criteria

All of the above pass, or any difference from the baseline is an intended fix and is
listed in `TEST_RESULTS.md`.

## Round 4 — focus by app identity (PWAs sharing a host exe), 2026-11-02

Change under test: "focus <app>" resolves by app identity (AppUserModelID, as the
taskbar groups), never by process; the running list refreshes on window events
(debounced); apps with no open windows are launched; "focus" also accepts
launch-list names (running entries win).

Rules: throwaway windows only; Jeff's real windows are inspected read-only. The
Edge cases use a throwaway Edge profile (--user-data-dir in %TEMP%), so its
processes are separate from Jeff's Edge.

| # | Case | Expected |
|---|------|----------|
| F1 | Throwaway profile: browser window + `--app=` window open | running list has both entries, each with its own windows |
| F2 | Close the throwaway browser window (app window stays, same msedge process) | its entry leaves the running list within ~0.5 s |
| F3 | "focus <app window>" with the browser closed | focuses the app window, not anything else |
| F4 | "focus edge"-style lookup when no browser window of that identity exists | launches (no process-level focus of the host) |
| F5 | Both open: focus each | each focuses its own window |
| F6 | Jeff's Gmail / Slack PWAs and Edge (read-only) | separate running entries; identity keys distinct; name map points at windows, not the msedge process |
| F7 | MMC consoles (Services, Event Viewer) | separate entries, each focuses its own console |
| F8 | rundll32/dllhost applet | own entry; focus works |
| F9 | Packaged app (Calculator) | focus works; when not running, "focus calculator" launches it |
| F10 | Win32 app (Notepad, throwaway) and console windows (cmd) | focus works |
| F11 | File Explorer window | focus works |
| F12 | Stale entry: window closed while its process keeps running | no focus of an unrelated window of that process |
| F13 | Grammar: a name in both running and launch lists | running wins (focuses, doesn't launch) |
| F14 | Performance: time rebuilds; talon.log has no watchdog stalls from the refresh | rebuild well under 100 ms typical; no stalls |
| F15 | Thumbnail switcher unaffected (window / app / launcher views open, focus by number) | unchanged |
