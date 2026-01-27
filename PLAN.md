# Session Reviewer - /share-session Skill Plan

## Goal
Create a `/share-session` skill for Claude Code that exports the current conversation to a Markdown file.

## Why Markdown?

- **Simple**: No templates, CSS, JavaScript, or vendor libraries needed
- **Native format**: Conversation content is already markdown
- **Portable**: Viewable in GitHub, VS Code, Obsidian, any text editor
- **Editable**: Easy to modify, annotate, or redact before sharing
- **Version controllable**: Works great with git
- **Convertible**: Can always render to HTML/PDF later with existing tools (Pandoc, etc.)

## Research Summary

### Claude Code Skills System
- Skills are markdown files with YAML frontmatter stored in:
  - `~/.claude/skills/<name>/SKILL.md` (personal)
  - `.claude/skills/<name>/SKILL.md` (project)
- Skills have access to all Claude Code tools: Read, Write, Edit, Bash, Glob, Grep, etc.
- Can use `allowed-tools` to restrict permissions
- Arguments available via `$ARGUMENTS` placeholder
- Session ID available via `${CLAUDE_SESSION_ID}`

## Approach: Context Reconstruction

Have Claude reconstruct the conversation from its current context and format as Markdown.

**Pros**:
- Works without accessing undocumented internal files
- Works immediately with the skill system
- Simple implementation

**Cons**:
- May be incomplete if conversation exceeds context window
- Relies on Claude's recall of the conversation

## Implementation Plan

### Skill Structure
```
session-reviewer/
├── SKILL.md                 # Main skill file with instructions
└── PLAN.md                  # This file
```

That's it. No templates, no vendor files.

### SKILL.md Design
```yaml
---
name: share-session
description: Export the current conversation to a Markdown file
disable-model-invocation: true
allowed-tools: Write
argument-hint: [output-path]
---
```

The skill will instruct Claude to:
1. Reconstruct the conversation from memory
2. Format each message appropriately
3. Write to the specified path (default: `./session-export.md`)

### Output Format

```markdown
# Session Export

**Exported**: 2024-01-27 10:30:00
**Working Directory**: /path/to/project

---

## User

[User's message content]

---

## Assistant

[Assistant's response]

### Tool Use: Read

**File**: `/path/to/file.ts`

\`\`\`typescript
[file contents]
\`\`\`

### Tool Use: Bash

**Command**: `npm test`

\`\`\`
[output]
\`\`\`

---

## User

[Next user message...]

---
```

### Formatting Rules

| Content Type | Markdown Format |
|--------------|-----------------|
| User message | `## User` heading + content |
| Assistant text | `## Assistant` heading + content |
| Tool call | `### Tool Use: {name}` subheading |
| Tool input | Parameters in bold or code block |
| Tool output | Fenced code block with language hint |
| Code in messages | Preserve existing fenced blocks |
| Images | `![image](path)` or note that image was shown |

## Open Questions

1. **Context limitations**: How much can Claude accurately recall?
   - Long conversations may be compacted/summarized
   - Should warn users about potential incompleteness

2. **Tool output verbosity**: Include full output or summarize?
   - Large file reads could bloat the export
   - Option: truncate with `[... N more lines]`

3. **Sensitive content**: How to handle?
   - API keys, passwords in tool outputs
   - Option: add `--redact` flag for manual review prompts

4. **Images**: How to reference?
   - Include path as markdown image syntax
   - Note: won't render if path is temporary

## Next Steps

1. [x] Create plan document
2. [ ] Create SKILL.md with detailed instructions
3. [ ] Test with current conversation
4. [ ] Iterate on output format
5. [ ] Add optional gist upload feature
6. [ ] Document usage

## Future Enhancements

- `--gist` flag: Upload to GitHub gist and return URL
- `--redact` flag: Prompt for review of sensitive content
- `--since N` flag: Export only last N messages
- `--format html` flag: Convert markdown to self-contained HTML
