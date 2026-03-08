# SessionStart Hook for rekah-unreal plugin
# This script runs when a Claude Code session starts (Windows/PowerShell)

Write-Host "[rekah-unreal] SessionStart hook triggered"
Write-Host "[rekah-unreal] Plugin root: $env:CLAUDE_PLUGIN_ROOT"
Write-Host "[rekah-unreal] Project dir: $env:CLAUDE_PROJECT_DIR"

# MCP server dependency check
$McpServerDir = Join-Path $env:CLAUDE_PLUGIN_ROOT "mcp-server"
$VenvDir = Join-Path $McpServerDir ".venv"

if (-not (Test-Path $VenvDir)) {
    Write-Host "[rekah-unreal] First run: installing MCP server dependencies..."
    uv --directory $McpServerDir sync
}

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Setup project using Python (settings.json, environment checks)
$SetupScript = Join-Path $ScriptDir "setup-project.py"

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[rekah-unreal] Running setup-project.py..."
    python $SetupScript
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    Write-Host "[rekah-unreal] Running setup-project.py..."
    python3 $SetupScript
} else {
    Write-Host "[rekah-unreal] Warning: Python not found, skipping project setup"
}

# Check if this is an Unreal Engine project
$UProjectFiles = Get-ChildItem -Path "." -Filter "*.uproject" -ErrorAction SilentlyContinue
$EngineDir = Test-Path "Engine"

if ($UProjectFiles -or $EngineDir) {
    Write-Host "[rekah-unreal] Unreal Engine project detected"
}

# Check for compile_commands.json
if (Test-Path "compile_commands.json") {
    Write-Host "[rekah-unreal] compile_commands.json found"
} else {
    Write-Host "[rekah-unreal] compile_commands.json NOT found - LSP may not work properly"
}

exit 0
