# Session Reviewer

A Claude Code skill that exports conversations to Markdown and HTML formats for sharing, archiving, or review.

## Features

- **Dual output**: Generates both Markdown and HTML from a single JSON data source
- **Self-contained HTML**: Works offline with `file://` protocol (no external dependencies)
- **Sidebar navigation**: HTML includes searchable message list with filters
- **Tool visibility**: Shows all tool uses with inputs and outputs
- **Collapsible sections**: Tool outputs can be expanded/collapsed in HTML view

## Installation

Copy the skill files to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/share-session
cp SKILL.md export.py template.html ~/.claude/skills/share-session/
```

Or run:

```bash
./install.sh
```

## Usage

After installation, restart Claude Code and run:

```bash
# Export with automatic naming (timestamp-based)
/share-session

# Export with custom session name
/share-session auth-refactor

# Export to custom path (bypasses default location)
/share-session ./custom/path
```

### Output Location

The skill automatically determines where to save sessions:

1. If `docs/` directory exists → `docs/sessions/<name>/`
2. Otherwise → `sessions/<name>/`

Each session gets its own subdirectory containing:
- `session.json` - Session data (intermediate format)
- `session.md` - Markdown export
- `session.html` - HTML export with sidebar UI

Example output structure:
```
docs/sessions/2024-01-29-1430/
  session.json
  session.md
  session.html
```

## How It Works

1. **Location**: Checks for `docs/` directory to determine output path
2. **Reconstruction**: Claude reconstructs the conversation from memory into structured JSON
3. **Export**: The `export.py` script converts the JSON to both Markdown and HTML
4. **Organization**: Each session gets its own subdirectory with all three files

```
┌─────────────────┐     ┌─────────────────────────────────┐
│ Claude recalls  │ ──▶ │ sessions/2024-01-29-1430/       │
│ conversation    │     │   session.json                  │
│                 │     │   session.md                    │
│                 │     │   session.html                  │
└─────────────────┘     └─────────────────────────────────┘
```

## File Structure

```
session-reviewer/
├── README.md           # This file
├── PLAN.md             # Original planning document
├── SKILL.md            # Skill instructions for Claude
├── export.py           # Python script to generate outputs
├── template.html       # HTML template with sidebar UI
└── install.sh          # Installation script
```

Installed skill location:
```
~/.claude/skills/share-session/
├── SKILL.md
├── export.py
└── template.html
```

Exported sessions (in your project repo):
```
docs/sessions/              # or sessions/ if no docs/ exists
├── 2024-01-29-1430/
│   ├── session.json
│   ├── session.md
│   └── session.html
├── 2024-01-30-auth-refactor/
│   ├── session.json
│   ├── session.md
│   └── session.html
└── ...
```

## Data Format

The JSON structure used by both exports:

```json
{
  "metadata": {
    "exportedAt": "2025-01-27T15:00:00",
    "workingDirectory": "/path/to/project"
  },
  "messages": [
    {
      "role": "user",
      "content": "User message text"
    },
    {
      "role": "assistant",
      "content": "Simple text response"
    },
    {
      "role": "assistant",
      "content": [
        {"type": "text", "text": "Response with tools"},
        {
          "type": "tool_use",
          "name": "Bash",
          "input": {"command": "ls -la"},
          "output": "file1.txt\nfile2.txt"
        }
      ]
    }
  ]
}
```

## Manual Export

You can also run the export script directly:

```bash
# Generate from existing JSON
python3 export.py session-data.json output-name

# This creates:
# - output-name.md
# - output-name.html
```

## HTML Features

The HTML export includes:

- **Sidebar**: Lists all messages with role icons and preview text
- **Search**: Filter messages by text content
- **Filters**: Show All, User only, Assistant only, or messages with Tools
- **Collapsible tools**: Click tool headers to expand/collapse output
- **Dark theme**: Easy on the eyes
- **Responsive**: Works on mobile devices

## Limitations

- **Context reconstruction**: Long conversations may have incomplete early history if they exceed Claude's context window
- **No images**: Image content is noted but not embedded
- **Manual trigger**: Skill must be invoked explicitly (`/share-session`)

## Background

This skill was inspired by the `/share` command in [pi-mono/coding-agent](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent), which exports sessions to HTML and uploads to GitHub Gist.

The key differences:
- This skill works with Claude Code (different product)
- Uses "context reconstruction" approach (Claude recalls the conversation)
- Outputs both Markdown and HTML
- No gist upload (yet) - files are local

## Future Enhancements

- [ ] `--gist` flag to upload HTML to GitHub Gist
- [ ] `--redact` flag to prompt for sensitive content review
- [ ] `--since N` flag to export only last N messages
- [ ] Light theme option for HTML

## Acknowledgments

This project builds on the work of others:

- **[Ben Tossell](https://github.com/bentossell/share-session)** - For demonstrating how to extract content from other repos, like the /share command, via this [YouTube video](https://www.youtube.com/live/5YBjll9XJlw?si=uEhRuA4GtrZTiSOA) (around 34:00)
- **[Mario Zechner (badlogic)](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent)** - The original `/share` command implementation in pi-mono/coding-agent that inspired this skill's approach to session export

## License

MIT
