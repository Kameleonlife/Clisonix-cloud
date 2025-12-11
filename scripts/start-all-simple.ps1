#!/usr/bin/env pwsh
#
# Clisonix Cloud - Simple Start Script
# Starts Frontend (Next.js) and API (FastAPI)
#

param(
    [switch]$Detached,
    [switch]$Clean
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location -Path $Root

Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  CLISONIX CLOUD - START SERVICES      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Cleanup if requested
if ($Clean) {
    Write-Host "[*] Stopping existing services..." -ForegroundColor Yellow
    Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "[✓] Cleanup complete`n" -ForegroundColor Green
}

# Start API (FastAPI)
Write-Host "[→] Starting FastAPI Backend..." -ForegroundColor Cyan
$apiCmd = {
    Set-Location $Root
    python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
}

if ($Detached) {
    Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$Root'; python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000"
    Write-Host "[✓] API started in new window (port 8000)" -ForegroundColor Green
} else {
    Start-Job -ScriptBlock $apiCmd -Name "API"
    Write-Host "[✓] API started in background (port 8000)" -ForegroundColor Green
}

Start-Sleep -Seconds 2

# Start Frontend (Next.js)
Write-Host "[→] Starting Next.js Frontend..." -ForegroundColor Cyan
$frontendCmd = {
    Set-Location "$Root\apps\web"
    $env:NEXT_PUBLIC_API_BASE = 'http://localhost:8000'
    npm run dev
}

if ($Detached) {
    Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$Root\apps\web'; `$env:NEXT_PUBLIC_API_BASE='http://localhost:8000'; npm run dev"
    Write-Host "[✓] Frontend started in new window (port 3000)" -ForegroundColor Green
} else {
    Start-Job -ScriptBlock $frontendCmd -Name "Frontend"
    Write-Host "[✓] Frontend started in background (port 3000)" -ForegroundColor Green
}

Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✓ SERVICES STARTED SUCCESSFULLY      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📍 SERVICE ENDPOINTS:" -ForegroundColor White
Write-Host "   Frontend Dashboard:   http://localhost:3000" -ForegroundColor Cyan
Write-Host "   API Documentation:    http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   API Health Check:     http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""

if (-not $Detached) {
    Write-Host "💼 BACKGROUND JOBS:" -ForegroundColor White
    Write-Host "   List jobs:    Get-Job" -ForegroundColor Gray
    Write-Host "   View logs:    Get-Job | Receive-Job" -ForegroundColor Gray
    Write-Host "   Stop all:     Get-Job | Stop-Job" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "[✓] System is ready!`n" -ForegroundColor Green
