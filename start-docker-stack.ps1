# Clisonix Cloud - Start Docker & Monitoring Stack
# This script starts Docker, Grafana, Prometheus, and other services

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("all", "docker", "grafana", "prometheus", "mesh", "status")]
    [string]$Service = "all"
)

Write-Host "🐳 Clisonix Cloud - Docker & Monitoring Stack" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

Set-Location "C:\neurosonix-cloud"

function Start-AllServices {
    Write-Host "[1/4] Starting Docker Services..." -ForegroundColor Green
    docker-compose up -d
    Start-Sleep -Seconds 3
    
    Write-Host "`n[2/4] Starting Prometheus (metrics collection)..." -ForegroundColor Green
    Write-Host "  📍 http://localhost:9090" -ForegroundColor Cyan
    
    Write-Host "`n[3/4] Starting Grafana (dashboards)..." -ForegroundColor Green
    Write-Host "  📍 http://localhost:3001" -ForegroundColor Cyan
    Write-Host "  🔑 Default: admin/admin" -ForegroundColor Yellow
    
    Write-Host "`n[4/4] Mesh Cluster Status..." -ForegroundColor Green
    Write-Host "  To start mesh nodes, run: python mesh_cluster_startup.py" -ForegroundColor Yellow
}

function Start-Docker {
    Write-Host "Starting Docker services..." -ForegroundColor Green
    docker-compose up -d
    Start-Sleep -Seconds 2
    Write-Host "✓ Docker services started" -ForegroundColor Green
}

function Start-Grafana {
    Write-Host "Starting Grafana..." -ForegroundColor Green
    docker-compose up -d grafana
    Start-Sleep -Seconds 3
    Write-Host "✓ Grafana started at http://localhost:3001" -ForegroundColor Green
}

function Start-Prometheus {
    Write-Host "Starting Prometheus..." -ForegroundColor Green
    docker-compose up -d prometheus
    Start-Sleep -Seconds 2
    Write-Host "✓ Prometheus started at http://localhost:9090" -ForegroundColor Green
}

function Start-MeshNodes {
    Write-Host "Starting Mesh Cluster Nodes..." -ForegroundColor Green
    if (Test-Path ".\mesh_cluster_startup.py") {
        python mesh_cluster_startup.py
    } else {
        Write-Host "⚠️  mesh_cluster_startup.py not found" -ForegroundColor Yellow
    }
}

function Show-Status {
    Write-Host "📊 Service Status:" -ForegroundColor Cyan
    
    Write-Host "`n🌐 Frontend & API:" -ForegroundColor Green
    $frontendRunning = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue
    $apiRunning = Test-NetConnection -ComputerName localhost -Port 8000 -WarningAction SilentlyContinue
    Write-Host "  Frontend: $(if($frontendRunning.TcpTestSucceeded) {'✓ Running'} else {'✗ Stopped'})" -ForegroundColor $(if($frontendRunning.TcpTestSucceeded) {'Green'} else {'Red'})
    Write-Host "  API:      $(if($apiRunning.TcpTestSucceeded) {'✓ Running'} else {'✗ Stopped'})" -ForegroundColor $(if($apiRunning.TcpTestSucceeded) {'Green'} else {'Red'})
    
    Write-Host "`n🐳 Docker Services:" -ForegroundColor Green
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Execute requested service
switch ($Service) {
    "all" { Start-AllServices }
    "docker" { Start-Docker }
    "grafana" { Start-Grafana }
    "prometheus" { Start-Prometheus }
    "mesh" { Start-MeshNodes }
    "status" { Show-Status }
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "✅ Complete!" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Cyan
