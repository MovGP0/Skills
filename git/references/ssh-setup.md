# SSH Setup For Git

## Windows SSH Agent

Enable and start the SSH agent:

```powershell
Set-Service ssh-agent -StartupType Manual
Start-Service ssh-agent
```

## Create And Register A Key

Create a key:

```powershell
ssh-keygen -C "user@example.com"
```

Add the private key to the agent:

```powershell
ssh-add ~/.ssh/id_rsa
```

Register the public key content from `~/.ssh/id_rsa.pub` with the Git server:

```text
ssh-rsa <public-key-material> user@hostname
```

## Host Compatibility Settings

Some older servers require explicit RSA algorithm compatibility in `~/.ssh/config`:

```sshconfig
Host *.example.com
    HostkeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
```

Use the narrowest matching host pattern possible.

## Git Config Context

An SSH-based Git setup often also has editor, LFS, user, and credential settings in `~/.gitconfig`. Treat note examples as placeholders and avoid copying private server names, user names, email addresses, or TLS workarounds into another machine unchanged.

Clone through SSH once the server has the public key:

```bash
git clone ssh://example.com/path/to/repository.git
```
