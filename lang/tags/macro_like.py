import csv

from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag(
    "code_macro_like",
    desc="Enables macro-like language functionality",
)

mod.list(
    "code_macro_like",
    desc="""
A list binding macro-like definition strings to their spoken forms, eg. `"spoken form": "macroName,(,)"`.
A macro-like definition string is defined as one or three values in the format `MACRO_LIKE_NAME,LEFT_DELIMITER,RIGHT_DELIMITER`,
    where both `LEFT_DELIMITER` and `RIGHT_DELIMITER` are optional, but must both be defined simultaneously.
See the documentation on module action `code_insert_macro_like` for more info.
""",
)

ctx.matches = r"""
tag: user.code_macro_like
"""


def do_macro_like_insert(text: str, selection: str, left_delim: str, right_delim: str):
    if selection:
        out_text = f"{text}{left_delim}{selection}{right_delim}"
    actions.user.paste(out_text)
    actions.edit.left()


@mod.capture(rule="{user.code_macro_like}")
def code_macro_like(m) -> str:
    return m.code_macro_like


@mod.action_class
class Actions:
    def code_insert_macro_like(text: str, selection: str):
        """
        Inserts a macro-like derived from the value portion of a spoken form-value pair in the capture <user.code_macro_like>.
        This is achieved by parsing the value into a name and two delimiters, or into either a basic form macro-like or a snippet insertion.
            The spoken form-value pair `"example macro": "example_macro"` either resolves to a snippet insertion
            if `example_macro` exactly matches a snippet name, or to a basic (one-to-one) insertion otherwise.

            The spoken form-value `"other example macro": "other_example,<,>"` resolves to an insertion of `other_example<>`
            with the cursor positioned between the two delimiters (`<` and `>`) if selection is nil or empty, or with
            the delimiters wrapping selection if selection has a coherent value.
        Raises an exception of type `ValueError` when passed an empty value for text, or if passed a value for text which only contains one delimiter.
        Issues a warning via actions.app.notify if passed a value for text which contains more than two delimiters
        """
        text_reader = csv.reader([text], doublequote=True, escapechar="\\")
        values = next(text_reader)
        if len(values) == 0:
            raise ValueError("Missing macro-like definition for given spoken form")
        if len(values) == 1:
            # no delimiters defined
            if values[0] in actions.users.get_snippet_names():
                actions.user.insert_snippet_by_name(values[0])
            else:
                # macro uses a basic insertion
                actions.user.paste(values[0])
        elif len(values) == 2:
            # missing right delimiter
            raise ValueError(
                f"Macro-like {values[0]} has left delimiter {values[1]} but no right delimiter"
            )
        else:
            if len(values) > 3:
                actions.app.notify(
                    f"Macro-like {values[0]} has more than two defined delimiters, ignoring extraneous values...",
                    "Macro-Like warning",
                )
        do_macro_like_insert(values[0], selection, values[1], values[2])
