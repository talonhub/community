from talon import speech_system, actions
import logging

cancel_phrase = "cancel cancel".split()

def pre_phrase(d):
    logging.info(d)
    n = len(cancel_phrase)
    before, after = d["text"][:-n], d['text'][-n:]
    if after != cancel_phrase: return
    # cancel the command
    d["parsed"]._sequence = []
    actions.app.notify(f"Command canceled: {' '.join(before)!r}")

speech_system.register("pre:phrase", pre_phrase)
