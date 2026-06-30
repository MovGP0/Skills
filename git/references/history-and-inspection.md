# History And Inspection

## Log Views

Compact graph:

```powershell
git log --graph --decorate --oneline
```

Custom history alias:

```powershell
git config --global alias.hs "log --pretty='%C(yellow)%h %C(cyan)%cd %Cblue%aN%C(auto)%d %Creset%s' --graph --date=relative --date-order"
git hs
```

Show only changed files in history:

```bash
git log --name-only --pretty=format:
```

## Search History

Pickaxe search for added or removed text:

```powershell
git log -S "FOOBAR"
```

Commit-message search:

```bash
git log --grep="FOOBAR" --since="2020-01-01" --until="2025-12-31"
```

## Find Hot Files

Most changed files by commit count:

```bash
git log --name-only --pretty=format: \
| sort | uniq -c | sort -rn
```

Files with many bug-fix commits:

```bash
git log --since="1 year ago" --no-merges --name-only --pretty=format: --grep="fix\|bug\|hotfix\|patch\|regression" -i \
| sort | uniq -c | sort -rn
```

On Windows, use the available shell tools. If a pipeline fails in PowerShell because of quoting or command differences, rerun it in the shell best suited to the local environment.

## Reflog

Use reflog to inspect recent local branch and HEAD movements:

```bash
git reflog
```

Reflog is often the first recovery tool after an accidental reset, rebase, or branch movement.

## Show Refs

List named refs:

```bash
git show-ref
```

Example ref categories include local branches, remote-tracking branches, notes refs, and tags:

```text
<sha> refs/heads/main
<sha> refs/remotes/origin/main
<sha> refs/notes/commits
<sha> refs/tags/v1.2.3
```

## Fsck

Find unreachable objects, including orphaned commits:

```bash
git fsck --unreachable
```

Use this for recovery investigations before pruning or garbage collection.

## External History Tools

The notes mention these history-analysis tools:

- GitK
- Git of Theseus
- Hercules
