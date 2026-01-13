#!/usr/bin/env python3
"""
Setup Claude Code project settings for rekah plugins.
Automatically detects project type and installs appropriate plugins.
- Unreal Engine projects: rekah-unreal plugin
- Python projects: rekah-py plugin
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# log prefix
LOG_PREFIX = "[rekah]"


def get_target_plugins(is_unreal: bool) -> list[str]:
    """
    Get plugins to install based on project type.

    Args:
        is_unreal: True if Unreal Engine project

    Returns:
        List of plugin names in plugin@marketplace format
    """
    if is_unreal:
        return ["rekah-unreal@rekah-plugins"]
    else:
        return ["rekah-py@rekah-plugins"]


def run_claude_command(args: list) -> tuple[bool, str]:
    """
    Run a claude CLI command.

    Args:
        args: Command arguments (without 'claude' prefix)

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            ["claude"] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        # Handle None values - can occur on Windows or when process is interrupted
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        output = stdout + stderr
        return result.returncode == 0, output.strip()
    except FileNotFoundError:
        return False, "claude CLI not found"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def get_installed_marketplaces() -> set:
    """
    Get list of currently installed marketplaces using CLI.

    Returns:
        Set of marketplace names
    """
    success, output = run_claude_command(["plugin", "marketplace", "list"])
    if not success:
        return set()

    # Parse output like:
    #   ❯ rekah-plugins
    #     Source: GitHub (tkdgur4427/rekah-plugins)
    marketplaces = set()
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('❯ '):
            name = line[2:].strip()
            marketplaces.add(name)
    return marketplaces


def add_marketplace(name: str, repo: str) -> bool:
    """
    Add a marketplace using claude CLI.

    Args:
        name: Marketplace name (for logging)
        repo: GitHub repo in owner/repo format

    Returns:
        True if successful or already exists
    """
    # Check if already installed
    installed = get_installed_marketplaces()
    if name in installed:
        print(f"[rekah] Marketplace already installed: {name}")
        return True

    # Add marketplace
    print(f"[rekah] Adding marketplace: {name} ({repo})")
    success, output = run_claude_command(["plugin", "marketplace", "add", repo])

    if success:
        print(f"[rekah] Successfully added marketplace: {name}")
        return True
    else:
        # Check if it's already added (might have been added by another process)
        if "already" in output.lower() or name in get_installed_marketplaces():
            print(f"[rekah] Marketplace already exists: {name}")
            return True
        print(f"[rekah] Failed to add marketplace {name}: {output}")
        return False


def install_plugin(plugin: str) -> bool:
    """
    Install a plugin using claude CLI.

    Args:
        plugin: Plugin name in plugin@marketplace format

    Returns:
        True if successful or already installed
    """
    print(f"[rekah] Installing plugin: {plugin} (project scope)")
    success, output = run_claude_command(["plugin", "install", plugin, "--scope", "project"])

    if success:
        print(f"[rekah] Successfully installed plugin: {plugin}")
        return True
    else:
        # Check if already installed
        if "already" in output.lower():
            print(f"[rekah] Plugin already installed: {plugin}")
            return True
        print(f"[rekah] Failed to install plugin {plugin}: {output}")
        return False


def setup_marketplaces_and_plugins(is_unreal: bool) -> bool:
    """
    Setup required marketplaces and plugins using claude CLI.

    Args:
        is_unreal: True if Unreal Engine project

    Returns:
        True if all successful, False otherwise
    """
    # Marketplaces to register (name -> GitHub repo)
    marketplaces = {
        "rekah-plugins": "tkdgur4427/rekah-plugins",
        "claude-plugins-official": "anthropics/claude-plugins-official"
    }

    # Plugins to install based on project type
    plugins = get_target_plugins(is_unreal)

    all_success = True

    # Add marketplaces
    for name, repo in marketplaces.items():
        if not add_marketplace(name, repo):
            all_success = False

    # Install plugins
    for plugin in plugins:
        if not install_plugin(plugin):
            all_success = False

    return all_success


def merge_settings(project_dir: str, is_unreal: bool) -> bool:
    """
    Merge rekah plugin settings into .claude/settings.json.
    Now primarily handles project-level settings, as marketplace/plugin
    installation is done via CLI.

    Args:
        project_dir: The project directory path
        is_unreal: True if Unreal Engine project

    Returns:
        True if successful, False otherwise
    """
    claude_dir = Path(project_dir) / ".claude"
    settings_file = claude_dir / "settings.json"

    # Plugin settings based on project type
    plugins = get_target_plugins(is_unreal)
    plugin_settings = {p: True for p in plugins}

    try:
        # Ensure .claude directory exists
        claude_dir.mkdir(parents=True, exist_ok=True)

        # Load existing settings or create new
        if settings_file.exists():
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
            print(f"[rekah] Loaded existing settings.json")
        else:
            settings = {}
            print(f"[rekah] Creating new settings.json")

        updated = False

        # Ensure enabledPlugins section exists
        if "enabledPlugins" not in settings:
            settings["enabledPlugins"] = {}

        # Merge plugin settings (only add if not already set)
        for plugin, enabled in plugin_settings.items():
            if plugin not in settings["enabledPlugins"]:
                settings["enabledPlugins"][plugin] = enabled
                print(f"[rekah] Added plugin to project settings: {plugin} = {enabled}")
                updated = True
            else:
                print(f"[rekah] Plugin already in project settings: {plugin}")

        # Save if updated
        if updated:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            print(f"[rekah] Settings saved to {settings_file}")
        else:
            print(f"[rekah] No changes needed")

        return True

    except Exception as e:
        print(f"[rekah] Error: {e}", file=sys.stderr)
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
        print(f"[rekah] compile_commands.json found")
        return True
    else:
        print(f"[rekah] WARNING: compile_commands.json NOT found")
        print(f"[rekah] LSP features may not work properly")
        print(f"[rekah] To generate, run:")
        print(f"[rekah]   dotnet Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll \\")
        print(f"[rekah]     -mode=GenerateClangDatabase \\")
        print(f"[rekah]     -project=\"<YourProject>.uproject\" \\")
        print(f"[rekah]     <ProjectName>Editor Win64 Development")
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
            print(f"[rekah] clangd found: {version_line}")
            return True
        else:
            print(f"[rekah] WARNING: clangd not responding properly")
            return False
    except FileNotFoundError:
        print(f"[rekah] WARNING: clangd NOT installed")
        print(f"[rekah] Install clangd for LSP support:")
        print(f"[rekah]   Windows: choco install llvm")
        print(f"[rekah]   Mac: brew install llvm")
        print(f"[rekah]   Linux: sudo apt install clangd")
        return False
    except subprocess.TimeoutExpired:
        print(f"[rekah] WARNING: clangd check timed out")
        return False
    except Exception as e:
        print(f"[rekah] Error checking clangd: {e}", file=sys.stderr)
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
        print(f"[rekah] Unreal project detected: {uproject_files[0].name}")
        return True

    # Check for Games directory (source build)
    games_dir = project_path / "Games"
    if games_dir.exists() and games_dir.is_dir():
        game_uprojects = list(games_dir.glob("*/*.uproject"))
        if game_uprojects:
            print(f"[rekah] Unreal Engine source build detected")
            print(f"[rekah] Game projects found: {len(game_uprojects)}")
            return True

    # Check for Engine directory (source build)
    engine_dir = project_path / "Engine"
    if engine_dir.exists() and engine_dir.is_dir():
        print(f"[rekah] Unreal Engine directory detected")
        return True

    print(f"[rekah] Not an Unreal Engine project")
    return False


def main():
    """Main entry point."""
    # Get project directory from environment or argument
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")

    if not project_dir and len(sys.argv) > 1:
        project_dir = sys.argv[1]

    if not project_dir:
        print("[rekah] Error: CLAUDE_PROJECT_DIR not set", file=sys.stderr)
        sys.exit(1)

    print(f"[rekah] Project directory: {project_dir}")
    print(f"[rekah] Running setup-project.py...")

    # Check if this is an Unreal project
    is_unreal = is_unreal_project(project_dir)

    # Setup marketplaces and plugins via CLI (user-level)
    marketplace_ok = setup_marketplaces_and_plugins(is_unreal)

    # Merge project-level settings
    settings_ok = merge_settings(project_dir, is_unreal)

    # Check LSP prerequisites for Unreal projects
    if is_unreal:
        compile_ok = check_compile_commands(project_dir)
        clangd_ok = check_clangd()

        print(f"[rekah] Setup complete:")
        print(f"[rekah]   - marketplaces: {'OK' if marketplace_ok else 'PARTIAL'}")
        print(f"[rekah]   - settings.json: {'OK' if settings_ok else 'FAILED'}")
        print(f"[rekah]   - compile_commands.json: {'OK' if compile_ok else 'NOT FOUND'}")
        print(f"[rekah]   - clangd: {'OK' if clangd_ok else 'NOT FOUND'}")
    else:
        print(f"[rekah] Setup complete:")
        print(f"[rekah]   - marketplaces: {'OK' if marketplace_ok else 'PARTIAL'}")
        print(f"[rekah]   - settings.json: {'OK' if settings_ok else 'FAILED'}")

    sys.exit(0 if settings_ok else 1)


if __name__ == "__main__":
    main()
