#os: linux
tag: terminal
-

# general
task version: "task --version\n"
task commands: "task commands\n"
task help: "task help\n"

# task list
task list: "task list\n"
task list orphans: "task project: list\n"
task list untagged: "task tags.none: list\n"
task list completed: "task completed\n"
task list completed project: "task completed project:"
task list <user.text>: "task list {text}\n"
task list project: "task list project: "
task list project <user.text>: "task list project:{text}\n"

task view <user.text>: "task list project:{text}\n"

# task editing
task <number_small> edit: "task {number_small} edit\n"

# task add
task add: "task add "
task add <user.text>: "task add {text}\n"
task undo: "task undo\n"

tasks [list] all: "task\n"
(tasks|task next): "task next\n"

# task editing
task <number_small> (edit|at it)$: "task {number_small} edit"
task <number_small> modify: "task {number_small} modify "


# task starting and stopping
task (<number_small> start|start <number_small>)$: "task {number_small} start"
task (<number_small> stop|stop <number_small>)$: "task {number_small} stop"
task stop active: "task +ACTIVE stop\n"
task (<number_small> done|done <number_small>)$: "task {number_small} done"
task done <number_small>$: "task {number_small} done"
task (<number_small> delete|delete <number_small>)$: "task {number_small} delete"

task <number_small>$: "task {number_small} "
