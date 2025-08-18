# This file provides support for defining functions that have an associated description
# Talon's version of python does not allow getting the code of a function through reflection, so we are instead allowing associating doc strings with lambdas and functions as a way to apply descriptions to the community help system


from typing import Callable

from talon import actions


def create_described_function(function: Callable, description: str) -> Callable:
    """Creates a function with an associated doc string. Primarily intended to be used with lambdas"""
    function.__doc__ = description
    return function


def described_function_create_insert_between(before: str, after: str) -> Callable:
    """Creates a described function for calling actions.user.insert_between"""
    return create_described_function(
        lambda: actions.user.insert_between(before, after),
        f"actions.user.insert_between('{before}', '{after}')",
    )
