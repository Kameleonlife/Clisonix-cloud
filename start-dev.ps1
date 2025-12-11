#!/usr/bin/env pwsh
# Quick dev mode launcher - bypasses build issues

$Root = 'c:\neurosonix-cloud'
Set-Location $Root

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║             CLISONIX CLOUD - DEV MODE LAUNCHER              ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

# Start API server in new window
Write-Host "Starting API server on port 8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "cd $Root; npm run dev:api" -NoNewWindow

# Wait for API to start
Write-Host "Waiting for API to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "Starting Frontend (Next.js dev) on port 3000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "cd $Root; npm run dev:web" -NoNewWindow

Write-Host "`n✓ Services launching in separate windows`n" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop services`n" -ForegroundColor Yellow
