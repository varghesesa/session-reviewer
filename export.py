#!/usr/bin/env python3
"""
Export session data to both Markdown and HTML formats.
Usage: python export.py [session-data.json] [output-base-name]
"""

import json
import base64
import sys
from pathlib import Path
from datetime import datetime

def load_session(path: str) -> dict:
    """Load session data from JSON file."""
    with open(path, 'r') as f:
        return json.load(f)

def format_tool_use_md(tool: dict) -> str:
    """Format a tool use block for Markdown."""
    lines = [f"\n### Tool Use: {tool.get('name', 'Unknown')}\n"]

    # Format input parameters
    input_data = tool.get('input', {})
    if isinstance(input_data, dict):
        for key, value in input_data.items():
            if isinstance(value, str) and len(value) > 100:
                lines.append(f"**{key}**:\n```\n{value[:100]}...\n```\n")
            else:
                lines.append(f"**{key}**: `{value}`\n")

    # Format output
    output = tool.get('output', '')
    if output:
        # Try to detect language for syntax highlighting
        lang = 'text'
        if 'function' in output or 'const ' in output or 'import ' in output:
            lang = 'typescript'
        elif output.strip().startswith('{') or output.strip().startswith('['):
            lang = 'json'

        # Truncate very long outputs
        if len(output) > 2000:
            output = output[:1500] + f"\n\n[... truncated, {len(output) - 1500} more chars]"

        lines.append(f"\n```{lang}\n{output}\n```\n")

    return ''.join(lines)

def format_message_content_md(content) -> str:
    """Format message content for Markdown."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if block.get('type') == 'text':
                parts.append(block.get('text', ''))
            elif block.get('type') == 'tool_use':
                parts.append(format_tool_use_md(block))
        return '\n'.join(parts)

    return str(content)

def generate_markdown(session: dict) -> str:
    """Generate Markdown from session data."""
    lines = ["# Session Export\n"]

    # Metadata
    metadata = session.get('metadata', {})
    lines.append(f"**Exported**: {metadata.get('exportedAt', datetime.now().isoformat())}")
    lines.append(f"**Working Directory**: {metadata.get('workingDirectory', 'Unknown')}\n")
    lines.append("---\n")

    # Messages
    for msg in session.get('messages', []):
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')

        # Role header
        lines.append(f"## {role.capitalize()}\n")

        # Content
        lines.append(format_message_content_md(content))
        lines.append("\n---\n")

    return '\n'.join(lines)

def generate_html(session: dict, template_path: str) -> str:
    """Generate HTML from session data using template."""
    # Read template
    with open(template_path, 'r') as f:
        template = f.read()

    # Encode session data as base64
    session_b64 = base64.b64encode(json.dumps(session).encode()).decode()

    # Replace placeholder
    html = template.replace('{{SESSION_DATA}}', session_b64)

    return html

def main():
    # Parse arguments
    if len(sys.argv) < 2:
        session_path = Path(__file__).parent / 'session-data.json'
    else:
        session_path = Path(sys.argv[1])

    if len(sys.argv) < 3:
        output_base = Path(__file__).parent / 'session-export'
    else:
        output_base = Path(sys.argv[2])

    template_path = Path(__file__).parent / 'template.html'

    # Load session
    print(f"Loading session from: {session_path}")
    session = load_session(session_path)
    print(f"Loaded {len(session.get('messages', []))} messages")

    # Generate Markdown
    md_output = output_base.with_suffix('.md')
    markdown = generate_markdown(session)
    with open(md_output, 'w') as f:
        f.write(markdown)
    print(f"Written: {md_output}")

    # Generate HTML
    if template_path.exists():
        html_output = output_base.with_suffix('.html')
        html = generate_html(session, template_path)
        with open(html_output, 'w') as f:
            f.write(html)
        print(f"Written: {html_output}")
    else:
        print(f"Template not found: {template_path}")

    print("Done!")

if __name__ == '__main__':
    main()
