# Large Repositories And Extensions

## Git LFS

Install Git LFS:

```bash
winget install -e --id GitHub.GitLFS
brew install git-lfs
sudo apt-get install git-lfs
```

Initialize LFS in a repository:

```bash
git lfs install
```

Track binary patterns:

```bash
git lfs track "*.jpg"
git lfs track "*.pdf"
```

Typical `.gitattributes` entries:

```gitattributes
*.psd filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
```

Check status:

```bash
git lfs status
```

Fetch a specific file's LFS content:

```bash
git lfs fetch --include "path/to/file.jpg"
```

When enabling LFS in an existing repository, inspect existing hooks before running commands that may overwrite them.

## Scalar / Microsoft Git

Scalar helps with large repository maintenance:

```bash
winget install --id Microsoft.Git
scalar clone <repository-url>
scalar register <repository-path>
scalar maintenance run
```

Submodule operations still use Git commands:

```bash
scalar clone --recurse-submodules <repository-url>
git submodule update --init --recursive
```

Scalar can be used with subtree workflows as well:

```bash
git subtree add --prefix=<directory> <repository-url> <branch>
git subtree pull --prefix=<directory> <repository-url> <branch>
```

## VFS For Git

The notes identify Git VFS as replaced by Scalar/Microsoft Git. Prefer Scalar for new work unless a legacy repository explicitly requires VFS.

Legacy commands:

```bash
winget install -e --id Microsoft.VFSforGit
gvfs clone https://server/example.git D:\Repository
gvfs mount D:\Repository
gvfs prefetch --files "*.cs"
gvfs status
gvfs diagnose
gvfs unmount D:\Repository
```

## git-tfs

Install:

```powershell
choco install gittfs
```

List remote TFS branches:

```powershell
git tfs list-remote-branches "https://tfs.example.com/Collection/"
```

Clone TFSVC content:

```powershell
git tfs clone "https://tfs.example.com/Collection/" "$/Project/Folder"
git tfs clone "https://tfs.example.com/Collection/" "$/Project/Folder" FolderName --branches=none
```

Verify and fetch:

```powershell
git tfs verify
git tfs fetch
```

Check in to TFS:

```powershell
git tfs checkin -m "Message"
git tfs checkin
```

Rename a TFS changeset comment:

```powershell
tf changeset /comment:"New comment" 8675309
```

Use placeholders for server URLs, collection names, project paths, and credentials from the user's actual environment.
