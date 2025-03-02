os: linux
tag: terminal
and tag: user.taskwarrior
-
# general
task version: "task --version\n"
task commands: "task commands\n"
task help: "task help\n"

# task list
task list: "task list\n"
task list orphans: "task project: list\n"
task list untagged: "task tags.none: list\n"
task list <user.text>: "task list {text}\n"
task list project: "task list project: "
task list project <user.text>: "task list project:{text}\n"

# task add
task add: "task add "
task add <user.text>: "task add {text}\n"
task undo: "task undo\n"

(tasks | task next): "task next\n"

# task editing
task <number> edit$: "task {number} edit"

# task completion
task <number> done$: "task {number} done"
task <number> delete$: "task {number} delete"
