app: /.*terminal/
app: Cmd.exe
app: iTerm2
app: Terminal
-
git add: insert("git add ")
git add patch:
  insert("git add . -p")
  key(enter)
git checkout: insert("git checkout ")
git new branch: insert("git checkout -b ")
git push:
  insert("git push")
  key(enter)
git push origin: insert("git push origin ")
git pull:
  insert("git pull")
  key(enter)
git pull origin: insert("git pull origin ")
git commit:
  insert("git commit")
  key(enter)
git clone clipboard:
  insert("git clone ")
  edit.paste()
  key(enter)
git status:
  insert("git status")
  key(enter)
git log:
  insert("git log")
  key(enter)
git stash:
  insert("git stash")
  key(enter)
git stash pop:
  insert("git stash pop")
  key(enter)