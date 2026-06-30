# Submodules And Subtrees

## Decision Guide

Use submodules when:

- The dependency should remain a separate repository.
- The dependency is maintained independently.
- The main repository should track a specific dependency commit.
- Keeping the main repository smaller matters.

Use subtrees when:

- The dependency should be integrated into the main repository.
- A simpler clone workflow matters.
- Unified history is preferred.
- A larger main repository is acceptable.

| Feature | Submodule | Subtree |
| --- | --- | --- |
| Repository structure | Separate repositories | Integrated into the main repository |
| Clone behavior | Requires init/update steps | Normal clone contains the subtree |
| History tracking | Main repository tracks a specific submodule commit | Subtree history is merged into main history |
| Management | More complex | Simpler day-to-day workflow |
| Repository size | Smaller main repository | Larger main repository |
| Independence | Strong independent development | Less modular |

## Submodules

Add a submodule:

```bash
git submodule add <repository-url> <path>
```

Initialize submodules after clone:

```bash
git submodule update --init --recursive
```

Update submodules:

```bash
git submodule update --remote
```

Use a subtree instead when the subdirectory should behave as part of the current repository.

## Subtrees

Add a subtree:

```bash
git subtree add --prefix=<directory> <repository-url> <branch>
```

Update a subtree:

```bash
git subtree pull --prefix=<directory> <repository-url> <branch>
```

Push changes from a subtree:

```bash
git subtree push --prefix=<directory> <repository-url> <branch>
```

Subtrees are part of the main repository checkout; no extra clone initialization is required.
