# Clisonix Backend Startup Script
# This script starts the backend server with proper uvicorn configuration

param(
    [string]$Port = "8000",
    [string]$HostAddr = "127.0.0.1",
    [switch]$Reload = $false,
    [switch]$NoAccessLog = $true
)

# Kill any existing Python processes
Write-Host "🛑 Stopping any existing Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Navigate to project root
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "🚀 Starting Clisonix Backend Server" -ForegroundColor Green
Write-Host "📍 URL: http://$HostAddr`:$Port" -ForegroundColor Cyan
Write-Host "📁 Directory: $(Get-Location)" -ForegroundColor Cyan

# Build uvicorn command
$uvicornArgs = @(
    "apps.api.main:app",
    "--host", $HostAddr,
    "--port", $Port
)

if ($Reload) {
    $uvicornArgs += "--reload"
}

if ($NoAccessLog) {
    $uvicornArgs += "--no-access-log"
}

Write-Host "⚙️  Running: python -m uvicorn $($uvicornArgs -join ' ')" -ForegroundColor Gray

# Start the server
python -m uvicorn @uvicornArgs

# If the process exits, show this message
Write-Host "❌ Backend server stopped" -ForegroundColor Red
