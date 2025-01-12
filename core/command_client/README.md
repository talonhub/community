# Talon command client

This directory contains the client code for communicating with the [VSCode command server](https://marketplace.visualstudio.com/items?itemName=pokey.command-server).

## Contributing

The source of truth is in https://github.com/talonhub/community/tree/main/core/command_client, but the code is also maintained as a subtree at https://github.com/cursorless-dev/talon-command-client.

To contribute, first open a PR on `community`.

Once the PR is merged, you can push the changes to the subtree by running the following commands on an up-to-date `community` main: (need write access)

```sh
git subtree split --prefix=core/command_client --annotate="[split] " -b split
git push git@github.com:cursorless-dev/talon-command-client.git split:main
```
