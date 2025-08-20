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

**Psychology**: Paradoxically, strict boundaries create freedom by eliminating decision overhead and reducing cognitive load.

**Implementation**: Replace vague suggestions ("consider," "you might") with definitive boundaries ("NEVER," "ALWAYS," "MUST").

### 2. **Strategic Redundancy Over Efficiency**
**Discovery**: Critical instructions are intentionally repeated across multiple contexts with variations.

**Evidence**:
- File creation constraints appear in tool descriptions, workflow sections, and summary reminders
- Each repetition adds contextual nuance rather than verbatim copying
- Spaced repetition prevents rule forgetting during complex tasks

**Psychology**: Leverages the spacing effect from cognitive science - information is better retained when encountered multiple times across different contexts.

**Implementation**: Identify your 3 most critical rules and embed them in at least 3 different sections with contextual variations.

### 3. **Identity-First Architecture** 
**Discovery**: Role definition precedes all other instructions and is reinforced throughout.

**Evidence**:
- "You are Claude Code, Anthropic's official CLI for Claude" opens the prompt
- Identity statements are repeated in different forms across sections
- Role clarity reduces interpretation uncertainty

**Psychology**: Exploits commitment/consistency bias - once an identity is established, actions align with that identity automatically.

**Implementation**: Begin prompts with definitive identity statements using "You are [X]" rather than "Your role is to..."

### 4. **Graduated Emphasis Hierarchy**
**Discovery**: Visual formatting creates information priority layers beyond simple headers.

**Evidence**:
- ALL CAPS reserved for absolute constraints
- **Bold** for important but flexible guidelines  
- `Backticks` for technical precision
- Examples anchor abstract concepts

**Psychology**: Creates visual attention hierarchy that guides information processing and recall priority.

**Implementation**: Establish consistent formatting hierarchy: CAPS → Bold → Backticks → Examples.

### 5. **Decision Architecture Design**
**Discovery**: Complex choices are pre-structured through conditional logic patterns.

**Evidence**:
- "When X, do Y" patterns eliminate decision-making overhead
- "Before executing, follow these steps" creates procedural checkpoints
- "If given a GitHub URL, use the gh command" provides clear decision trees

**Psychology**: Reduces cognitive load by converting complex decisions into simple pattern matching.

**Implementation**: Structure complex guidance as conditional trees rather than general principles.

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

## Practical Application Guide

### Immediate Improvements for CLAUDE.md

**Current Pattern**: 
```
## Core Programming Philosophy
- Code is a liability, not an asset - Minimize implementation
```

**Anthropic Pattern**:
```
NEVER create unnecessary code - Every line must justify its existence
ALWAYS minimize implementation while maximizing value  
MUST prioritize working software over comprehensive documentation
```

**Current Pattern**:
```
- Begin each feature with a requirements dialogue
- Structure the dialogue to establish goals...
```

**Anthropic Pattern**:
```
When starting any feature:
1. Define precise acceptance criteria BEFORE writing code
2. Document edge cases and expected behaviors  
3. Create failing tests that specify the behavior
4. Implement minimal code to pass the tests
```

### Copy-Paste Ready Templates

**Identity Reinforcement** (place at document start):
```
You are a BookMinder Developer, following disciplined engineering practices.
You are committed to test-driven development and scientific validation of all changes.
```

**Critical Constraint Pattern**:
```
NEVER implement features without corresponding tests
ALWAYS write failing tests before implementation code  
MUST maintain test coverage above 90% for all new code
```

**Decision Tree Pattern**:
```
When implementing new functionality:
- If the feature affects core business logic → Write acceptance test first
- If the feature is UI-only → Write integration test first  
- If the feature is utility/helper → Write unit test first
```

### Language Pattern Upgrades

| Weak Pattern | Strong Pattern |
|--------------|----------------|
| "You should consider..." | "ALWAYS..." |
| "It's recommended to..." | "MUST..." |
| "Try to avoid..." | "NEVER..." |
| "You might want to..." | "When X, do Y:" |
| "Please remember..." | "Before X, verify Y:" |

## Compliance Measurement

### Weekly Assessment Questions

1. Are new developers following constraints without reminder?
2. Do team members cite specific patterns from guidance?
3. Are decision trees being used instead of asking for clarification?
4. Is identity language ("we are X") appearing in team communications?
5. Are critical rules being referenced during code reviews?

### Success Indicators

**High Compliance (80%+)**:
- Developers automatically write tests first
- Code reviews reference specific CLAUDE.md patterns  
- Decision-making follows documented conditional logic
- New team members adopt practices within 1 week

**Medium Compliance (60-80%)**:
- Most practices followed with occasional reminders
- Some decision trees used, some questions still asked
- Identity alignment emerging in team language

**Low Compliance (<60%)**:
- Frequent clarification requests on documented processes
- Inconsistent practice adoption
- Rules treated as suggestions rather than constraints

## Next Steps

1. **Apply Assessment Checklist** to current CLAUDE.md
2. **Implement Copy-Paste Templates** from above section
3. **Test Language Pattern Upgrades** with team members
4. **Measure Compliance** using weekly assessment questions
5. **Iterate Based on Results** using systematic refinement

---

*Analysis conducted through systematic reverse engineering of Anthropic's Claude Code system prompt, focusing exclusively on techniques developed by Anthropic rather than project-specific content.*