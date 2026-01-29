---
name: share-session
description: Export the current conversation to Markdown and HTML files for sharing or archiving
disable-model-invocation: true
allowed-tools: Write, Bash
argument-hint: [output-path]
---

# Export Session to Markdown and HTML

Export this conversation to both Markdown and HTML formats using a shared JSON data structure.

## Output Paths

Base path from arguments: `$ARGUMENTS`

### Default Location (no arguments provided)

1. Check if `docs/` directory exists in the current repo
2. If yes: use `docs/sessions/<timestamp>/`
3. If no: use `sessions/<timestamp>/`

Timestamp format: `YYYY-MM-DD-HHMM` (e.g., `2024-01-29-1430`)

### With Arguments

If the user provides a path, use it as the session directory name:
- `/share-session auth-refactor` → `docs/sessions/auth-refactor/` or `sessions/auth-refactor/`
- `/share-session ./custom/path` → `./custom/path/` (absolute paths bypass the default location logic)

### Files Created

Within the session directory:
- `session.json` - Session data (intermediate)
- `session.md` - Markdown version
- `session.html` - HTML version with sidebar navigation

Example structure:
```
docs/sessions/2024-01-29-1430/
  session.json
  session.md
  session.html
```

## Step 1: Reconstruct Conversation to JSON

Create a JSON file with this structure:

```json
{
  "metadata": {
    "exportedAt": "[current date/time]",
    "workingDirectory": "[current working directory]"
  },
  "messages": [
    {
      "role": "user",
      "content": "User's message text"
    },
    {
      "role": "assistant",
      "content": "Simple text response"
    },
    {
      "role": "assistant",
      "content": [
        {"type": "text", "text": "Response with tool uses"},
        {
          "type": "tool_use",
          "name": "ToolName",
          "input": {"param": "value"},
          "output": "Tool output text"
        },
        {"type": "text", "text": "More response text"}
      ]
    }
  ]
}
```

### Content Rules

- **User messages**: Always a string
- **Assistant messages**: String for text-only, array for responses with tool uses
- **Tool uses**: Include name, input parameters, and output
- **Large outputs**: Truncate to ~2000 chars with `[... truncated]`
- **Sensitive data**: Replace API keys/passwords with `[REDACTED]`

## Step 2: Generate Exports

After writing the JSON file, run the export script:

```bash
python3 ~/.claude/skills/share-session/export.py "{base}.json" "{base}"
```

This generates both `.md` and `.html` files from the JSON.

## Step 3: Report Results

Tell the user:
- Paths to all created files
- Number of messages exported
- Any warnings (truncated content, redacted secrets, incomplete recall)

## Example Workflow

```bash
# User runs: /share-session (no arguments, docs/ exists)

# 1. Determine output directory
mkdir -p docs/sessions/2024-01-29-1430

# 2. Write JSON
Write "docs/sessions/2024-01-29-1430/session.json" with reconstructed conversation

# 3. Run export script
python3 ~/.claude/skills/share-session/export.py "docs/sessions/2024-01-29-1430/session.json" "docs/sessions/2024-01-29-1430/session"

# 4. Report
Created:
- docs/sessions/2024-01-29-1430/session.json (session data)
- docs/sessions/2024-01-29-1430/session.md (Markdown)
- docs/sessions/2024-01-29-1430/session.html (HTML with sidebar)
```

```bash
# User runs: /share-session auth-refactor (named session, no docs/ directory)

# 1. Determine output directory
mkdir -p sessions/auth-refactor

# 2. Write JSON
Write "sessions/auth-refactor/session.json" with reconstructed conversation

# 3. Run export script
python3 ~/.claude/skills/share-session/export.py "sessions/auth-refactor/session.json" "sessions/auth-refactor/session"

# 4. Report
Created:
- sessions/auth-refactor/session.json
- sessions/auth-refactor/session.md
- sessions/auth-refactor/session.html
```

## Important Notes

- Reconstruct the ENTIRE conversation from the beginning
- Include ALL messages and tool uses
- If conversation is very long and early parts are unclear, note this in metadata
- The HTML file is self-contained and works offline (file:// protocol)
