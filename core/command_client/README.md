# Talon command client

This directory contains the client code for communicating with the [VSCode command server](https://marketplace.visualstudio.com/items?itemName=pokey.command-server).

## Hotkey conflicts

Common reason for the `Exception: Timed out waiting for response` error in the Talon log.

The command client sends key presses that the command server listens for as a signal to start processing the request. If you have another application or IDE extension using the same hotkey a conflict will occur. The command server will never process the request and the client will time out.

The hotkeys to look for are:

- [Windows/linux: `ctrl-shift-f17`](https://github.com/talonhub/community/blob/358d327b96891f628bd84728831a3fb544a27a15/core/command_client/command_client.py#L129)
- [Mac: `cmd-shift-f17`](https://github.com/talonhub/community/blob/358d327b96891f628bd84728831a3fb544a27a15/core/command_client/command_client.py#L148)
- [Vscode Linux: `ctrl-shift-alt-p`](https://github.com/talonhub/community/blob/358d327b96891f628bd84728831a3fb544a27a15/apps/vscode/vscode_command_client.py#L107)

## Contributing

The source of truth is in https://github.com/talonhub/community/tree/main/core/command_client, but the code is also maintained as a subtree at https://github.com/cursorless-dev/talon-command-client.

To contribute, first open a PR on `community`.

Once the PR is merged, you can push the changes to the subtree by running the following commands on an up-to-date `community` main: (need write access)

```sh
git subtree split --prefix=core/command_client --annotate="[split] " -b split
git push git@github.com:cursorless-dev/talon-command-client.git split:main
```
