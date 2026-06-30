---
name: git
description: "Local Git operations skill based on the user's Obsidian Git notes. Use when Codex needs to help with Git configuration, commits, branches, merging, rebasing, fixup commits, amending commits, splitting commits, stash, bisect, worktrees, tags, logs, reflog, refs, LFS, Scalar, git-tfs, submodules, subtrees, SSH setup, credential helpers, or Git troubleshooting workflows."
---

# Git

## Overview

Use this skill for practical Git tasks and troubleshooting. Start from the repository state and the exact command, branch, commit, remote, or error the user mentions. Prefer focused commands that inspect the current state before changing anything.

When the task involves a destructive or history-changing operation such as `reset --hard`, branch deletion, force pushes, or broad cleanup, inspect state first and make the risk explicit before acting.

## Reference Routing

Read only the reference file needed for the current task:

- `references/configuration.md`: `git config`, identity, aliases, editor/diff/merge tool setup, credential helpers, self-signed certificate handling, and recommended config values.
- `references/daily-workflows.md`: branches, commits, stash, bisect, worktrees, tags, remote pruning, revert/reset, Git notes, and basic ref migration.
- `references/branching-merging-rebasing.md`: branch management, merge choices, conflict handling, rebasing, autosquash fixups, amend, split commits, reorder/drop commits, and force-with-lease guidance.
- `references/history-and-inspection.md`: `git log`, pickaxe/grep history search, changed-file history analysis, `show-ref`, `reflog`, and `fsck`.
- `references/large-repos-and-extensions.md`: Git LFS, Scalar/Microsoft Git, VFS for Git, and git-tfs.
- `references/submodules-and-subtrees.md`: choosing between submodules and subtrees plus add/update/push commands.
- `references/ssh-setup.md`: SSH agent setup, key creation, host compatibility settings, public-key registration, and SSH clone reminders.

## Operating Rules

- Use `git status --short --branch` or a similarly focused inspection command before changing repository state.
- Preserve the user's exact branch, path, remote, commit hash, and ref names.
- Prefer scoped, reversible operations over broad cleanup.
- Do not run destructive commands just because a note lists them as examples.
- Treat examples that contain private names, email addresses, IP addresses, domains, or credentials as placeholders to be replaced with task-specific values.
- For Git LFS setup, avoid overwriting existing hooks blindly. If hooks already exist, inspect them and use the manual update flow when needed.
- For self-signed certificate problems, avoid globally disabling TLS verification. Prefer host-scoped configuration or Git Credential Manager certificate configuration.
- For large repositories, consider Scalar before older VFS for Git; the notes identify VFS for Git as superseded.

## Validation

After making Git configuration or repository changes, validate with the narrowest useful command:

```bash
git status --short --branch
git config --list --show-origin
git log --oneline --decorate -5
```

Use only the commands relevant to the task; do not dump large logs unless the user asks for them.
