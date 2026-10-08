# Move Kuyet to another GitHub account

## 1. Create the repo on the new account

On the **new** GitHub user or org: **New repository** → name e.g. `kuyet` → empty (no README).

## 2. Push from this machine

Replace `NEWUSER` with the GitHub username or org:

```bash
cd /home/agbolase/Projects/Kuyet
git remote rename origin old-origin    # keeps agbolase/kuyet as backup remote
git remote add origin git@github.com:NEWUSER/kuyet.git
git push -u origin main
```

If SSH is only set up for `agbolase`, either:

- Add an SSH key to the **new** GitHub account, or  
- Use HTTPS: `git remote add origin https://github.com/NEWUSER/kuyet.git` and a **Personal Access Token** when prompted.

## 3. Reconnect Codemagic

1. Codemagic → **Applications** → add app or change repository URL to `github.com/NEWUSER/kuyet`.
2. Sign in to GitHub as the **new** account when authorizing Codemagic.
3. Trigger **Start new build** on `main` (uses `codemagic.yaml` at repo root).

## 4. Optional: remove old remote

```bash
git remote remove old-origin
```
