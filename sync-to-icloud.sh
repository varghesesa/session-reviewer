#!/bin/bash
# Sync exports to iCloud Drive for private backup
# This script is called automatically after /share-session or can be run manually

ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/code-exports/session-reviewer"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXPORTS_DIR="$SCRIPT_DIR/exports"

# Ensure iCloud directory exists
mkdir -p "$ICLOUD_DIR"

# Check if exports directory exists
if [ ! -d "$EXPORTS_DIR" ]; then
    echo "No exports directory found at $EXPORTS_DIR"
    exit 0
fi

# Sync using rsync (preserves structure, only copies changes)
rsync -av --delete "$EXPORTS_DIR/" "$ICLOUD_DIR/exports/"

echo "Synced to iCloud: $ICLOUD_DIR/exports/"
