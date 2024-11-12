from typing import Optional
from datetime import datetime
from talon import Module, actions, imgui, settings, speech_system, clip, app
import os

# We keep rejection_history_size lines of history, but by default display only
# rejection_history_display of them.
mod = Module()
mod.setting("rejection_history_size", type=int, default=50)
mod.setting("rejection_history_display", type=int, default=10)
mod.setting("rejection_path", 
    type=str, 
    default=os.path.expandvars("%AppData%\\talon\\recordings\\2024-11\\reject") if app.platform=="windows" else os.path.expanduser("~/.talon/recordings/2024-11/reject"), 
    desc="""rejection path"""
)

hist_more = False
history = []
history_no_timestamp = []
good_category_one = os.path.expanduser("~/Desktop/rejections/good category one")
good_category_two = os.path.expanduser("~/Desktop/rejections/good category two")

def on_phrase(j):
    global history, history_no_timestamp
    meta = j['_metadata']
    if meta['reject']:
        print(f"Rejected: {meta['emit']} {datetime.now()}")
        hypothesis = f"{meta['emit']}"

        history.append(f"{hypothesis} {datetime.now()}" if len (hypothesis) > 0 else f"Noise rejected {datetime.now()}")
        history_no_timestamp.append(f"{hypothesis}")
        history_no_timestamp = history_no_timestamp[-settings.get("user.rejection_history_size") :]
        history = history[-settings.get("user.rejection_history_size") :]


# todo: dynamic rect?
@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Rejection History")
    gui.line()
    text = (
        history[:]
        if hist_more
        else history[-settings.get("user.rejection_history_display") :]
    )
    for index, line in enumerate (text, 1):
        gui.text(f"{index}. {line}")

    gui.spacer()
    if gui.button("Rejection history close"):
        actions.user.rejection_history_disable()


speech_system.register("phrase", on_phrase)
def get_latest_reject():
    import glob
    import os
    import shutil
    path =os.path.join(settings.get("user.rejection_path"), "*") 
    print(path)
    list_of_files = glob.glob(path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getmtime)
    print(latest_file)
    return latest_file

@mod.action_class
class Actions:
    def rejection_history_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def rejection_history_enable():
        """Enables the history"""
        gui.show()

    def rejection_history_disable():
        """Disables the history"""
        gui.hide()

    def rejection_history_clear():
        """Clear the history"""
        global history
        history = []

    def rejection_history_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def rejection_history_less():
        """Show less history"""
        global hist_more
        hist_more = False

    def rejection_history_get(number: int) -> str:
        """returns the history entry at the specified index"""
        num = (0 - number) - 1
        return history[num]

    def rejection_history_transform_phrase_text(words: list[str]) -> Optional[str]:
        """Transforms phrase text for presentation in history. Return `None` to omit from history"""

        if not actions.speech.enabled():
            return None

        return " ".join(words) if words else None
    
    def rejection_copy_last():
        """placeholder"""
        clip.set_text(history_no_timestamp[-1])
    
    def rejection_move_last(category: int):
        """placeholder"""
        import shutil
        latest_reject = get_latest_reject()
        # I spoke and it was correctly rejected 
        if category==1:

            shutil.move(latest_reject, good_category_one)
            actions.app.notify(f"moved reject {latest_reject} to category one")
        # background speech that was correctly rejected
        else:
            shutil.move(latest_reject, good_category_two)
            actions.app.notify(f"moved reject {latest_reject} to category two")
    
    # def rejection_move(category: int):
    #     import glob
    #     import os
    #     import shutil

    #     list_of_files = glob.glob('/Users/knausj/.talon/recordings/2024-11/reject/*') # * means all if need specific format then *.csv
    #     latest_file = max(list_of_files, key=os.path.getmtime)
    #     print(latest_file)
    #     # I spoke and it was correctly rejected 
    #     if category==1:
    #         shutil.move(latest_file, '/Users/knausj/Desktop/rejections/good category one')
    #     else:
    #         shutil.move(latest_file, '/Users/knausj/Desktop/rejections/good category two')
        
            
        
