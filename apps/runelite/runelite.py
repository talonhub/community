from talon import Module, cron, ctrl, actions

mod = Module()
hold_jobs = {}  # Dictionary to track cron jobs for each key

@mod.action_class
class Actions:
    def toggle_key_repeater(key_name: str):
        """Toggles holding down a specified key."""
        if key_name in hold_jobs:
            actions.user.stop_key_repeater(key_name)
        else:
            actions.user.start_key_repeater(key_name)

    def start_key_repeater(key_name: str):
        """Holds down the specified key with a repeating signal."""
        global hold_jobs
        if key_name not in hold_jobs:
            ctrl.key_press(key_name, down=True)  # Initial hold down
            hold_jobs[key_name] = cron.interval("10ms", lambda: ctrl.key_press(key_name))

    def stop_key_repeater(key_name: str):
        """Stops holding down the specified key, releasing it."""
        global hold_jobs
        job = hold_jobs.pop(key_name, None)
        if job:
            cron.cancel(job)
            ctrl.key_press(key_name, up=True)  # Release the key
