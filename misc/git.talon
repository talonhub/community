app: /terminal/
app: Cmd.exe
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
git push <phrase>: insert("git push {phrase} ")
git pull:
  insert("git pull")
  key(enter)
git pull <phrase>: insert("git pull {phrase} ")
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