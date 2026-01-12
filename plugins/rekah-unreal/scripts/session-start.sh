#!/bin/bash
# SessionStart Hook for rekah-unreal plugin
# This script runs when a Claude Code session starts

echo "[rekah-unreal] SessionStart hook triggered"
echo "[rekah-unreal] Plugin root: ${CLAUDE_PLUGIN_ROOT}"
echo "[rekah-unreal] Project dir: ${CLAUDE_PROJECT_DIR}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Setup project using Python (settings.json, environment checks)
if command -v python3 &> /dev/null; then
    python3 "${SCRIPT_DIR}/setup-project.py"
elif command -v python &> /dev/null; then
    python "${SCRIPT_DIR}/setup-project.py"
else
    echo "[rekah-unreal] Warning: Python not found, skipping project setup"
fi

# Check if this is an Unreal Engine project
if [ -f "*.uproject" ] || [ -d "Engine" ]; then
    echo "[rekah-unreal] Unreal Engine project detected"
fi

# Check for compile_commands.json
if [ -f "compile_commands.json" ]; then
    echo "[rekah-unreal] compile_commands.json found"
else
    echo "[rekah-unreal] compile_commands.json NOT found - LSP may not work properly"
fi

exit 0
