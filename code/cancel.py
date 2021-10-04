# to disable command cancellation, comment out this entire file.
# you may also wish to adjust the commands in misc/cancel.talon.
from talon import speech_system, actions

# To change the phrase used to cancel commands, you must also adjust misc/cancel.talon
cancel_phrase = "cancel cancel".split()

def pre_phrase(d):
    n = len(cancel_phrase)
    if 'text' in d and 'parsed' in d:
        before, after = d["text"][:-n], d['text'][-n:]
        if after != cancel_phrase: return
        # cancel the command
        d["parsed"]._sequence = []
        actions.app.notify(f"Command canceled: {' '.join(before)!r}")

speech_system.register("pre:phrase", pre_phrase)
