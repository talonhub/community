app: /terminal/
app: cmd.exe
app: iTerm2
app: Terminal
app: Windows Command Processor
app: Code
app: Visual Studio Code
app: Code.exe
-
git add patch: "git add . -p\n"
git add: "git add "
git bisect: "git bisect "
git branch: "git branch "
git checkout: "git checkout "
git cherry pick: "git cherry-pick "
git clone: "git clone "
git clone clipboard:
  insert("git clone ")
  edit.paste()
  key(enter)
git commit message <phrase>: "git commit -m '{phrase}'"
git commit: "git commit\n"
git diff (colour|color) words: "git diff --color-words "
git diff: "git diff "
git fetch: "git fetch\n"
git fetch <phrase>: "git fetch {phrase}"
git in it: "git init\n"
git log: "git log\n"
git merge: "git merge "
git merge <phrase>:"git merge {phrase}"
git move: "git mv "
git new branch: "git checkout -b "
git pull: "git pull\n"
git pull origin: "git pull origin "
git pull rebase: "git pull --rebase\n"
git pull <phrase>: "git pull {phrase} "
git push: "git push\n"
git push origin: "git push origin "
git push <phrase>: "git push {phrase} "
git push tags: "git push --tags\n"
git rebase: "git rebase\n"
git rebase continue: "git rebase --continue"
git rebase skip: "git rebase --skip"
git remove: "git rm "
git reset: "git rese "
git reset soft: "git reset --soft "
git reset hard: "git reset --hard "
git show: "git show "
git stash pop: "git stash pop\n"
git stash: "git stash\n"
git status: "git status\n"
git tag: "git tag "

