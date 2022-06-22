app: thunderbird_tasks
-
# event/task
event new: user.thunderbird_mod("i")
task new: user.thunderbird_mod("d")
(task | event) delete: key(delete)
# layout
toggle today: key(f11)
