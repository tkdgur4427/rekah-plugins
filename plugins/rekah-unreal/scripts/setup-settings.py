#!/usr/bin/env python3
"""
Setup Claude Code settings for rekah-unreal plugin.
Merges plugin settings into existing .claude/settings.json without overwriting.
"""

import json
import os
import sys
from pathlib import Path


def merge_settings(project_dir: str) -> bool:
    """
    Merge rekah-unreal plugin settings into .claude/settings.json.

    Args:
        project_dir: The project directory path

    Returns:
        True if successful, False otherwise
    """
    claude_dir = Path(project_dir) / ".claude"
    settings_file = claude_dir / "settings.json"

    # Plugin settings to add
    plugin_settings = {
        "rekah-unreal@rekah-plugins": True
    }

    try:
        # Ensure .claude directory exists
        claude_dir.mkdir(parents=True, exist_ok=True)

        # Load existing settings or create new
        if settings_file.exists():
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
            print(f"[rekah-unreal] Loaded existing settings.json")
        else:
            settings = {}
            print(f"[rekah-unreal] Creating new settings.json")

        # Ensure enabledPlugins section exists
        if "enabledPlugins" not in settings:
            settings["enabledPlugins"] = {}

        # Merge plugin settings (only add if not already set)
        updated = False
        for plugin, enabled in plugin_settings.items():
            if plugin not in settings["enabledPlugins"]:
                settings["enabledPlugins"][plugin] = enabled
                print(f"[rekah-unreal] Added plugin: {plugin} = {enabled}")
                updated = True
            else:
                print(f"[rekah-unreal] Plugin already configured: {plugin}")

        # Save if updated
        if updated:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            print(f"[rekah-unreal] Settings saved to {settings_file}")
        else:
            print(f"[rekah-unreal] No changes needed")

        return True

    except Exception as e:
        print(f"[rekah-unreal] Error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Get project directory from environment or argument
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")

    if not project_dir and len(sys.argv) > 1:
        project_dir = sys.argv[1]

    if not project_dir:
        print("[rekah-unreal] Error: CLAUDE_PROJECT_DIR not set", file=sys.stderr)
        sys.exit(1)

    print(f"[rekah-unreal] Project directory: {project_dir}")

    success = merge_settings(project_dir)
    sys.exit(0 if success else 1)
