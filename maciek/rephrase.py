from typing import Union
from talon import Module, actions, speech_system, cron
from talon.grammar import Phrase
import time

mod = Module()

phrase_stack = []


def on_pre_phrase(d):
    phrase_stack.append(d)


def on_post_phrase(d):
    phrase_stack.pop()


speech_system.register("pre:phrase", on_pre_phrase)
speech_system.register("post:phrase", on_post_phrase)

from typing import Union


def extract_samples(phrase):
    current_phrase = phrase_stack[-1]
    print("current_phrase", current_phrase)
    ts = current_phrase["_ts"]
    start = phrase.words[0].start - ts
    end = phrase.words[-1].end - ts
    samples = current_phrase["samples"]
    print(start, end)
    pstart = int(start * 16_000)
    pend = int(end * 16_000)
    samples = samples[pstart:pend]
    return samples


@mod.action_class
class Actions:
    def rephrase(phrase: Union[Phrase, str], run_async: bool = True):
        """Re-evaluate and run phrase"""
        if not phrase:
            return
        print("rephrase ", phrase)
        samples = extract_samples(phrase)

        if run_async:
            cron.after("0ms", lambda: speech_system._on_audio_frame(samples))
        else:
            speech_system._on_audio_frame(samples)

    # def polish_single_phrase(phrase: Union[Phrase, str] = None):
    #     """has to be here"""
    #     actions.mode.enable("user.polish_dictation")
    #     actions.mode.disable("command")
    #     samples = extract_samples(phrase)
    #     print("samples extracted")
    #     if phrase:

    #         def f():
    #             print("delayed function is running")
    #             speech_system._on_audio_frame(samples)

    #             actions.mode.disable("user.polish_dictation")
    #             actions.mode.enable("command")

    #         cron.after("4000ms", f)
