---
description: Say hi and get caught up on the BookMinder project
allowed-tools: Bash(tree:*), Bash(pytest:*), Bash(git log:*), Bash(git status:*), Read
---

# Hi! Let me get caught up on BookMinder

First, let me check the project structure and current state:

tree -h -I '__pycache__|claude-dev-log-diary' .
!`tree -h -I '__pycache__|claude-dev-log-diary' .`

pytest --spec
!`pytest --spec`

Now I'll read the key documentation:

@docs/apple_books.md
@TODO.md

Let me also check recent work:

git log --oneline -10
!`git log --oneline -10`

git status
!`git status`