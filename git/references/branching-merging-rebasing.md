# Branching, Merging, And Rebasing

Use this reference for branch topology and history-editing tasks. Always inspect the current branch, upstream, and dirty state first:

```bash
git status --short --branch
git branch -vv
git log --oneline --decorate --graph --all -20
```

Do not rewrite public/shared history unless the user explicitly asks for that and understands the consequence.

## Branch Management

Create and switch:

```bash
git switch -c feature/name
git switch feature/name
```

Older equivalent:

```bash
git checkout -b feature/name
git checkout feature/name
```

Rename the current branch:

```bash
git branch -m new-name
```

Set upstream:

```bash
git push -u origin feature/name
git branch --set-upstream-to=origin/feature/name
```

Delete branches after confirming they are merged or no longer needed:

```bash
git branch --merged
git branch -d feature/name
git push origin --delete feature/name
```

Use `-D` only when deliberately deleting an unmerged local branch.

## Merge

Use a fast-forward merge when the target can simply advance:

```bash
git switch main
git merge --ff-only feature/name
```

Create an explicit merge commit when preserving branch topology matters:

```bash
git switch main
git merge --no-ff feature/name
```

Abort a conflicted merge:

```bash
git merge --abort
```

After resolving conflicts:

```bash
git status --short
git add <resolved-files>
git merge --continue
```

## Rebase

Update a feature branch on top of a newer base:

```bash
git fetch origin
git switch feature/name
git rebase origin/main
```

Abort or continue:

```bash
git rebase --abort
git add <resolved-files>
git rebase --continue
```

Use `--onto` to transplant a commit range to a different base:

```bash
git rebase --onto <new-base> <old-base> <branch>
```

Example: move commits after `old-base` from `feature/name` onto `origin/main`:

```bash
git rebase --onto origin/main old-base feature/name
```

## Interactive Rebase

Edit the last `N` commits:

```bash
git rebase -i HEAD~N
```

Common todo actions:

```text
pick   keep commit as-is
reword keep changes but edit message
edit   stop at commit for manual changes
squash combine with previous commit and edit message
fixup  combine with previous commit and discard this message
drop   remove commit
```

Before interactive rebase, inspect the range:

```bash
git log --oneline --decorate HEAD~N..HEAD
```

## Amend The Latest Commit

Amend staged changes into the latest commit:

```bash
git add <files>
git commit --amend
```

Keep the message:

```bash
git add <files>
git commit --amend --no-edit
```

Amending rewrites the commit hash. Avoid amending commits others may already have based work on unless coordinating.

## Fixup Commit And Autosquash

Create a fixup commit for a target commit:

```bash
git commit --fixup <target-commit>
```

Then autosquash during interactive rebase:

```bash
git rebase -i --autosquash <base>
```

For the last 10 commits:

```bash
git rebase -i --autosquash HEAD~10
```

If `rebase.autoSquash=true`, Git will automatically reorder `fixup!` and `squash!` commits when starting an interactive rebase.

## Split A Commit

Use interactive rebase and mark the commit with `edit`:

```bash
git rebase -i <base-before-commit>
```

When Git stops at the commit, reset it while keeping its changes in the worktree:

```bash
git reset HEAD^
```

Create smaller commits:

```bash
git add <first-set-of-files>
git commit -m "First focused change"
git add <second-set-of-files>
git commit -m "Second focused change"
git rebase --continue
```

Use patch staging when a single file needs to be split:

```bash
git add -p
```

## Edit An Older Commit

Start an interactive rebase before the commit:

```bash
git rebase -i <commit>^
```

Change `pick` to `edit` for that commit. When Git stops:

```bash
git add <files>
git commit --amend
git rebase --continue
```

## Drop Or Reorder Commits

Use interactive rebase:

```bash
git rebase -i <base>
```

Move lines to reorder commits. Delete a line or use `drop` to remove a commit. Inspect the resulting history afterward:

```bash
git log --oneline --decorate --graph <base>..HEAD
```

## Publishing Rewritten History

After a rebase, amended commit, split, or autosquash, prefer:

```bash
git push --force-with-lease
```

`--force-with-lease` refuses to overwrite remote work that appeared after the last fetch. Fetch and inspect before retrying if it fails.
