# Context Recovery Pattern

## Overview

This document captures an effective pattern for using Task delegation to recover context after memory compaction events.

## The Problem

After context compaction (manual `/compact` or automatic), the assistant loses crucial context about:
- Design decisions and rationale
- User corrections and redirections  
- Implementation details and current state
- Philosophical discussions about methodology

## The Solution: Deep Context Recovery via Task

### Initial Attempt (Less Effective)

The first attempt provided specific search suggestions:
```
- Conversation mode design: `./xs e583 -S "conversation mode"`
- Bug symptoms: `./xs e583 -S "bug|error|issue"`
- Design decisions: `./xs e583 -S "should|design|approach"`
```

This approach yielded surface-level results - the Task found matches but didn't synthesize deep understanding.

### Improved Approach (Highly Effective)

The second attempt removed specific searches and instead asked for:
1. **Start by scanning the timeline** to understand session flow
2. **Think carefully between each tool use** about what to explore next
3. **Extract full details** of design conversations with complete context
4. **Focus on the WHY** behind decisions

This yielded rich insights including:
- The fundamental tension the tool addresses
- The "xs" naming philosophy (extra small, excess sessions, cross-session)
- Scientific methodology discussions
- Self-documenting UX principles
- Tool boundary philosophy

## Key Elements of Effective Prompting

### 1. Avoid Over-Specification
Don't provide specific searches - let the Task agent discover patterns organically.

### 2. Emphasize Thinking
Explicitly ask the agent to "think carefully between each tool use" - this promotes deeper analysis rather than mechanical searching.

### 3. Request Full Context
Ask for "full details of design conversations" rather than summaries - this captures nuance.

### 4. Focus on Understanding
Direct attention to "WHY behind decisions" rather than just WHAT was done.

### 5. Start with Overview
Begin with timeline scanning to understand structure before diving into specifics.

## Template for Future Use

```
Deep dive into session [ID] to extract full details of design conversations between user and assistant.

### Your Mission
1. **Start by scanning the timeline** to understand the session's flow and structure
2. **Identify design conversations** - look for patterns where user and assistant discuss approaches, architecture, or implementation strategies
3. **Extract full details** of these conversations with complete context
4. **Think carefully between each tool use** about what you've learned and what to explore next

### Important
- DO NOT rush to implementation details
- Focus on the WHY behind decisions
- Look for moments where approaches change or evolve
- Pay attention to user corrections or redirections
- Note any philosophical or methodological discussions

### Process
1. Begin with a timeline scan to orient yourself
2. Think about what patterns you observe
3. Systematically explore interesting conversation threads
4. Build up a complete picture of the design thinking in this session
```

## Results Comparison

### Surface-Level Results (First Attempt)
- Found 40 matches for "conversation mode"
- Listed commands executed
- Provided match counts

### Deep Understanding (Second Attempt)
- Discovered the meta-problem of building a tool to overcome its own limitations
- Revealed naming philosophy with multiple layers of meaning
- Captured methodological commitments (scientific approach, YAGNI)
- Understood architectural boundaries and design principles
- Synthesized evolution of thinking throughout session

## Lessons Learned

1. **Less guidance often yields better results** - Over-specification leads to mechanical execution
2. **Thinking prompts matter** - Explicitly asking for reflection between steps improves quality
3. **Context beats search** - Understanding flow and evolution is more valuable than finding specific terms
4. **Synthesis emerges from exploration** - Let the agent discover patterns rather than prescribing them

## Application

This pattern is particularly valuable for:
- Recovering context after compaction events
- Understanding design evolution in long sessions
- Extracting philosophical/methodological insights
- Building comprehensive understanding of complex discussions