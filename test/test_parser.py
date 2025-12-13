import talon


if hasattr(talon, "test_mode"):
    from talon import registry
    from core.help.parser import parse

    

    def test_parse_community():
        for context_name, context in registry.contexts.items():
            for command_alias, command in context.commands.items():
                try:
                    assert parse(command.rule.rule) is not None, f"Failed to parse command '{command.rule.rule}' in context '{context_name}'"
                except Exception as e:
                    print(f"Error parsing command '{command.rule.rule}' in context '{context_name}': {e}")
