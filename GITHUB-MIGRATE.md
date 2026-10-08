# Move Kuyet to another GitHub account

## 1. Create the repo on the new account

On the **new** GitHub user or org: **New repository** → name e.g. `kuyet` → empty (no README).

## 2. Push from this machine

This clone is configured as:

| Remote     | URL |
|-----------|-----|
| `melody`  | `git@github.com:Melody4063/kuyet.git` |
| `agbolase`| `git@github.com:agbolase/kuyet.git` (backup) |

```bash
cd /home/agbolase/Projects/Kuyet
git push -u melody main
```

If SSH fails with **Permission denied to agbolase**, this PC’s key is tied to the `agbolase` account. Use one of:

**A — Personal access token (quickest)**  
On GitHub as **Melody4063**: Settings → Developer settings → Fine-grained token → repo access `kuyet` → Contents read/write.

```bash
cd /home/agbolase/Projects/Kuyet
git remote set-url melody https://github.com/Melody4063/kuyet.git
git push -u melody main
# Username: Melody4063
# Password: paste the token (not your GitHub password)
```

**B — SSH key on Melody4063**  
Add this machine’s public key (`~/.ssh/id_ed25519.pub` or `id_rsa.pub`) under **Melody4063** → Settings → SSH keys, then `git push -u melody main` again.

## 3. Reconnect Codemagic

1. Codemagic → **Applications** → add app or change repository URL to `github.com/NEWUSER/kuyet`.
2. Sign in to GitHub as the **new** account when authorizing Codemagic.
3. Trigger **Start new build** on `main` (uses `codemagic.yaml` at repo root).

## 4. Optional: remove old remote

```bash
git remote remove old-origin
```
