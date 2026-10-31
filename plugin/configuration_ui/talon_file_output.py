from .talon_file_parsing import VALUE_UNAVAILABLE, SettingsParser


def _convert_value_to_talon_script_literal(value, indentation) -> str:
    """Convert the Python value to TalonScript"""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        value = value.replace("\\", "\\\\").replace('"', '\\"')
        if "\n" in value:
            # this preserves a trailing new line whereas split lines does not
            lines = value.split("\n")
            indented_lines = "\n".join([f"{indentation}{l}" for l in lines])
            return f'"""\n{indented_lines}"""'
        return f'"{value}"'
    raise ValueError(f"Could not convert value {value} to Talonscript")


def update_setting(setting, new_value=VALUE_UNAVAILABLE, make_comment=False):
    """Update the setting with the new value and comment status. If not given a new value, use the current one"""
    name = setting.name
    path = setting.path
    value = setting.value.get() if new_value == VALUE_UNAVAILABLE else new_value

    parser = SettingsParser(path)
    if name in parser.duplicate_settings:
        raise OSError(
            f"Found duplicate setting assignment for {name} inside file {path}"
        )
    if name not in parser.settings:
        raise OSError(f"Could not find {name} inside file {path}")

    info = parser.settings[name]
    assignment_prefix = info.assignment_prefix
    # the prefix can include #'s, but we only want to add those if we are intentionally making this a comment
    # the logic was done this way to to avoid depending on knowing exactly what the prefix is
    if not assignment_prefix.isspace():
        num_leading_spaces = len(assignment_prefix) - len(assignment_prefix.lstrip())
        assignment_prefix = assignment_prefix[:num_leading_spaces]
    if make_comment:
        assignment_prefix += "# "
    converted_value = _convert_value_to_talon_script_literal(value, assignment_prefix)
    new_setting_text = f"{assignment_prefix}{name} = {converted_value}"

    lines = parser.lines
    lines[info.start_line_index : info.line_after_index] = [new_setting_text]

    path.write_text("\n".join(lines), encoding="utf-8")


def update_tag(tag, should_be_active):
    """Update the status of the tag"""
    name = tag.name
    path = tag.path
    parser = SettingsParser(path)
    if name in parser.duplicate_tags:
        raise OSError(
            f"Found duplicate tag activation for tag {name} in the file {path}!"
        )
    if name in parser.tags and parser.tags[name].value == should_be_active:
        return

    lines = parser.lines
    prefix = "" if should_be_active else "# "
    new_string = f"{prefix}tag(): {name}"

    if name in parser.tags:
        info = parser.tags[name]
        lines[info.start_line_index] = new_string
    else:
        lines.append("\n")
        lines.append(new_string)

    path.write_text("\n".join(lines), encoding="utf-8")
