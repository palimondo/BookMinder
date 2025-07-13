---
description: Say hi and get caught up on the BookMinder project
allowed-tools: Bash(tree:*), Bash(source:*), Bash(pytest:*), Bash(git log:*), Bash(git status:*), Read
---

# Hi! Let's get caught up on BookMinder

First, let's check the project structure:

`tree -h -I '__pycache__|claude-dev-log-diary|Library' .` # Library folders in `fixture/users` ommitted for brevity
```zsh
!`tree -h -I '__pycache__|claude-dev-log-diary|Library' .`
```

Next, let's check the living specification and our test coverage:
`source .venv/bin/activate && pytest --spec  --cov=bookminder --cov-report=term-missing`
```zsh
!`source .venv/bin/activate && pytest --spec --cov=bookminder --cov-report=term-missing`
```

Let's check recent work:
`git log --oneline -10`
```zsh
!`git log --oneline -10`
```

`git status`
```zsh
!`git status`
```

Finally read key documentation:

@docs/apple_books.md
@TODO.md

Let's NOT jump straight into the action! We'll think harder about where we are in the project and we'll **discuss and plan** the next steps first.