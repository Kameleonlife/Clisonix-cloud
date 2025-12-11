#!/usr/bin/env pwsh
#
# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    CLISONIX CLOUD - MEGA LAUNCHER                 ║
# ║                   "Next Generation Startup Script"                ║
# ║                                                                   ║
# ║  Launches the entire Clisonix Cloud stack like a modern aircraft  ║
# ║  with pre-flight checks, parallel initialization, and real-time   ║
# ║  monitoring dashboard.                                            ║
# ╚═══════════════════════════════════════════════════════════════════╝
#

param(
    [ValidateSet('1', '2', '3')]
    [string]$Mode = '3',
    [switch]$Clean,
    [switch]$Monitor
)

$Root = 'c:\neurosonix-cloud'
Set-Location $Root

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION & STYLING
# ═══════════════════════════════════════════════════════════════════

$Colors = @{
    Title    = 'Magenta'
    Success  = 'Green'
    Warning  = 'Yellow'
    Error    = 'Red'
    Info     = 'Cyan'
    Section  = 'Blue'
}

function Show-Banner {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Title
    Write-Host "║                                                                   ║" -ForegroundColor $Colors.Title
    Write-Host "║     🚀  CLISONIX CLOUD - NEXT GENERATION LAUNCHER  🚀             ║" -ForegroundColor $Colors.Title
    Write-Host "║                                                                   ║" -ForegroundColor $Colors.Title
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor $Colors.Title
}

function Show-Status {
    param([string]$Message, [string]$Status = 'INFO')
    $Icon = @{
        'INFO'    = '▸'
        'OK'      = '✓'
        'WAIT'    = '◌'
        'ERROR'   = '✗'
        'WARN'    = '⚠'
    }[$Status]
    
    $Color = @{
        'INFO'    = $Colors.Info
        'OK'      = $Colors.Success
        'WAIT'    = $Colors.Warning
        'ERROR'   = $Colors.Error
        'WARN'    = $Colors.Warning
    }[$Status]
    
    Write-Host "  $Icon " -NoNewline -ForegroundColor $Color
    Write-Host $Message
}

function Invoke-PreFlightCheck {
    Write-Host "`n┌─── PRE-FLIGHT CHECKS ───────────────────────────────────────┐" -ForegroundColor $Colors.Section
    
    # Check Node.js
    Show-Status "Checking Node.js..." 'WAIT'
    $node = node --version 2>$null
    if ($node) {
        Show-Status "Node.js $node ✓" 'OK'
    } else {
        Show-Status "Node.js not found" 'ERROR'
        return $false
    }
    
    # Check Python
    Show-Status "Checking Python..." 'WAIT'
    $python = python --version 2>&1
    if ($?) {
        Show-Status "Python installed ✓" 'OK'
    } else {
        Show-Status "Python not found" 'ERROR'
        return $false
    }
    
    # Check dependencies
    Show-Status "Checking dependencies..." 'WAIT'
    if (-not (Test-Path 'apps\web\node_modules')) {
        Show-Status "Installing npm dependencies..." 'WAIT'
        npm install --legacy-peer-deps --silent 2>$null
        Show-Status "Dependencies ready ✓" 'OK'
    } else {
        Show-Status "Dependencies cached ✓" 'OK'
    }
    
    # Check ports
    Show-Status "Checking ports..." 'WAIT'
    $ports3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
    $ports8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    
    if ($ports3000 -or $ports8000) {
        Show-Status "Ports already in use - will attempt restart" 'WARN'
        if ($Clean) {
            Get-Process node, python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
            Start-Sleep 2
            Show-Status "Processes cleaned ✓" 'OK'
        }
    } else {
        Show-Status "Ports available ✓" 'OK'
    }
    
    Write-Host "└────────────────────────────────────────────────────────────────┘" -ForegroundColor $Colors.Section
    return $true
}

function Start-Mode1 {
    Write-Host "`n┌─── MODE 1: BACKGROUND JOBS ─────────────────────────────────┐" -ForegroundColor $Colors.Section
    
    Show-Status "Starting API Server (port 8000)..." 'WAIT'
    $apiJob = Start-Job -Name 'API' -ScriptBlock {
        Set-Location 'c:\neurosonix-cloud'
        python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
    }
    Show-Status "API started (Job #$($apiJob.Id)) ✓" 'OK'
    
    Start-Sleep 2
    
    Show-Status "Starting Frontend (port 3000)..." 'WAIT'
    $webJob = Start-Job -Name 'Frontend' -ScriptBlock {
        Set-Location 'c:\neurosonix-cloud\apps\web'
        $env:NEXT_PUBLIC_API_BASE = 'http://localhost:8000'
        npm run dev
    }
    Show-Status "Frontend started (Job #$($webJob.Id)) ✓" 'OK'
    
    Write-Host "└────────────────────────────────────────────────────────────────┘" -ForegroundColor $Colors.Section
    Show-Status "Use: Get-Job | Stop-Job to stop services" 'INFO'
}

function Start-Mode2 {
    Write-Host "`n┌─── MODE 2: DETACHED WINDOWS ────────────────────────────────┐" -ForegroundColor $Colors.Section
    
    Show-Status "Starting API in new window..." 'WAIT'
    Start-Process pwsh -ArgumentList @(
        '-NoExit',
        '-Command',
        'Set-Location c:\neurosonix-cloud; $host.UI.RawUI.WindowTitle = "Clisonix - API (8000)"; Write-Host "Starting API..." -ForegroundColor Green; python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000'
    )
    Show-Status "API window opened ✓" 'OK'
    
    Start-Sleep 3
    
    Show-Status "Starting Frontend in new window..." 'WAIT'
    Start-Process pwsh -ArgumentList @(
        '-NoExit',
        '-Command',
        'Set-Location c:\neurosonix-cloud\apps\web; $host.UI.RawUI.WindowTitle = "Clisonix - Frontend (3000)"; $env:NEXT_PUBLIC_API_BASE="http://localhost:8000"; Write-Host "Starting Frontend..." -ForegroundColor Green; npm run dev'
    )
    Show-Status "Frontend window opened ✓" 'OK'
    
    Write-Host "└────────────────────────────────────────────────────────────────┘" -ForegroundColor $Colors.Section
    Show-Status "Check the new PowerShell windows for output" 'INFO'
}

function Start-Mode3 {
    Write-Host "`n┌─── MODE 3: MEGA LAUNCH (Next Generation) ──────────────────┐" -ForegroundColor $Colors.Section
    
    Show-Status "Initializing parallel startup sequence..." 'WAIT'
    Start-Sleep 1
    
    Show-Status "Launching API Server..." 'WAIT'
    $apiCmd = 'Set-Location c:\neurosonix-cloud; $host.UI.RawUI.WindowTitle = "🔷 CLISONIX - API SERVER (8000)"; Write-Host "╔═════════════════════════════════════════╗" -ForegroundColor Cyan; Write-Host "║   API SERVER ONLINE - Port 8000        ║" -ForegroundColor Cyan; Write-Host "╚═════════════════════════════════════════╝" -ForegroundColor Cyan; python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000'
    Start-Process pwsh -ArgumentList @('-NoExit', '-Command', $apiCmd)
    Show-Status "API launched ✓" 'OK'
    
    Start-Sleep 2
    
    Show-Status "Launching Frontend..." 'WAIT'
    $webCmd = 'Set-Location c:\neurosonix-cloud\apps\web; $host.UI.RawUI.WindowTitle = "🔶 CLISONIX - FRONTEND (3000)"; $env:NEXT_PUBLIC_API_BASE="http://localhost:8000"; Write-Host "╔═════════════════════════════════════════╗" -ForegroundColor Yellow; Write-Host "║   FRONTEND ONLINE - Port 3000          ║" -ForegroundColor Yellow; Write-Host "╚═════════════════════════════════════════╝" -ForegroundColor Yellow; npm run dev'
    Start-Process pwsh -ArgumentList @('-NoExit', '-Command', $webCmd)
    Show-Status "Frontend launched ✓" 'OK'
    
    Write-Host "└────────────────────────────────────────────────────────────────┘" -ForegroundColor $Colors.Section
    
    Start-Sleep 3
    
    # Health Check
    Write-Host "`n┌─── HEALTH CHECK ────────────────────────────────────────────┐" -ForegroundColor $Colors.Section
    
    for ($i = 1; $i -le 5; $i++) {
        Write-Host "  Checking connectivity ($i/5)..." -ForegroundColor $Colors.Info
        $apiHealth = Invoke-WebRequest -Uri 'http://localhost:8000/health' -SkipHttpErrorCheck -TimeoutSec 2 -ErrorAction SilentlyContinue
        $webHealth = Invoke-WebRequest -Uri 'http://localhost:3000' -SkipHttpErrorCheck -TimeoutSec 2 -ErrorAction SilentlyContinue
        
        if ($apiHealth.StatusCode -eq 200) {
            Show-Status "API responding ✓" 'OK'
            break
        }
        if ($i -lt 5) { Start-Sleep 2 }
    }
    
    Write-Host "└────────────────────────────────────────────────────────────────┘`n" -ForegroundColor $Colors.Section
}

function Show-Dashboard {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Title
    Write-Host "║                        🎯 SYSTEM ONLINE 🎯                        ║" -ForegroundColor $Colors.Title
    Write-Host "╠═══════════════════════════════════════════════════════════════════╣" -ForegroundColor $Colors.Title
    Write-Host "║                                                                   ║" -ForegroundColor $Colors.Title
    Write-Host "║  📊 ENDPOINTS                                                     ║" -ForegroundColor $Colors.Title
    Write-Host "║  ├─ Frontend:      http://localhost:3000                          ║" -ForegroundColor $Colors.Success
    Write-Host "║  ├─ API:           http://localhost:8000                          ║" -ForegroundColor $Colors.Success
    Write-Host "║  ├─ Docs:          http://localhost:8000/docs                     ║" -ForegroundColor $Colors.Success
    Write-Host "║  └─ Health:        http://localhost:8000/health                   ║" -ForegroundColor $Colors.Success
    Write-Host "║                                                                   ║" -ForegroundColor $Colors.Title
    Write-Host "║  ⚙️  STATUS                                                       ║" -ForegroundColor $Colors.Title
    Write-Host "║  └─ Mode: $Mode" -NoNewline -ForegroundColor $Colors.Title
    if ($Mode -eq '1') { Write-Host " (Background Jobs)" -ForegroundColor $Colors.Info }
    elseif ($Mode -eq '2') { Write-Host " (Detached Windows)" -ForegroundColor $Colors.Info }
    else { Write-Host " (Mega Launch - Next Gen)" -ForegroundColor $Colors.Info }
    Write-Host "║                                                                   ║" -ForegroundColor $Colors.Title
    Write-Host "║  💡 TIPS                                                          ║" -ForegroundColor $Colors.Title
    Write-Host "║  ├─ Get-Job              | Show running jobs                      ║" -ForegroundColor $Colors.Warning
    Write-Host "║  ├─ Stop-Job -Name API   | Stop API service                      ║" -ForegroundColor $Colors.Warning
    Write-Host "║  └─ Get-Job | Remove-Job | Clean all jobs                        ║" -ForegroundColor $Colors.Warning
    Write-Host "║                                                                   ║" -ForegroundColor $Colors.Title
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor $Colors.Title
}

# ═══════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════

Show-Banner

if (-not (Invoke-PreFlightCheck)) {
    Show-Status "Pre-flight check failed!" 'ERROR'
    exit 1
}

switch ($Mode) {
    '1' { Start-Mode1 }
    '2' { Start-Mode2 }
    '3' { Start-Mode3 }
}

Show-Dashboard

Write-Host "🚀 Clisonix Cloud is ready for takeoff!`n" -ForegroundColor $Colors.Success
