#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════════════════
# CLISONIX CLOUD - UNIVERSAL LAUNCHER
# Multi-dimensional, multi-command startup system with auto port detection
# ═══════════════════════════════════════════════════════════════════════════

param(
    [Parameter(Position=0)]
    [ValidateSet("all", "frontend", "backend", "docker", "minimal", "full-stack", "clean")]
    [string]$Mode = "all",
    
    [Parameter()]
    [switch]$AutoPorts,
    
    [Parameter()]
    [switch]$CleanCache,
    
    [Parameter()]
    [int]$MinPort = 3000,
    
    [Parameter()]
    [int]$MaxPort = 9099
)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

$ProjectRoot = "C:\clisonix-cloud"
$Global:ServicePorts = @{}

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

function Write-Banner {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                                   ║" -ForegroundColor Cyan
    Write-Host "║              🚀 CLISONIX CLOUD - UNIVERSAL LAUNCHER 🚀            ║" -ForegroundColor Cyan
    Write-Host "║                                                                   ║" -ForegroundColor Cyan
    Write-Host "║                  Multi-Dimensional System Startup                 ║" -ForegroundColor Cyan
    Write-Host "║                                                                   ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Find-AvailablePort {
    param([int]$StartPort, [int]$EndPort)
    
    for ($port = $StartPort; $port -le $EndPort; $port++) {
        $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($null -eq $connection) {
            return $port
        }
    }
    Write-Host "❌ No available ports in range $StartPort-$EndPort" -ForegroundColor Red
    return $null
}

function Stop-AllServices {
    Write-Host "`n[1/6] 🛑 Stopping existing services..." -ForegroundColor Yellow
    
    # Stop Node.js processes
    $nodeProcesses = Get-Process | Where-Object {$_.ProcessName -match "node|next|npm"}
    if ($nodeProcesses) {
        $nodeProcesses | ForEach-Object {
            Write-Host "  Stopping: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    }
    
    # Stop Python processes (only project-related)
    $pythonProcesses = Get-Process | Where-Object {
        $_.ProcessName -match "python" -and $_.Path -like "*clisonix-cloud*"
    }
    if ($pythonProcesses) {
        $pythonProcesses | ForEach-Object {
            Write-Host "  Stopping: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    }
    
    Start-Sleep -Seconds 2
    Write-Host "  ✓ Cleanup complete" -ForegroundColor Green
}

function Clear-BuildCache {
    Write-Host "`n[2/6] 🧹 Cleaning build cache..." -ForegroundColor Yellow
    
    $nextCache = Join-Path $ProjectRoot "apps\web\.next"
    if (Test-Path $nextCache) {
        Remove-Item -Path $nextCache -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Next.js cache cleared" -ForegroundColor Green
    }
    
    $nodeModules = Join-Path $ProjectRoot "apps\web\node_modules\.cache"
    if (Test-Path $nodeModules) {
        Remove-Item -Path $nodeModules -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Node modules cache cleared" -ForegroundColor Green
    }
}

function Initialize-Ports {
    Write-Host "`n[3/6] 🔍 Detecting available ports..." -ForegroundColor Yellow
    
    if ($AutoPorts) {
        $Global:ServicePorts.Frontend = Find-AvailablePort -StartPort $MinPort -EndPort $MaxPort
        if ($null -eq $Global:ServicePorts.Frontend) { exit 1 }
        
        $Global:ServicePorts.Backend = Find-AvailablePort -StartPort ($Global:ServicePorts.Frontend + 1) -EndPort $MaxPort
        $Global:ServicePorts.Grafana = Find-AvailablePort -StartPort ($Global:ServicePorts.Backend + 1) -EndPort $MaxPort
        $Global:ServicePorts.Prometheus = Find-AvailablePort -StartPort ($Global:ServicePorts.Grafana + 1) -EndPort $MaxPort
    } else {
        # Use default ports
        $Global:ServicePorts.Frontend = 3000
        $Global:ServicePorts.Backend = 8000
        $Global:ServicePorts.Grafana = 3001
        $Global:ServicePorts.Prometheus = 9090
    }
    
    Write-Host "  ✓ Frontend:   $($Global:ServicePorts.Frontend)" -ForegroundColor Green
    Write-Host "  ✓ Backend:    $($Global:ServicePorts.Backend)" -ForegroundColor Green
    Write-Host "  ✓ Grafana:    $($Global:ServicePorts.Grafana)" -ForegroundColor Green
    Write-Host "  ✓ Prometheus: $($Global:ServicePorts.Prometheus)" -ForegroundColor Green
}

function Start-DockerServices {
    Write-Host "`n[4/6] 🐳 Starting Docker services..." -ForegroundColor Yellow
    
    Set-Location $ProjectRoot
    
    if ($AutoPorts) {
        # Create dynamic docker-compose file
        $dockerContent = Get-Content "docker-compose.prod.yml" -Raw
        
        $dockerContent = $dockerContent -replace '- "3001:3000"', "- `"$($Global:ServicePorts.Grafana):3000`""
        $dockerContent = $dockerContent -replace '- "9090:9090"', "- `"$($Global:ServicePorts.Prometheus):9090`""
        $dockerContent = $dockerContent -replace '- "8000:8000"', "- `"$($Global:ServicePorts.Backend):8000`""
        $dockerContent = $dockerContent -replace '- "5436:8000"', "- `"$($Global:ServicePorts.Backend):8000`""
        $dockerContent = $dockerContent -replace '- "3000:3000"', "- `"$($Global:ServicePorts.Frontend):3000`""
        
        $dockerContent | Set-Content "docker-compose.runtime.yml" -Force
        
        docker compose -f docker-compose.runtime.yml up -d 2>&1 | Out-Null
    } else {
        docker compose -f docker-compose.prod.yml up -d 2>&1 | Out-Null
    }
    
    Start-Sleep -Seconds 3
    Write-Host "  ✓ Docker services started" -ForegroundColor Green
}

function Start-Frontend {
    Write-Host "`n[5/6] 🌐 Starting Frontend..." -ForegroundColor Yellow
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        `$Host.UI.RawUI.WindowTitle = 'Clisonix Frontend - Port $($Global:ServicePorts.Frontend)';
        cd $ProjectRoot\apps\web;
        Write-Host '🌐 Frontend starting on port $($Global:ServicePorts.Frontend)...' -ForegroundColor Cyan;
        Write-Host '⚠️  Note: Next.js may have workspace bugs (ENOWORKSPACES)' -ForegroundColor Yellow;
        `$env:PORT = '$($Global:ServicePorts.Frontend)';
        npm run dev;
"@
    
    Write-Host "  ✓ Frontend launching on port $($Global:ServicePorts.Frontend)" -ForegroundColor Green
    Write-Host "  ⚠️  If frontend fails, backend API is still functional" -ForegroundColor Yellow
}

function Start-Backend {
    Write-Host "`n[6/6] ⚡ Starting Backend API (Python FastAPI)..." -ForegroundColor Yellow
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
        `$Host.UI.RawUI.WindowTitle = 'Clisonix Backend API - Port $($Global:ServicePorts.Backend)';
        cd $ProjectRoot\apps\api;
        Write-Host '⚡ Backend API starting on port $($Global:ServicePorts.Backend)...' -ForegroundColor Cyan;
        Write-Host '📦 Python FastAPI with 78+ endpoints' -ForegroundColor Green;
        python -m uvicorn main:app --host 127.0.0.1 --port $($Global:ServicePorts.Backend) --reload;
"@
    
    Write-Host "  ✓ Backend (Python) launching on port $($Global:ServicePorts.Backend)" -ForegroundColor Green
}
function Show-Summary {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                                   ║" -ForegroundColor Green
    Write-Host "║                    ✅ ALL SERVICES STARTED!                       ║" -ForegroundColor Green
    Write-Host "║                                                                   ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    
    Write-Host "`n🌐 Primary Services:" -ForegroundColor Cyan
    Write-Host "   Frontend (Next.js):  http://localhost:$($Global:ServicePorts.Frontend)" -ForegroundColor White
    Write-Host "   Backend (Python):    http://localhost:$($Global:ServicePorts.Backend)" -ForegroundColor White
    Write-Host "   API Docs (Swagger):  http://localhost:$($Global:ServicePorts.Backend)/docs" -ForegroundColor White
    Write-Host "   OpenAPI Schema:      http://localhost:$($Global:ServicePorts.Backend)/openapi.json" -ForegroundColor White
    
    Write-Host "`n📊 Monitoring Services:" -ForegroundColor Cyan
    Write-Host "   Grafana:             http://localhost:$($Global:ServicePorts.Grafana)" -ForegroundColor Gray
    Write-Host "   Prometheus:          http://localhost:$($Global:ServicePorts.Prometheus)" -ForegroundColor Gray
    Write-Host "   Metrics Endpoint:    http://localhost:$($Global:ServicePorts.Backend)/metrics" -ForegroundColor Gray
    
    Write-Host "`n🐳 Docker Microservices:" -ForegroundColor Cyan
    Write-Host "   Alba (AI Agent):        Port 5050" -ForegroundColor Gray
    Write-Host "   Albi (AI Agent):        Port 6060" -ForegroundColor Gray
    Write-Host "   Jona (AI Agent):        Port 7070" -ForegroundColor Gray
    Write-Host "   Orchestrator:           Port 9999" -ForegroundColor Gray
    
    Write-Host "`n💡 Tips:" -ForegroundColor Yellow
    Write-Host "   • Backend has 78+ endpoints (ASI, Brain, Fitness, ALBA, Reporting)" -ForegroundColor Gray
    Write-Host "   • Frontend may have Next.js workspace bugs - backend is standalone" -ForegroundColor Gray
    Write-Host "   • To stop Docker: docker compose -f docker-compose.$(if($AutoPorts){'runtime'}else{'prod'}).yml down" -ForegroundColor Gray
    Write-Host "   • All services run in separate windows - close manually or use Ctrl+C" -ForegroundColor Gray
    
    Write-Host "`n═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan
}   Write-Host "`n═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

Write-Banner

Set-Location $ProjectRoot

# Execute based on mode
switch ($Mode) {
    "all" {
        Stop-AllServices
        if ($CleanCache) { Clear-BuildCache }
        Initialize-Ports
        Start-DockerServices
        Start-Frontend
        Start-Backend
        Show-Summary
    }
    
    "frontend" {
        Stop-AllServices
        Initialize-Ports
        Start-Frontend
        Write-Host "`n✅ Frontend started on port $($Global:ServicePorts.Frontend)" -ForegroundColor Green
    }
    
    "backend" {
        Stop-AllServices
        Initialize-Ports
        Start-Backend
        Write-Host "`n✅ Backend started on port $($Global:ServicePorts.Backend)" -ForegroundColor Green
    }
    
    "docker" {
        Initialize-Ports
        Start-DockerServices
        Write-Host "`n✅ Docker services started" -ForegroundColor Green
    }
    
    "minimal" {
        Stop-AllServices
        Initialize-Ports
        Start-Frontend
        Start-Backend
        Write-Host "`n✅ Minimal stack started (Frontend + Backend only)" -ForegroundColor Green
    }
    
    "full-stack" {
        Stop-AllServices
        Clear-BuildCache
        Initialize-Ports
        Start-DockerServices
        Start-Frontend
        Start-Backend
        Show-Summary
    }
    
    "clean" {
        Stop-AllServices
        Clear-BuildCache
        Write-Host "`n✅ All services stopped and cache cleaned" -ForegroundColor Green
    }
}

Write-Host "`nPress Ctrl+C to exit (services will keep running)" -ForegroundColor Yellow
Write-Host "Monitoring services..." -ForegroundColor Gray

# Keep script alive to monitor
while ($true) {
    Start-Sleep -Seconds 10
}

