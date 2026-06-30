# Daily Git Workflows

## Branches

Create and switch branches:

```bash
git branch feature/name
git checkout feature/name
git checkout -b feature/name
```

List branches:

```bash
git branch
git branch --all
git branch -vv
git branch -vv --all
```

Delete a local branch only after confirming it is merged or no longer needed:

```bash
git branch -d feature/name
```

## Commits

Stage and commit:

```powershell
git add *
git commit -m "Commit message"
```

Commit tracked changes:

```powershell
git commit -a -m "Commit message"
```

If untracked files should be included, stage them explicitly first:

```powershell
git add -A
git commit -m "Commit message"
```

## Stash

Save current changes:

```bash
git stash
git stash push -m "item-name"
```

List stash entries:

```bash
git stash list
```

Apply and remove a stash:

```bash
git stash pop
git stash pop stash@{1}
git stash pop --index 1
```

Apply and keep a stash:

```bash
git stash apply
git stash apply stash@{1}
git stash apply --index 1
```

Delete stash entries:

```bash
git stash drop
git stash clear
```

## Bisect

Use bisect to find the commit that introduced a bug:

```powershell
git bisect start
git bisect start <bad-commit> <good-commit>
git bisect bad <bad-commit>
git bisect good <good-commit>
git bisect skip <commit-that-cannot-be-tested>
git bisect reset
```

Manual flow:

```powershell
git bisect start
git bisect bad <known-bad-commit>
git bisect good <known-good-commit>
git bisect good
git bisect bad
git bisect reset
```

## Worktrees

Worktrees allow multiple checkouts from the same repository:

```bash
git worktree add <path> <branch>
git worktree list
git worktree remove <path>
```

Before removing a worktree, check for uncommitted changes inside that worktree.

## Tags

Create an annotated tag:

```bash
git tag -a "version.1.2.3" -m "Message" <commit>
```

Push tags:

```bash
git push origin "version.1.2.3"
git push origin --tags
```

Query tags:

```bash
git tag -l "version.*" -n 1
git rev-list --no-walk "version.1.2.3"
git rev-list --count <commit>..HEAD
```

## Remotes

Prune deleted remote refs:

```bash
git remote update --prune
```

## Revert And Reset

Revert creates a new commit that undoes a previous commit:

```powershell
git revert <commit>
```

Reset hard moves the current branch and discards local worktree changes. Inspect first:

```bash
git status --short --branch
git reset --hard origin/main
```

Only run `reset --hard` when discarding local changes is intentional.

## Git Notes

Git notes attach metadata to commits without changing the commit:

```bash
git notes add -m "Comment"
git notes add -m "Comment" <commit>
git notes edit <commit>
git notes remove <commit>
git notes add -m "Comment" --ref=<namespace>
```

Notes are visible in log output when the relevant notes ref is available. They can be shared by pushing or fetching the notes ref explicitly.

## Refs Format Migration

Some applications may not support newer ref storage formats. To migrate refs back to files:

```powershell
git refs migrate --ref-format=files
```

Inspect the repository and tool compatibility before running migrations.
