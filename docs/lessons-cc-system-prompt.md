# Reverse Engineering Anthropic's Claude Code System Prompt

## Executive Summary

This document systematically analyzes Claude Code's system prompt to extract Anthropic's proven prompt engineering techniques through reverse engineering. By focusing exclusively on Anthropic-authored content (excluding project-specific CLAUDE.md instructions), we identify counterintuitive practices that can improve AI guidance systems.

## Methodology

Analysis was conducted by examining the Anthropic-authored portions of Claude Code's system prompt across four dimensions:
1. **Structural Patterns** - Organization and information architecture
2. **Tone & Style** - Voice, authority, and communication techniques
3. **Repetition Strategies** - Reinforcement and strategic placement
4. **Linguistic Engineering** - Keywords, formatting, and cognitive triggers

## Key Findings: Counterintuitive Practices

### 1. **Constraint as Empowerment**
**Discovery**: Anthropic uses extensive negative commands (NEVER/ALWAYS) not to restrict, but to create confident operational frameworks.

**Evidence**:
- "NEVER create files unless absolutely necessary" appears 4 times in different contexts
- "ALWAYS prefer editing existing files" provides clear decision logic
- Absolute constraints reduce decision paralysis by eliminating options

**Implementation**: Replace vague suggestions ("consider," "you might") with definitive boundaries ("NEVER," "ALWAYS," "MUST").

### 2. **Strategic Redundancy Over Efficiency**
**Discovery**: Critical instructions are intentionally repeated across multiple contexts with variations.

**Evidence**:
- File creation constraints appear in tool descriptions, workflow sections, and summary reminders
- Each repetition adds contextual nuance rather than verbatim copying
- Spaced repetition prevents rule forgetting during complex tasks

**Implementation**: Identify your 3 most critical rules and embed them in at least 3 different sections with contextual variations.

### 3. **Identity-First Architecture**
**Discovery**: Role definition precedes all other instructions and is reinforced throughout.

**Evidence**:
- "You are Claude Code, Anthropic's official CLI for Claude" opens the prompt
- Identity statements are repeated in different forms across sections
- Role clarity reduces interpretation uncertainty

**Implementation**: Begin prompts with definitive identity statements using "You are [X]" rather than "Your role is to..."

### 4. **Graduated Emphasis Hierarchy**
**Discovery**: Visual formatting creates information priority layers beyond simple headers.

**Evidence**:
- ALL CAPS reserved for absolute constraints
- **Bold** for important but flexible guidelines  
- `Backticks` for technical precision
- Examples anchor abstract concepts

**Implementation**: Establish consistent formatting hierarchy: CAPS → Bold → Backticks → Examples.

## Structural Analysis

### Hierarchical Information Architecture

Anthropic organizes Claude Code's prompt in a "Cone of Specificity":
```
Identity Definition
    ↓
Core Guidelines & Constraints
    ↓
Workflow Instructions
    ↓
Tool Usage Policies
    ↓
Environmental Context
```

**Key Insight**: This structure mirrors how humans need information - broad context first, specific implementation details last.

### XML-Style Semantic Boundaries
While not using literal XML tags, Anthropic creates clear semantic sections that function like containers:
- Each section has a distinct purpose and scope
- Instructions are grouped by operational context
- Related concepts are co-located for cognitive efficiency

## Tone & Style Patterns

### Authority Through Precision
**Pattern**: Direct imperatives without hedging language
- ✓ "Use this tool when you need to search"
- ✗ "You might want to consider using this tool"

### Second Person Ownership
**Pattern**: Exclusive use of "you" creates immediate accountability
- ✓ "When you complete the task"
- ✗ "When the task is completed"

### Active Voice Dominance
**Pattern**: Instructions focus on actions, not abstract states
- ✓ "Check that all required parameters are provided"
- ✗ "All required parameters should be checked"

## Repetition & Reinforcement Strategies

### Contextual Embedding
Critical rules appear in multiple relevant sections rather than a single "rules" list:
- File creation constraints in tool descriptions AND workflow sections
- Authority reinforcement in identity AND capability sections
- Security guidelines in relevant operational contexts

### Escalation Patterns
Instructions build intensity through repetition:
1. Initial guideline: "Prefer editing existing files"
2. Stronger constraint: "ALWAYS prefer editing"  
3. Absolute prohibition: "NEVER create files unless absolutely necessary"

### Strategic Spacing
Repetitions are separated by other content to avoid redundancy perception while maintaining reinforcement effectiveness.

## Linguistic Engineering

### Power Keyword Usage
**NEVER/ALWAYS/MUST**: Reserved for non-negotiable constraints (used 12+ times)
**IMPORTANT**: Cognitive interrupt for critical exceptions (used 8+ times)
**DO NOT**: Secondary prohibition level (used 15+ times)

### Behavioral Trigger Phrases
- "When X, do Y" - Creates conditional behavioral patterns
- "Before/After" - Establishes procedural checkpoints  
- "You have the capability to" - Enables confident action

### Technical Precision
- Specific tool names: `ripgrep` not "text search"
- Exact parameters: `120000ms` not "a couple minutes"
- Precise conditions: "file paths that contain spaces" not "problematic paths"

## Framework for Evaluating CLAUDE.md

### Assessment Checklist

**Structural Quality**:
- [ ] Does identity definition appear first?
- [ ] Are related concepts grouped together?
- [ ] Is information organized by specificity (broad → detailed)?
- [ ] Are sections clearly bounded with semantic containers?

**Authority & Clarity**:
- [ ] Are commands phrased as imperatives rather than suggestions?
- [ ] Is second person ("you") used consistently for accountability?
- [ ] Are critical constraints expressed as NEVER/ALWAYS statements?
- [ ] Is technical language precise and unambiguous?

**Reinforcement Effectiveness**:
- [ ] Are the 3 most critical rules repeated across multiple contexts?
- [ ] Do repetitions add contextual value rather than verbatim copying?
- [ ] Are absolute constraints visually emphasized (CAPS, bold)?
- [ ] Are behavioral triggers clearly established ("When X, do Y")?

**Cognitive Load Management**:
- [ ] Is formatting hierarchy consistent throughout?
- [ ] Are complex concepts supported with concrete examples?
- [ ] Are decision trees clear and unambiguous?
- [ ] Is information scannable with visual anchors?

### Improvement Priorities (80/20 Rule)

**High Impact, Low Effort**:
1. Add definitive identity statement at the beginning
2. Convert 3 most important suggestions to NEVER/ALWAYS statements
3. Add concrete examples after abstract concepts
4. Establish consistent formatting hierarchy

**Medium Impact, Medium Effort**:
1. Reorganize content by specificity (broad → detailed)
2. Embed critical rules across multiple relevant sections
3. Replace hedging language with direct imperatives
4. Add behavioral trigger phrases ("When X, do Y")

## Implementation Templates

### Identity Statement Pattern
```
You are [Role], [Organization/Context]'s [Specific Function].
You are [Operational Description] that helps users with [Primary Capability].
```

### Constraint Establishment Pattern
```
IMPORTANT: [Context-setting statement about boundaries/safety]

NEVER [absolute prohibition with brief rationale]
ALWAYS [mandatory behavior with brief rationale]  
MUST [non-negotiable requirement with brief rationale]
```

### Contextual Reinforcement Pattern
```
[Section Title]
[Specific instructions for this context]
[Critical rule restated in this context]
[Example or concrete application]
```

### Behavioral Trigger Pattern
```
When [specific condition]:
- [Required action 1]
- [Required action 2]
- [Example or clarification]
```

## Next Steps

1. **Apply Assessment Checklist** to current CLAUDE.md
2. **Implement High-Impact Changes** using templates above
3. **Test Behavioral Compliance** through iterative prompt testing
4. **Measure Effectiveness** through task completion quality
5. **Iterate Based on Results** using systematic refinement

---

*Analysis conducted through systematic reverse engineering of Anthropic's Claude Code system prompt, focusing exclusively on techniques developed by Anthropic rather than project-specific content.*