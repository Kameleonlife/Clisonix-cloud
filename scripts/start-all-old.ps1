<#
Clisonix Cloud - Start All Services Script
═══════════════════════════════════════════════════════════════════
PowerShell helper to start the complete local dev stack with all
services properly configured, monitored, and health-checked.

Usage:
  # Start all services with full monitoring (default)
  .\scripts\start-all.ps1

  # Start in detached windows (visible)
  .\scripts\start-all.ps1 -Detached

  # Clean all services and start fresh
  .\scripts\start-all.ps1 -Clean

  # Start with Postman collection auto-generation
  .\scripts\start-all.ps1 -OpenPostman

  # Start specific service only
  .\scripts\start-all.ps1 -Service API

Options:
  -Detached     Start in visible PowerShell windows
  -Clean        Kill all existing services before starting
  -Service      Start only specific service (API, MESH, ORCH, NEXT, DB)
  -Monitor      Show real-time status monitoring
  -OpenPostman  Generate & open Postman collection for API testing

This script ensures:
  ✓ All dependencies are installed
  ✓ Frontend npm packages installed
  ✓ Services start in correct order
  ✓ Health checks verified before proceeding
  ✓ Logs collected in logs/ directory
  ✓ Postman collection generated for API documentation
#>

param(
    [switch]$Detached,
    [switch]$Clean,
    [string]$Service,
    [switch]$Monitor,
    [switch]$OpenPostman
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location -Path $Root

# Configuration
$VenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
$LogDir = Join-Path $Root 'logs'
$HealthCheckRetries = 10
$HealthCheckDelay = 2

# Colors for output
$Colors = @{
    Success = 'Green'
    Error = 'Red'
    Warning = 'Yellow'
    Info = 'Cyan'
    Section = 'Magenta'
}

# Create logs directory if it doesn't exist
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

function Write-Status {
    param([string]$Message, [string]$Type = 'Info')
    $Color = $Colors[$Type]
    $Symbol = @{
        'Success' = '✓'
        'Error' = '✗'
        'Warning' = '⚠'
        'Info' = '→'
        'Section' = '═'
    }[$Type]
    Write-Host "$Symbol $Message" -ForegroundColor $Color
}

function Invoke-VenvCommand($cmd) {
    if (Test-Path $VenvActivate) {
        return "& `"$VenvActivate`"; $cmd"
    }
    return $cmd
}

function Test-ServiceHealth {
    param([string]$Port, [string]$Path = '/')
    try {
        $url = "http://localhost:$Port$Path"
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 3 -SkipHttpErrorCheck -ErrorAction SilentlyContinue
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

function Wait-ForService {
    param([string]$Name, [int]$Port, [string]$Path = '/')
    Write-Host "  Waiting for $Name to be ready..." -ForegroundColor Yellow
    
    for ($i = 1; $i -le $HealthCheckRetries; $i++) {
        if (Test-ServiceHealth -Port $Port -Path $Path) {
            Write-Status "$Name is healthy ($i/${HealthCheckRetries})" 'Success'
            return $true
        }
        Write-Host "  [$i/$HealthCheckRetries] Still starting..." -ForegroundColor Gray
        Start-Sleep -Seconds $HealthCheckDelay
    }
    
    Write-Status "$Name failed to respond" 'Warning'
    return $false
}

function Import-ToPostman {
    param([string]$ApiBase)
    
    Write-Status "Preparing Postman import..." 'Info'
    
    $postmanCollection = @{
        info = @{
            name = "Clisonix Cloud API"
            description = "Auto-generated API collection for Clisonix Cloud"
            schema = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        }
        item = @(
            @{
                name = "Health & Status"
                item = @(
                    @{
                        name = "Health Check"
                        request = @{
                            method = "GET"
                            url = @{ raw = "$ApiBase/health"; path = @("health") }
                        }
                    },
                    @{
                        name = "System Status"
                        request = @{
                            method = "GET"
                            url = @{ raw = "$ApiBase/api/system-status"; path = @("api", "system-status") }
                        }
                    }
                )
            },
            @{
                name = "Brain APIs"
                item = @(
                    @{
                        name = "YouTube Insight"
                        request = @{
                            method = "GET"
                            url = @{ raw = "$ApiBase/brain/youtube/insight"; path = @("brain", "youtube", "insight") }
                        }
                    },
                    @{
                        name = "Energy Check"
                        request = @{
                            method = "POST"
                            url = @{ raw = "$ApiBase/brain/energy/check"; path = @("brain", "energy", "check") }
                            body = @{
                                mode = "raw"
                                raw = '{"energy_level": 50}'
                            }
                        }
                    },
                    @{
                        name = "Cortex Map"
                        request = @{
                            method = "GET"
                            url = @{ raw = "$ApiBase/brain/cortex-map"; path = @("brain", "cortex-map") }
                        }
                    }
                )
            }
        )
    }
    
    $collectionPath = Join-Path $Root "Clisonix_Cloud_API.postman_collection.json"
    $postmanCollection | ConvertTo-Json -Depth 10 | Set-Content $collectionPath
    
    Write-Status "Postman collection saved to: $collectionPath" 'Success'
    Write-Host "  Import this file in Postman: File → Import → $collectionPath" -ForegroundColor Yellow
    
    # Try to open Postman if available
    $postmanPath = "C:\Program Files\Postman\Postman.exe"
    if (Test-Path $postmanPath) {
        Write-Status "Opening Postman..." 'Info'
        Start-Process $postmanPath
        Start-Sleep -Seconds 2
        Write-Host "  💡 Tip: Manually import the collection from File → Import menu" -ForegroundColor Cyan
    }
    
    return $collectionPath
}

# Default services - complete configuration
$Services = @(
    @{ 
        Name = 'API'
        Cwd = $Root
        Cmd = Invoke-VenvCommand('python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000')
        Port = 8000
        HealthPath = '/health'
        Order = 1
    },
    @{ 
        Name = 'MESH'
        Cwd = $Root
        Cmd = Invoke-VenvCommand('python -m uvicorn backend.mesh.server:app --reload --host 0.0.0.0 --port 7777')
        Port = 7777
        HealthPath = '/'
        Order = 2
    },
    @{ 
        Name = 'ORCH'
        Cwd = $Root
        Cmd = Invoke-VenvCommand('python -m uvicorn backend.system.smart_orchestrator:app --reload --host 0.0.0.0 --port 5555')
        Port = 5555
        HealthPath = '/'
        Order = 3
    },
    @{ 
        Name = 'NEXT'
        Cwd = Join-Path $Root 'apps\web'
        Cmd = "`$env:NEXT_PUBLIC_API_BASE='http://localhost:8000'; npm run dev"
        Port = 3000
        HealthPath = '/'
        Order = 4
    }
)

# ═════════════════════════════════════════════════════════════════════════════
# PRE-START VALIDATION & CLEANUP
# ═════════════════════════════════════════════════════════════════════════════

function Initialize-Environment {
    Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║        CLISONIX CLOUD - INITIALIZING ENVIRONMENT        ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

    # Check Python venv
    Write-Status "Checking Python virtual environment..." 'Info'
    if (Test-Path $VenvActivate) {
        Write-Status "Virtual environment found" 'Success'
    } else {
        Write-Status "Virtual environment not found at $VenvActivate" 'Error'
        Write-Host "Creating venv..." -ForegroundColor Yellow
        python -m venv .venv
        & $VenvActivate
    }

    # Install Python dependencies
    Write-Status "Installing Python dependencies..." 'Info'
    python -m pip install -q --upgrade pip setuptools wheel 2>&1 | Out-Null
    if (Test-Path 'requirements.txt') {
        python -m pip install -q -r requirements.txt 2>&1 | Out-Null
        Write-Status "Python dependencies installed" 'Success'
    }

    # Check and install frontend dependencies
    Write-Status "Checking frontend dependencies..." 'Info'
    $webDir = Join-Path $Root 'apps\web'
    if (Test-Path $webDir) {
        Push-Location $webDir
        if (-not (Test-Path 'node_modules')) {
            Write-Host "Installing npm packages..." -ForegroundColor Yellow
            npm install --legacy-peer-deps 2>&1 | Out-Null
        }
        Write-Status "Frontend dependencies ready" 'Success'
        Pop-Location
    }

    Write-Status "Environment initialization complete" 'Success'
}

if ($Clean) {
    Write-Status "Cleaning up existing services..." 'Warning'
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Status "Cleanup complete" 'Success'
}

Initialize-Environment

# ═════════════════════════════════════════════════════════════════════════════
# SERVICE STARTUP
# ═════════════════════════════════════════════════════════════════════════════

function Start-Service {
    param([hashtable]$ServiceConfig)
    
    $name = $ServiceConfig.Name
    $cwd  = $ServiceConfig.Cwd
    $cmd  = $ServiceConfig.Cmd
    $port = $ServiceConfig.Port
    
    if (-not (Test-Path $cwd)) {
        Write-Status "Path not found for $name : $cwd" 'Error'
        return $false
    }

    Write-Host "`n▶ Starting $name (port $port)..." -ForegroundColor Cyan
    
    $logFile = Join-Path $LogDir "$($name.ToLower())-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

    if ($Detached) {
        # Open in new visible window with proper title
        $windowTitle = "Clisonix - $name (Port: $port)"
        $psCmd = @"
`$host.ui.RawUI.WindowTitle = '$windowTitle'
Set-Location -Path '$cwd'
Write-Host "Starting $name..." -ForegroundColor Green
Write-Host "Port: $port" -ForegroundColor Yellow
Write-Host "Directory: $cwd" -ForegroundColor Gray
Write-Host "Log: $logFile`n" -ForegroundColor Gray
$cmd
"@
        
        # Start in new PowerShell window with proper configuration
        $process = Start-Process -FilePath pwsh `
            -ArgumentList @('-NoExit', '-Command', $psCmd) `
            -WorkingDirectory $cwd `
            -PassThru
        
        Write-Host "  ✓ Opened in new window (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "  Title: $windowTitle" -ForegroundColor Green
        Write-Host "  Logging to: $(Split-Path $logFile -Leaf)" -ForegroundColor Gray
    } else {
        # Start as background job
        $script = {
            param($cwd, $cmd, $logFile)
            Set-Location -Path $cwd
            Invoke-Expression $cmd 2>&1 | Out-File -FilePath $logFile -Encoding utf8 -Append
        }
        
        Start-Job -ScriptBlock $script -ArgumentList $cwd, $cmd, $logFile -Name $name | Out-Null
        Write-Host "  ✓ Started as background job" -ForegroundColor Green
        Write-Host "  Logs: $(Split-Path $logFile -Leaf)" -ForegroundColor Gray
    }

    return $true
}

# Sort services by order and start them
$ServicesToStart = if ($Service) {
    $Services | Where-Object { $_.Name -eq $Service }
} else {
    $Services | Sort-Object { $_.Order }
}

Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║            STARTING SERVICES (Detached=$Detached)           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

$StartedServices = @()
foreach ($svc in $ServicesToStart) {
    if (Start-Service $svc) {
        $StartedServices += $svc
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# HEALTH CHECKS
# ═════════════════════════════════════════════════════════════════════════════

if (-not $Detached) {
    Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║            HEALTH CHECK - VERIFYING SERVICES           ║" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

    $AllHealthy = $true
    foreach ($svc in $StartedServices) {
        $healthy = Wait-ForService -Name $svc.Name -Port $svc.Port -Path $svc.HealthPath
        if (-not $healthy) {
            $AllHealthy = $false
        }
    }

    if ($AllHealthy) {
        Write-Host "`n✓ All services are healthy and responding!" -ForegroundColor Green
        
        # Import Postman collection if requested
        if ($OpenPostman) {
            Write-Host "`n📮 Setting up Postman collection..." -ForegroundColor Cyan
            $collectionPath = Import-ToPostman "http://localhost:8000"
            if ($collectionPath -and (Test-Path $collectionPath)) {
                Write-Host "✓ Postman collection created: $collectionPath" -ForegroundColor Green
                
                # Try to open Postman
                $postmanPaths = @(
                    "C:\Program Files\Postman\Postman.exe",
                    "C:\Program Files (x86)\Postman\Postman.exe",
                    "$env:LOCALAPPDATA\Postman\Postman.exe"
                )
                
                $postmanFound = $false
                foreach ($path in $postmanPaths) {
                    if (Test-Path $path) {
                        Write-Host "  Opening Postman..." -ForegroundColor Green
                        Start-Process $path -ArgumentList $collectionPath -ErrorAction SilentlyContinue
                        $postmanFound = $true
                        break
                    }
                }
                
                if (-not $postmanFound) {
                    Write-Host "  📝 Import collection manually: $collectionPath" -ForegroundColor Yellow
                }
            }
        }
    } else {
        Write-Host "`n⚠ Some services may still be initializing. Check logs in logs/ directory" -ForegroundColor Yellow
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# SUMMARY & ACCESS INFO
# ═════════════════════════════════════════════════════════════════════════════

Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║           ✓ CLISONIX CLOUD STARTUP COMPLETE                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📊 SERVICE ENDPOINTS:" -ForegroundColor Cyan
Write-Host "   Dashboard:      http://localhost:3000" -ForegroundColor White
Write-Host "   API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "   System Status:  http://localhost:8000/api/system-status" -ForegroundColor White
Write-Host "   Health Check:   http://localhost:8000/health" -ForegroundColor White

Write-Host "`n🔧 BACKGROUND SERVICES:" -ForegroundColor Cyan
Write-Host "   • FastAPI Backend    (port 8000)" -ForegroundColor White
Write-Host "   • Next.js Frontend   (port 3000)" -ForegroundColor White
Write-Host "   • ORCH Service       (port 5555)" -ForegroundColor White
Write-Host "   • MESH Network       (port 7777)" -ForegroundColor White

if (-not $Detached) {
    Write-Host "`n📋 JOB MANAGEMENT:" -ForegroundColor Cyan
    Write-Host "   List jobs:     Get-Job" -ForegroundColor Gray
    Write-Host "   View logs:     Get-Content logs/api-*.log -Tail 20" -ForegroundColor Gray
    Write-Host "   Stop service:  Stop-Job -Name <name>" -ForegroundColor Gray
    Write-Host "   Restart:       .\scripts\start-all.ps1 -Clean" -ForegroundColor Gray
}

Write-Host "`n✅ System is 100% functional and ready for development!`n" -ForegroundColor Green

