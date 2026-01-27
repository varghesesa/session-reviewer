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

If no path is provided, use `./session-export` as the base name.

This will create:
- `{base}.json` - Session data (intermediate)
- `{base}.md` - Markdown version
- `{base}.html` - HTML version with sidebar navigation

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
# User runs: /share-session ./exports/my-session

# 1. Write JSON
Write "./exports/my-session.json" with reconstructed conversation

# 2. Run export script
python3 ~/.claude/skills/share-session/export.py "./exports/my-session.json" "./exports/my-session"

# 3. Report
Created:
- ./exports/my-session.json (session data)
- ./exports/my-session.md (Markdown)
- ./exports/my-session.html (HTML with sidebar)
```

## Important Notes

- Reconstruct the ENTIRE conversation from the beginning
- Include ALL messages and tool uses
- If conversation is very long and early parts are unclear, note this in metadata
- The HTML file is self-contained and works offline (file:// protocol)
