app: windows_explorer
# The taskbar id; Control Panel windows (also CabinetWClass) are Microsoft.Windows.ControlPanel
and user.window_app_user_model_id: Microsoft.Windows.Explorer

app: windows_open_dialog
# Only dialogs hosting a shell folder view; see windows_open_dialog.py
and user.file_dialog: true
-
settings():
    user.context_sensitive_dictation = true
    user.paste_to_insert_threshold = 0

tag(): user.address
tag(): user.file_manager
tag(): user.navigation

^go <user.letter>$: user.file_manager_open_volume("{letter}:")
