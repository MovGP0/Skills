# Git Configuration

## Config Scopes

`git config` reads and writes Git settings at three levels:

- Local: repository-specific settings in `.git/config`.
- Global: user-specific settings, usually in `~/.gitconfig`.
- System: machine-wide settings.

Local overrides global, and global overrides system. If no scope is specified, Git writes local configuration when run inside a repository.

Useful commands:

```bash
git config user.email
git config --local user.email "first.last@example.com"
git config --global --edit
git config --list --show-origin
git config --global --add alias.lg "log --graph --oneline --all"
git config --global --unset alias.lg
```

## Identity

Set identity globally unless the repository needs a project-specific identity:

```bash
git config --global user.name "Firstname Lastname"
git config --global user.email "first.last@example.com"
```

## Aliases

Aliases without `!` are expanded as Git subcommands. Aliases with `!` run shell commands:

```powershell
git config --global alias.a "add ."
git config --global alias.ac "!git add -A && git commit -m"
```

Usage:

```powershell
git a
git ac "Commit message"
```

## Editor, Diff Tool, And Merge Tool

Visual Studio Code can be configured as the editor and as diff/merge tooling:

```powershell
git config --global core.editor "code --wait"
git config --global diff.tool default-difftool
git config --global difftool.default-difftool.cmd "code --wait --diff `$LOCAL `$REMOTE"
git config --global merge.tool code
git config --global mergetool.code.cmd "code --wait --merge `$REMOTE `$LOCAL `$BASE `$MERGED"
```

When writing these values into `.gitconfig` directly:

```ini
[core]
    editor = code --wait
[diff]
    tool = default-difftool
[difftool "default-difftool"]
    cmd = code --wait --diff $LOCAL $REMOTE
[merge]
    tool = code
[mergetool "code"]
    cmd = code --wait --merge $REMOTE $LOCAL $BASE $MERGED
```

## Credential Helpers

Use the OS credential helper when possible:

```bash
git config --global credential.helper wincred
git config --global credential.helper osxkeychain
git config --global credential.helper store
```

On Windows, credentials can also be inspected in Credential Manager under Windows Credentials. Git server entries commonly use an address such as `git:https://example.com/`.

## Self-Signed Certificates

Do not disable certificate verification globally by default:

```bash
git config --global http.sslVerify false
```

Prefer a host-scoped exception when no better certificate solution is available:

```bash
git config --global http.https://example.com.sslVerify false
git config --global http.sslVerify true
git config --global http.version HTTP/1.1
```

Also consider Git Credential Manager's TLS/certificate configuration before weakening Git's global TLS behavior.

## Recommended Config Shape

These settings from the notes are useful defaults when they match the repository and team:

```ini
[branch]
    sort = committerdate
[commit]
    verbose = true
[column]
    ui = auto
[core]
    fsmonitor = true
    untrackedCache = true
    autocrlf = false
    ignorecase = false
[diff]
    algorithm = histogram
    colorMoved = plain
    mnemonicPrefix = true
    renames = true
[fetch]
    prune = true
    pruneTags = true
    all = true
[grep]
    patternType = perl
[help]
    autocorrect = prompt
[init]
    defaultBranch = main
[merge]
    conflictstyle = zdiff3
    ff = only
[push]
    default = simple
    autoSetupRemote = true
    followTags = true
[pull]
    rebase = true
[rebase]
    autoSquash = true
    autoStash = true
    updateRefs = true
[rerere]
    enabled = true
    autoupdate = true
[tag]
    sort = version:refname
```

Check team conventions before setting line-ending, merge, pull, or rebase defaults globally.
