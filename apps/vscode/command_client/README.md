# Talon VSCode command client

This directory contains the client code for communicating with the [VSCode command server](https://marketplace.visualstudio.com/items?itemName=pokey.command-server).

## Contributing

The source of truth is in https://github.com/talonhub/community/tree/main/apps/vscode/command_client, but the code is also maintained as a subtree at https://github.com/pokey/talon-vscode-command-client.

To contribute, first open a PR on `community`.

Once the PR is merged, you can push the changes to the subtree by running the following commands on an up-to-date `community` main: (need write access)

```sh
git subtree split --prefix=apps/vscode/command_client --annotate="[split] " -b split
git push talon-vscode-command-client split:master
```

Note that you'll need to have set the upstream up the first time:

```sh
git remote add talon-vscode-command-client git@github.com:pokey/talon-vscode-command-client.git
```
