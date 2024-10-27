from contextlib import suppress
from dataclasses import dataclass
from typing import Callable, Literal

from talon import Module, actions


@dataclass
class NavigationStep:
    direction: Literal["up", "right", "down", "left"]
    type: Literal["word", "character"]
    count: int


mod = Module()


@mod.capture(rule="[<number_small>] [word | words] {user.arrow_key}")
def navigation_step(m) -> NavigationStep:
    type = "character"
    count = 1

    with suppress(IndexError):
        if m[-2] in ["word", "words"]:
            type = "word"

    with suppress(AttributeError):
        count = m.number_small

    return NavigationStep(
        direction=m.arrow_key,
        type=type,
        count=count,
    )


@mod.action_class
class Actions:
    def perform_navigation_steps(steps: list[NavigationStep]):
        """Navigate by a series of steps"""
        for step in steps:
            match step.direction:
                case "up":
                    repeat_action(actions.edit.up, step.count)
                case "down":
                    repeat_action(actions.edit.down, step.count)
                case "left":
                    if step.type == "word":
                        repeat_action(actions.edit.word_left, step.count)
                    else:
                        repeat_action(actions.edit.left, step.count)
                case "right":
                    if step.type == "word":
                        repeat_action(actions.edit.word_right, step.count)
                    else:
                        repeat_action(actions.edit.right, step.count)


def repeat_action(action: Callable, count: int):
    for _ in range(count):
        action()
