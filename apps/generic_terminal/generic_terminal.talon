tag: terminal
-
# tags should be activated for each specific terminal in the respective talon file

lisa:
    user.terminal_list_directories()
lisa all:
    user.terminal_list_all_directories()
katie [<user.text>]: user.terminal_change_directory(text or "")
katie root: user.terminal_change_directory_root()
go <user.system_path>: insert("cd \"{system_path}\"\n")
clear screen: user.terminal_clear_screen()
run last: user.terminal_run_last()
rerun [<user.text>]: user.terminal_rerun_search(text or "")
rerun search: user.terminal_rerun_search("")
kill all: user.terminal_kill_all()

git status:
  "git status"
  key(enter)

git fetch:
  "git fetch"
  key(enter)

git pull:
  "git pull"
  key(enter)

git checkout:
  "git checkout "

git commit all:
  "git commit -am \""

git branch:
  "git checkout -b "

git push:
  "git push"


git set upstream:
  "git branch --set-upstream-to=origin/"


git add all:
  "git add ."
  key(enter)

git commit:
  "git commit -m \""


git log:
  "git log --oneline"
  key(enter)

git push origin head:
  "git push origin head"

git stash:
  "git stash"

git stash apply:
  "git stash apply"

git clone:
  "git clone "

git change name:
  "git config user.name "

git change email:
  "git config user.email "


  

copy paste:

    edit.copy()
    sleep(50ms)
    edit.paste()
