# How session.json is Generated

The `/share-session` skill uses **context reconstruction** to create the `session.json` file. This document explains how it works and its limitations.

## How It Works

When you run `/share-session`, Claude reconstructs the conversation from its context window:

1. Claude "looks back" at the conversation history available in the current context
2. Claude can see: user messages, assistant responses, tool calls, and tool outputs
3. Claude manually writes this out as structured JSON

```
┌─────────────────────────────────┐
│     Claude's Context Window     │
│                                 │
│  User: "Fix the auth bug"       │
│  Assistant: "I'll check..."     │
│  Tool: Read auth.ts → [output]  │
│  Assistant: "Found the issue"   │
│  User: "Great, fix it"          │
│  ...                            │
└─────────────────────────────────┘
            │
            ▼ Claude reconstructs
┌─────────────────────────────────┐
│         session.json            │
│  {                              │
│    "messages": [                │
│      {"role": "user", ...},     │
│      {"role": "assistant", ...} │
│    ]                            │
│  }                              │
└─────────────────────────────────┘
```

## Why This Approach?

Three approaches were considered during the original planning:

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **A: Session Files** | Read Claude Code's internal session files | Accurate, complete | Undocumented format, may change |
| **B: Context Reconstruction** | Claude recalls conversation from memory | Works immediately, no dependencies | May be incomplete for long conversations |
| **C: MCP Server** | Build proper integration | Clean API, robust | Complex to implement |

**Approach B was chosen** for simplicity - it works immediately without needing to reverse-engineer Claude Code's internal storage format.

## Limitations

### 1. Context Window Limits

Claude has a finite context window. For very long conversations:
- Early messages may be summarized or compressed
- Some details from the beginning may be lost
- The skill notes this in metadata when it occurs

### 2. Not a True Export

This is reconstruction from memory, not reading from a file:
- Small inaccuracies are possible
- Tool output formatting may differ slightly from original
- Timestamps are approximate (export time, not original message time)

### 3. Truncation

- Tool outputs longer than ~2000 characters are truncated
- This may already have happened in Claude's context
- The JSON reflects whatever Claude can currently see

## Alternatives Considered

### Reading Session Files Directly

Claude Code stores sessions somewhere locally, but:
- The format is undocumented
- It could change between versions
- Would require discovering and parsing internal files

This could be revisited if Anthropic documents the session format.

### MCP Server Integration

A Model Context Protocol server could provide:
- Clean API for session data
- Proper timestamps
- Complete history regardless of context limits

This would be more robust but requires significant implementation effort.

## When Context Reconstruction Works Well

- Sessions under ~50 messages
- Recent conversations (same session)
- When approximate reconstruction is acceptable

## When to Consider Alternatives

- Very long planning sessions (100+ messages)
- Need for exact timestamps
- Legal/compliance requirements for accuracy
