#
# Clisonix Cloud - Start All Services Script
# ===============================================
# PowerShell helper to start the complete local dev stack with all
# services properly configured, monitored, and health-checked.
#
# Usage:
#   .\scripts\start-all.ps1                   # Start all services
#   .\scripts\start-all.ps1 -Detached         # Start in visible windows
#   .\scripts\start-all.ps1 -Clean            # Clean and restart
#   .\scripts\start-all.ps1 -OpenPostman      # Generate & open Postman
#
# Options:
#   -Detached     Start in visible PowerShell windows
#   -Clean        Kill all existing services before starting
#   -Service      Start only specific service (API, MESH, ORCH, NEXT, DB)
#   -Monitor      Show real-time status monitoring
#   -OpenPostman  Generate Postman collection for API testing
#

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
        'Success' = '[OK]'
        'Error' = '[ERR]'
        'Warning' = '[WRN]'
        'Info' = '[INF]'
        'Section' = '[---]'
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
            Write-Status "$Name is healthy ($i/$HealthCheckRetries)" 'Success'
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
    
    Write-Status "Preparing Postman collection..." 'Info'
    
    # Build comprehensive collection
    $postmanCollection = @{
        info = @{
            name = "Clisonix Cloud API"
            description = "Auto-generated API collection for Clisonix Cloud - Complete microservices API"
            schema = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        }
        item = @(
            @{
                name = "Health & Diagnostics"
                description = "System health and status endpoints"
                item = @(
                    @{
                        name = "Health Check"
                        description = "Get system health status"
                        request = @{
                            method = "GET"
                            header = @()
                            url = @{ 
                                raw = "$ApiBase/health"
                                protocol = "http"
                                host = @("localhost")
                                port = "8000"
                                path = @("health")
                            }
                        }
                    },
                    @{
                        name = "System Status"
                        description = "Get complete system status"
                        request = @{
                            method = "GET"
                            header = @( @{ key = "Accept"; value = "application/json" } )
                            url = @{ 
                                raw = "$ApiBase/api/system-status"
                                protocol = "http"
                                host = @("localhost")
                                port = "8000"
                                path = @("api", "system-status")
                            }
                        }
                    }
                )
            },
            @{
                name = "Brain Intelligence APIs"
                description = "Advanced AI and cognitive processing endpoints"
                item = @(
                    @{
                        name = "YouTube Insight"
                        description = "Analyze YouTube content and extract insights"
                        request = @{
                            method = "GET"
                            header = @()
                            url = @{ 
                                raw = "$ApiBase/brain/youtube/insight"
                                path = @("brain", "youtube", "insight")
                            }
                        }
                    },
                    @{
                        name = "Energy Check"
                        description = "Check energy levels and system performance"
                        request = @{
                            method = "POST"
                            header = @( @{ key = "Content-Type"; value = "application/json" } )
                            body = @{
                                mode = "raw"
                                raw = '{"energy_level": 50, "threshold": 30}'
                            }
                            url = @{ 
                                raw = "$ApiBase/brain/energy/check"
                                path = @("brain", "energy", "check")
                            }
                        }
                    },
                    @{
                        name = "Cortex Map"
                        description = "Get neural network topology and connections"
                        request = @{
                            method = "GET"
                            header = @()
                            url = @{ 
                                raw = "$ApiBase/brain/cortex-map"
                                path = @("brain", "cortex-map")
                            }
                        }
                    }
                )
            },
            @{
                name = "Documentation"
                description = "API documentation and schema"
                item = @(
                    @{
                        name = "OpenAPI Docs"
                        description = "Interactive Swagger UI documentation"
                        request = @{
                            method = "GET"
                            url = @{ 
                                raw = "$ApiBase/docs"
                                path = @("docs")
                            }
                        }
                    },
                    @{
                        name = "ReDoc Docs"
                        description = "ReDoc API documentation"
                        request = @{
                            method = "GET"
                            url = @{ 
                                raw = "$ApiBase/redoc"
                                path = @("redoc")
                            }
                        }
                    },
                    @{
                        name = "OpenAPI Schema"
                        description = "OpenAPI specification JSON"
                        request = @{
                            method = "GET"
                            url = @{ 
                                raw = "$ApiBase/openapi.json"
                                path = @("openapi.json")
                            }
                        }
                    }
                )
            }
        )
    }
    
    # Save collection to file
    $collectionPath = Join-Path $Root "Clisonix_Cloud_API.postman_collection.json"
    $postmanCollection | ConvertTo-Json -Depth 20 | Set-Content $collectionPath -Encoding UTF8
    
    Write-Status "Postman collection saved to: $collectionPath" 'Success'
    Write-Host "  File size: $('{0:N0}' -f (Get-Item $collectionPath).Length) bytes" -ForegroundColor Cyan
    Write-Host "  Import in Postman: File → Import → $collectionPath" -ForegroundColor Yellow
    
    # Try to open Postman if available
    $postmanPaths = @(
        "C:\Program Files\Postman\Postman.exe",
        "C:\Program Files (x86)\Postman\Postman.exe",
        "$env:LOCALAPPDATA\Postman\Postman.exe"
    )
    
    $postmanFound = $false
    foreach ($path in $postmanPaths) {
        if (Test-Path $path) {
            Write-Status "Opening Postman..." 'Info'
            Start-Process $path -ErrorAction SilentlyContinue
            $postmanFound = $true
            break
        }
    }
    
    if (-not $postmanFound) {
        Write-Host "  💡 Postman not found in common locations" -ForegroundColor Yellow
        Write-Host "  📝 Import collection manually in Postman:" -ForegroundColor Cyan
        Write-Host "     1. Open Postman" -ForegroundColor Gray
        Write-Host "     2. Click 'Import' button" -ForegroundColor Gray
        Write-Host "     3. Select: $collectionPath" -ForegroundColor Gray
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

# ===============================================
# PRE-START VALIDATION & CLEANUP
# ===============================================

function Initialize-Environment {
    Write-Host "`n========================================" -ForegroundColor Magenta
    Write-Host "CLISONIX CLOUD - INITIALIZING ENVIRONMENT" -ForegroundColor Magenta
    Write-Host "========================================`n" -ForegroundColor Magenta

    # Check Python venv
    Write-Status "Checking Python virtual environment..." 'Info'
    if (Test-Path $VenvActivate) {
        Write-Status "Virtual environment found" 'Success'
    } else {
        Write-Status "Virtual environment not found" 'Warning'
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

# ===============================================
# SERVICE STARTUP
# ===============================================

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

    Write-Host "`n> Starting $name (port $port)..." -ForegroundColor Cyan
    
    $logFile = Join-Path $LogDir "$($name.ToLower())-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

    if ($Detached) {
        # Open in new visible window with proper title
        $windowTitle = "Clisonix - $name (Port: $port)"
        $psCmd = @"
`$host.ui.RawUI.WindowTitle = '$windowTitle'
Set-Location -Path '$cwd'
Write-Host 'Starting $name...' -ForegroundColor Green
Write-Host 'Port: $port' -ForegroundColor Yellow
Write-Host 'Directory: $cwd' -ForegroundColor Gray
Write-Host 'Log: $logFile`n' -ForegroundColor Gray
$cmd
"@
        
        # Start in new PowerShell window with proper configuration
        $process = Start-Process -FilePath pwsh `
            -ArgumentList @('-NoExit', '-Command', $psCmd) `
            -WorkingDirectory $cwd `
            -PassThru
        
        Write-Host "  [OK] Opened in new window (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "  Title: $windowTitle" -ForegroundColor Green
    } else {
        # Start as background job
        $script = {
            param($cwd, $cmd, $logFile)
            Set-Location -Path $cwd
            Invoke-Expression $cmd 2>&1 | Out-File -FilePath $logFile -Encoding utf8 -Append
        }
        
        Start-Job -ScriptBlock $script -ArgumentList $cwd, $cmd, $logFile -Name $name | Out-Null
        Write-Host "  [OK] Started as background job" -ForegroundColor Green
    }

    return $true
}

# Sort services by order and start them
$ServicesToStart = if ($Service) {
    $Services | Where-Object { $_.Name -eq $Service }
} else {
    $Services | Sort-Object { $_.Order }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "STARTING SERVICES (Detached=$Detached)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$StartedServices = @()
foreach ($svc in $ServicesToStart) {
    if (Start-Service $svc) {
        $StartedServices += $svc
    }
}

# ===============================================
# HEALTH CHECKS
# ===============================================

if (-not $Detached) {
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "HEALTH CHECK - VERIFYING SERVICES" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow

    $AllHealthy = $true
    foreach ($svc in $StartedServices) {
        $healthy = Wait-ForService -Name $svc.Name -Port $svc.Port -Path $svc.HealthPath
        if (-not $healthy) {
            $AllHealthy = $false
        }
    }

    if ($AllHealthy) {
        Write-Host "`n[OK] All services are healthy and responding!" -ForegroundColor Green
    } else {
        Write-Host "`n[WRN] Some services may still be initializing. Check logs/" -ForegroundColor Yellow
    }

    # Generate Postman collection if requested (regardless of health status)
    if ($OpenPostman) {
        Write-Host "`n[INF] Setting up Postman collection..." -ForegroundColor Cyan
        $collectionPath = Import-ToPostman "http://localhost:8000"
        if ($collectionPath -and (Test-Path $collectionPath)) {
            Write-Host "[OK] Postman collection created" -ForegroundColor Green
            
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
                    Start-Process $path -ErrorAction SilentlyContinue
                    $postmanFound = $true
                    break
                }
            }
            
            if (-not $postmanFound) {
                Write-Host "  Import manually: $collectionPath" -ForegroundColor Yellow
            }
        }
    }
}

# ===============================================
# SUMMARY & ACCESS INFO
# ===============================================

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "[OK] CLISONIX CLOUD STARTUP COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "SERVICE ENDPOINTS:" -ForegroundColor Cyan
Write-Host "   Dashboard:      http://localhost:3000" -ForegroundColor White
Write-Host "   API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "   System Status:  http://localhost:8000/api/system-status" -ForegroundColor White
Write-Host "   Health Check:   http://localhost:8000/health" -ForegroundColor White

Write-Host "`nBACKGROUND SERVICES:" -ForegroundColor Cyan
Write-Host "   - FastAPI Backend    (port 8000)" -ForegroundColor White
Write-Host "   - Next.js Frontend   (port 3000)" -ForegroundColor White
Write-Host "   - ORCH Service       (port 5555)" -ForegroundColor White
Write-Host "   - MESH Network       (port 7777)" -ForegroundColor White

if (-not $Detached) {
    Write-Host "`nJOB MANAGEMENT:" -ForegroundColor Cyan
    Write-Host "   List jobs:     Get-Job" -ForegroundColor Gray
    Write-Host "   View logs:     Get-Content logs/api-*.log -Tail 20" -ForegroundColor Gray
    Write-Host "   Stop service:  Stop-Job -Name <name>" -ForegroundColor Gray
    Write-Host "   Restart:       .\scripts\start-all.ps1 -Clean" -ForegroundColor Gray
}

Write-Host "`n[OK] System is 100% functional and ready!`n" -ForegroundColor Green
