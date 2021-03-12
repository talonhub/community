from talon import actions, speech_system


def fn(d):
    words = d["parsed"]._unmapped
    if words[0] == "keeper":
        actions.insert(" ".join(words[1:]))
        d["parsed"]._sequence = []


speech_system.register("pre:phrase", fn)
