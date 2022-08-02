tag: terminal
and tag: user.git
-
# Standard commands
git add patch: "git add . -p\n"
git add: "git add "
git add everything: "git add -u\n"
git bisect: "git bisect "
git blame: "git blame "
git branch: "git branch "
git branch list: "git branch -vv\n"
git remote branches: "git branch --remote\n"
git branch <user.text>: "git branch {text}"
git checkout: "git checkout "
git checkout master: "git checkout master\n"
git checkout main: "git checkout main\n"
git checkout <user.text>: "git checkout {text}"
git cherry pick: "git cherry-pick "
git cherry pick continue: "git cherry-pick --continue "
git cherry pick abort: "git cherry-pick --abort "
git cherry pick skip: "git cherry-pick --skip "
git clone: "git clone "
# Leave \n out for confirmation since the operation is destructive
git clean everything: "git clean -dfx"
git commit message <user.text>: "git commit -m '{text}'"
git commit: "git commit\n"
git commit amend: "git commit --amend\n"
git commit no verify: "git commit -n"
git commit existing: "git commit -a\n"
git diff (colour|color) words: "git diff --color-words "
git diff: "git diff "
git diff cached: "git diff --cached\n"
git diff tool: "git difftool -d\n"
git diff tool cached: "git difftool --cached -d\n"
git fetch: "git fetch\n"
git fetch all: "git fetch --all\n"
git fetch <user.text>: "git fetch {text}"
git fetch prune: "git fetch --prune\n"
git in it: "git init\n"
git log all: "git log\n"
git log all changes: "git log -c\n"
git log: "git log "
git log changes: "git log -c "
git merge: "git merge "
git merge <user.text>:"git merge {text}"
git merge tool: "git mergetool\n"
git move: "git mv "
git pull: "git pull\n"
git pull origin: "git pull origin "
git pull rebase: "git pull --rebase\n"
git pull fast forward: "git pull --ff-only\n"
git pull <user.text>: "git pull {text} "
git push: "git push\n"
git push origin: "git push origin "
git push up stream origin: "git push -u origin"
git push <user.text>: "git push {text} "
git push tags: "git push --tags\n"
git rebase: "git rebase "
git rebase continue: "git rebase --continue"
git rebase skip: "git rebase --skip"
git remove: "git rm "
git (remove|delete) branch: "git branch -d "
git (remove|delete) remote branch: "git push --delete origin "
git reset: "git reset "
git reset soft: "git reset --soft "
git reset hard: "git reset --hard "
git restore: "git restore "
git restore staged: "git restore --staged "
git restore source: "git restore --source="
git remote: "git remote "
git remote add: "git remote add "
git remote list: "git remote -v\n"
git remote set url: "git remote set-url "
git remote add upstream: "git remote add upstream "
git remote remove: "git remote remove "
git remote show origin: "git remote show origin\n"
git show: "git show "
git stash pop: "git stash pop\n"
git stash: "git stash\n"
git stash push: user.insert_between("git stash push -m '", "'")
git stash apply: "git stash apply\n"
git stash list: "git stash list\n"
git stash show: "git stash show"
git status: "git status\n"
git switch [<user.text>]: "git switch {user.formatted_text(text or '', 'DASH_SEPARATED')}"
git switch master: "git switch master "
git switch main: "git switch main "
git switch detached: "git switch --detach "
git (switch create | new branch) [<user.text>]:
  "git switch -c {user.formatted_text(text or '', 'DASH_SEPARATED')}"
git switch orphan: "git switch --orphan "
git submodule add:  "git submodule add "
git tag: "git tag "

# Convenience
git edit config: "git config --local -e\n"

git clone clipboard:
  insert("git clone ")
  edit.paste()
  key(enter)
git diff highlighted:
    edit.copy()
    insert("git diff ")
    edit.paste()
    key(enter)
git diff clipboard:
    insert("git diff ")
    edit.paste()
    key(enter)
git add highlighted:
    edit.copy()
    insert("git add ")
    edit.paste()
    key(enter)
git add clipboard:
    insert("git add ")
    edit.paste()
    key(enter)
git commit highlighted:
    edit.copy()
    insert("git add ")
    edit.paste()
    insert("\ngit commit\n")
