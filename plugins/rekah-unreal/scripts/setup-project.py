#!/usr/bin/env python3
"""
Setup Claude Code project settings for rekah-unreal plugin.
Extends setup-settings.py with LSP configuration and environment checks.
"""

import json
import os
import subprocess
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
        "rekah-unreal@rekah-plugins": True,
        "clangd-lsp@claude-plugins-official": True  # LSP support for C++
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


def setup_lsp_config(project_dir: str) -> bool:
    """
    Create .lsp.json file for clangd LSP configuration.

    Args:
        project_dir: The project directory path

    Returns:
        True if successful, False otherwise
    """
    lsp_file = Path(project_dir) / ".lsp.json"

    # LSP configuration template
    lsp_config = {
        "clangd": {
            "command": "clangd",
            "args": [
                "--log=verbose",
                "--pretty",
                "--background-index",
                f"--compile-commands-dir={project_dir}",
                "-j=2",
                "--background-index-priority=background"
            ],
            "extensionToLanguage": {
                ".cpp": "cpp",
                ".cc": "cpp",
                ".h": "cpp",
                ".hpp": "cpp",
                ".inl": "cpp"
            },
            "startupTimeout": 10000,
            "restartOnCrash": True,
            "maxRestarts": 3
        }
    }

    try:
        # Only create if not exists (preserve existing config)
        if lsp_file.exists():
            print(f"[rekah-unreal] .lsp.json already exists, skipping")
            return True

        with open(lsp_file, "w", encoding="utf-8") as f:
            json.dump(lsp_config, f, indent=2, ensure_ascii=False)
        print(f"[rekah-unreal] Created .lsp.json at {lsp_file}")
        return True

    except Exception as e:
        print(f"[rekah-unreal] Error creating .lsp.json: {e}", file=sys.stderr)
        return False


def check_compile_commands(project_dir: str) -> bool:
    """
    Check if compile_commands.json exists.

    Args:
        project_dir: The project directory path

    Returns:
        True if exists, False otherwise
    """
    compile_commands = Path(project_dir) / "compile_commands.json"

    if compile_commands.exists():
        print(f"[rekah-unreal] compile_commands.json found")
        return True
    else:
        print(f"[rekah-unreal] WARNING: compile_commands.json NOT found")
        print(f"[rekah-unreal] LSP features may not work properly")
        print(f"[rekah-unreal] To generate, run:")
        print(f"[rekah-unreal]   dotnet Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll \\")
        print(f"[rekah-unreal]     -mode=GenerateClangDatabase \\")
        print(f"[rekah-unreal]     -project=\"<YourProject>.uproject\" \\")
        print(f"[rekah-unreal]     <ProjectName>Editor Win64 Development")
        return False


def check_clangd() -> bool:
    """
    Check if clangd is installed.

    Returns:
        True if installed, False otherwise
    """
    try:
        result = subprocess.run(
            ["clangd", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.strip().split('\n')[0]
            print(f"[rekah-unreal] clangd found: {version_line}")
            return True
        else:
            print(f"[rekah-unreal] WARNING: clangd not responding properly")
            return False
    except FileNotFoundError:
        print(f"[rekah-unreal] WARNING: clangd NOT installed")
        print(f"[rekah-unreal] Install clangd for LSP support:")
        print(f"[rekah-unreal]   Windows: choco install llvm")
        print(f"[rekah-unreal]   Mac: brew install llvm")
        print(f"[rekah-unreal]   Linux: sudo apt install clangd")
        return False
    except subprocess.TimeoutExpired:
        print(f"[rekah-unreal] WARNING: clangd check timed out")
        return False
    except Exception as e:
        print(f"[rekah-unreal] Error checking clangd: {e}", file=sys.stderr)
        return False


def is_unreal_project(project_dir: str) -> bool:
    """
    Check if the directory is an Unreal Engine project.

    Args:
        project_dir: The project directory path

    Returns:
        True if Unreal project detected, False otherwise
    """
    project_path = Path(project_dir)

    # Check for .uproject file
    uproject_files = list(project_path.glob("*.uproject"))
    if uproject_files:
        print(f"[rekah-unreal] Unreal project detected: {uproject_files[0].name}")
        return True

    # Check for Games directory (source build)
    games_dir = project_path / "Games"
    if games_dir.exists() and games_dir.is_dir():
        game_uprojects = list(games_dir.glob("*/*.uproject"))
        if game_uprojects:
            print(f"[rekah-unreal] Unreal Engine source build detected")
            print(f"[rekah-unreal] Game projects found: {len(game_uprojects)}")
            return True

    # Check for Engine directory (source build)
    engine_dir = project_path / "Engine"
    if engine_dir.exists() and engine_dir.is_dir():
        print(f"[rekah-unreal] Unreal Engine directory detected")
        return True

    print(f"[rekah-unreal] Not an Unreal Engine project")
    return False


def main():
    """Main entry point."""
    # Get project directory from environment or argument
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")

    if not project_dir and len(sys.argv) > 1:
        project_dir = sys.argv[1]

    if not project_dir:
        print("[rekah-unreal] Error: CLAUDE_PROJECT_DIR not set", file=sys.stderr)
        sys.exit(1)

    print(f"[rekah-unreal] Project directory: {project_dir}")
    print(f"[rekah-unreal] Running setup-project.py...")

    # Check if this is an Unreal project
    is_unreal = is_unreal_project(project_dir)

    # Always merge settings (plugin activation)
    settings_ok = merge_settings(project_dir)

    # Only setup LSP config for Unreal projects
    if is_unreal:
        lsp_ok = setup_lsp_config(project_dir)
        compile_ok = check_compile_commands(project_dir)
        clangd_ok = check_clangd()

        print(f"[rekah-unreal] Setup complete:")
        print(f"[rekah-unreal]   - settings.json: {'OK' if settings_ok else 'FAILED'}")
        print(f"[rekah-unreal]   - .lsp.json: {'OK' if lsp_ok else 'FAILED'}")
        print(f"[rekah-unreal]   - compile_commands.json: {'OK' if compile_ok else 'NOT FOUND'}")
        print(f"[rekah-unreal]   - clangd: {'OK' if clangd_ok else 'NOT FOUND'}")
    else:
        print(f"[rekah-unreal] Setup complete:")
        print(f"[rekah-unreal]   - settings.json: {'OK' if settings_ok else 'FAILED'}")
        print(f"[rekah-unreal]   - LSP setup: SKIPPED (not Unreal project)")

    sys.exit(0 if settings_ok else 1)


if __name__ == "__main__":
    main()
