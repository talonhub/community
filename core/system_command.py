import os
import subprocess

from talon import Module, system

mod = Module()


def split_command(cmd: str):
    """
    Splits the given command string into its component parts in a way similar
    to the unix shell, but more forgiving of Window's filesystem paths. Supports
    single/doubly quoted strings and escaping a double quote within a string using
    a backslash (like "I said \"hi\"")
    e.g.
        "~/my-script.sh args \"with quotes\"" ->
        ("ok", [
            ("~/my-script.sh", "simple"),
            ("args", "simple"),
            ("with quotes", "quoted"),
        ])

        "WScript C:\\Users\\Administrator\\test.vbs" ->
        ("ok", [
            ("WScript", "simple"),
            ("C:\\Users\\Administrator\\test.vbs", "simple"),
        ])
    """

    quote_chars = ('"', "'")
    terminal_chars = (" ", None)

    state = "start"
    result_type = None
    quote_char = None
    quote_pos = None
    buffer = ""
    rtn = []

    for i, c in enumerate(list(cmd) + [None]):
        if state == "start":
            if c in quote_chars:
                state = "quoted"
                result_type = "quoted"
                quote_char = c
                quote_pos = i + 1
            elif c in terminal_chars:
                continue
            elif c == "\\":
                state = "esc_simple"
                result_type = "simple"
            else:
                state = "simple"
                result_type = "simple"
                buffer += c
        elif state == "simple":
            if c in terminal_chars:
                rtn.append((buffer, result_type))
                state = "start"
                result_type = None
                quote_char = None
                quote_pos = None
                buffer = ""
            elif c in quote_chars:
                state = "quoted"
                result_type = "quoted"
                quote_char = c
                quote_pos = i + 1
            elif c == "\\":
                state = "esc_simple"
            else:
                buffer += c
        elif state == "quoted":
            if c is None:
                return ("error", f"Unclosed quote at character {quote_pos}")

            if c == quote_char:
                state = "simple"
            elif c == "\\":
                if quote_char == '"':
                    state = "esc_quoted"
                else:
                    buffer += c
            else:
                buffer += c
        elif state == "esc_quoted":
            if c is None:
                return ("error", f"Unclosed quote at character {quote_pos}")

            if c == quote_char:
                buffer += c
            else:
                buffer += "\\"
                buffer += c

            state = "quoted"
        elif state == "esc_simple":
            if c in quote_chars:
                buffer += c
            elif c is None:
                # End of input with trailing slash
                buffer += "\\"
                rtn.append((buffer, result_type))
            else:
                buffer += "\\"
                buffer += c

            state = "simple"

    return ("ok", rtn)


def process_command(cmd: str):
    success, result = split_command(cmd)

    if success == "error":
        raise RuntimeError(result)

    if len(result) == 0:
        raise RuntimeError("Empty command string")

    return [
        os.path.expanduser(piece) if result_type == "simple" else piece
        for piece, result_type in result
    ]


@mod.action_class
class Actions:
    def system_command(cmd: str) -> None:
        """Run a command and wait for it to finish"""
        args = process_command(cmd)
        subprocess.run(args, check=True)

    def system_command_nb(cmd: str) -> None:
        """Run a command without waiting for it to finish"""
        args = process_command(cmd)
        cmd, args = args[0], args[1:]
        system.launch(path=cmd, args=args)
