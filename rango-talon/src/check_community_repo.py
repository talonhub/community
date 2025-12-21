from talon import app, registry

required_captures = [
    "number_small",
    "user.number_string",
    "user.letter",
    "user.text",
]

required_actions = [
    "user.paste",
]

required_lists = ["user.website"]


def on_ready():
    missing_captures = [
        capture for capture in required_captures if capture not in registry.captures
    ]
    missing_actions = [
        action for action in required_actions if action not in registry.actions
    ]
    missing_lists = [
        list_name for list_name in required_lists if list_name not in registry.lists
    ]
    errors = []
    if missing_captures:
        errors.append(f"Missing captures: {', '.join(missing_captures)}")
    if missing_actions:
        errors.append(f"Missing actions: {', '.join(missing_actions)}")
    if missing_lists:
        errors.append(f"Missing lists: {', '.join(missing_lists)}")
    if errors:
        print("\n".join(errors))
        app.notify(
            "Please install the community repository",
            body="https://github.com/talonhub/community",
        )


app.register("ready", on_ready)
