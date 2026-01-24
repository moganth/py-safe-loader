# Contributing to py-safe-loader

Thank you for your interest in contributing! To maintain code quality and security, we require all contributions to follow these guidelines.

## Sign Your Commits (DCO)

All commits must include a Developer Certificate of Origin (DCO) sign-off. This certifies that you have the right to submit the code and agree to the project license.

### How to sign commits:

```bash
git commit -s -m "Your commit message"
```

This adds a `Signed-off-by` line with your name and email.

### Make it automatic:

```bash
git config --local format.signoff true
```

Now all your commits will be signed automatically.

### For existing unsigned commits:

```bash
git commit --amend -s --no-edit
git push --force
```

## Cryptographically Signed Commits Required

This repository requires all commits to be cryptographically signed with GPG or SSH keys.

### SSH Signing (Recommended):

```bash
# Configure git to sign with SSH
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Then add your SSH key as a **Signing Key** in GitHub:
- Go to [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys)
- Click **New SSH key**
- Select **Key type: Signing Key**
- Paste your public key

### GPG Signing:

```bash
# Generate GPG key
gpg --full-generate-key

# List keys and copy the key ID
gpg --list-secret-keys --keyid-format=long

# Configure git
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Export public key
gpg --armor --export YOUR_KEY_ID
```

Add the exported GPG key to [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys).

## Pull Request Process

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes with signed commits
4. Ensure all tests pass
5. Submit a pull request

All PRs must:
- Have signed commits (DCO)
- Have cryptographically signed commits (GPG/SSH)
- Pass all status checks (tests, code scanning, DCO check)
- Be reviewed before merging

## Questions?

Open an issue if you need help with the contribution process.
