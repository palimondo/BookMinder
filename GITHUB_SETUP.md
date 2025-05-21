# GitHub Setup Instructions

Since you don't have GitHub CLI installed, follow these steps to connect your local repository to GitHub:

## 1. Create a Repository on GitHub

1. Go to [GitHub](https://github.com)
2. Log in with your username `palimondo`
3. Click the "+" icon in the top right and select "New repository"
4. Fill in:
   - Repository name: BookMinder
   - Description: Extract content and highlights from Apple Books for LLM analysis
   - Visibility: Public
   - Initialize with: Don't select any options (we'll push existing code)
5. Click "Create repository"

## 2. Connect Your Local Repository

After creating the repository, GitHub will show instructions. Run these commands:

```bash
# Add the GitHub repository as a remote
git remote add origin https://github.com/palimondo/BookMinder.git

# Push your main branch to GitHub
git checkout main
git push -u origin main

# Push your astral branch to GitHub
git checkout astral
git push -u origin astral
```

## 3. Setting Up on Your MacBook Air

Once your repository is on GitHub, you can set up on a fresh macOS installation:

1. Follow the instructions in the `docs/uv_setup.md` file, particularly the "Fresh macOS Installation" section
2. This will guide you through installing the necessary development tools and setting up the project

## 4. Optional: Install GitHub CLI

If you'd like to simplify GitHub operations in the future, you can install GitHub CLI:

```bash
# Install via Homebrew
brew install gh

# Authenticate
gh auth login
```

This makes managing pull requests, issues, and other GitHub tasks easier from the command line.
