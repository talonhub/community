# to disable command cancellation, comment out this entire file.
# you may also wish to adjust the commands in plugin/cancel/cancel.talon.
from talon import actions, speech_system

# To change the phrase used to cancel commands, you must also adjust plugin/cancel/cancel.talon
cancel_phrases = ["cancel cancel"]

# Alternatively, if you want to use a two-word phrase that
# can include homophones, you can use this code instead:
# cancel_words = ["cancel", "counsel", "council"]
# cancel_phrases = [
#     " ".join([word1, word2])
#     for word1 in cancel_words
#     for word2 in cancel_words
# ]


def pre_phrase(d):
    if "text" in d and "parsed" in d:
        text_str = " ".join(d["text"])
        for phrase in cancel_phrases:
            if text_str.endswith(phrase):
                # cancel the command
                d["parsed"]._sequence = []
                command_without_cancel_phrase = text_str[: -len(phrase)].strip()
                actions.app.notify(
                    f"Command canceled: {command_without_cancel_phrase!r}"
                )
                return


speech_system.register("pre:phrase", pre_phrase)
