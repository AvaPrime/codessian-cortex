<#
 Bootstrap the Ava Prime Dashboard v2.0 environment on Windows (PowerShell).
 Steps:
 1) Create venv
 2) Install requirements
 3) Prepare .env and directories
#>

param(
    [string]$PythonExe = "python"
)

Write-Host "[Setup] Creating virtual environment..." -ForegroundColor Cyan
$venvPath = Join-Path $PSScriptRoot "venv"
& $PythonExe -m venv $venvPath

Write-Host "[Setup] Activating virtual environment..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

Write-Host "[Setup] Upgrading pip and installing requirements..." -ForegroundColor Cyan
pip install --upgrade pip
if (Test-Path "$PSScriptRoot\requirements.txt") {
    pip install -r "$PSScriptRoot\requirements.txt"
} else {
    Write-Warning "requirements.txt not found. Install dependencies manually if needed."
}

Write-Host "[Setup] Preparing .env file..." -ForegroundColor Cyan
if (-not (Test-Path "$PSScriptRoot\.env")) {
    if (Test-Path "$PSScriptRoot\.env.example") {
        Copy-Item "$PSScriptRoot\.env.example" "$PSScriptRoot\.env"
        Write-Host "Created .env from template. Please update values." -ForegroundColor Yellow
    } else {
        New-Item -ItemType File -Path "$PSScriptRoot\.env" | Out-Null
        Write-Host "Created empty .env. Please add required values." -ForegroundColor Yellow
    }
}

Write-Host "[Setup] Ensuring directories exist..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$PSScriptRoot\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$PSScriptRoot\cache" | Out-Null

Write-Host "[Setup] Done. Next steps:" -ForegroundColor Green
Write-Host "  - Update .env with your API keys and settings"
Write-Host "  - Run: python verify_setup.py"
Write-Host "  - Then: python ava_prime_integration.py" 

