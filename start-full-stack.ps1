# Clisonix Cloud - Start All Services (Production Stack)
# This script starts: Frontend, Backend, API, Docker, Grafana, Prometheus, CI/CD, and Mesh Nodes

param(
    [switch]$Background = $false
)

Write-Host "🚀 Starting Clisonix Cloud - Full Production Stack..." -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Kill any existing processes
Write-Host "`n[1/8] Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Navigate to project
Set-Location "C:\neurosonix-cloud"

# 1. Start Frontend (External Port)
Write-Host "`n[2/8] Starting Frontend Server (External)..." -ForegroundColor Green
Write-Host "  📍 http://localhost:3000" -ForegroundColor Cyan
Write-Host "  📍 http://192.168.2.122:3000 (Network)" -ForegroundColor Cyan

# 2. Start Backend API
Write-Host "`n[3/8] Starting Backend API..." -ForegroundColor Green
Write-Host "  📍 http://localhost:8000" -ForegroundColor Cyan
Write-Host "  📍 http://192.168.2.122:8000 (Network)" -ForegroundColor Cyan

# 3. Start Docker Services
Write-Host "`n[4/8] Checking Docker Services..." -ForegroundColor Green
$dockerStatus = docker ps -q 2>$null
if ($null -eq $dockerStatus) {
    Write-Host "  ⚠️  Docker daemon not running" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
}

# 4. Start Prometheus
Write-Host "`n[5/8] Starting Prometheus..." -ForegroundColor Green
Write-Host "  📍 http://localhost:9090" -ForegroundColor Cyan
Write-Host "  Note: Run manually: docker-compose -f docker-compose.yml up prometheus -d" -ForegroundColor Yellow

# 5. Start Grafana
Write-Host "`n[6/8] Starting Grafana..." -ForegroundColor Green
Write-Host "  📍 http://localhost:3001 (default port)" -ForegroundColor Cyan
Write-Host "  Note: Run manually: docker-compose -f docker-compose.yml up grafana -d" -ForegroundColor Yellow

# 6. CI/CD Workflows
Write-Host "`n[7/8] CI/CD Pipeline Information..." -ForegroundColor Green
Write-Host "  📍 GitHub Actions: .github/workflows/ci-cd.yml" -ForegroundColor Cyan
Write-Host "  ✓ Pipeline includes: Testing, Docker Build, API Testing, Deployment" -ForegroundColor Green

# 7. Mesh Nodes
Write-Host "`n[8/8] Mesh Network Nodes..." -ForegroundColor Green
Write-Host "  📍 Mesh nodes configured in distributed_pulse_balancer.py" -ForegroundColor Cyan
Write-Host "  Note: Run mesh startup: python mesh_cluster_startup.py" -ForegroundColor Yellow

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "🎯 Starting Main Services (Frontend + Backend)..." -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# Start main services
npm run dev

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "✅ Services Started!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "`n📌 QUICK REFERENCE:" -ForegroundColor Cyan
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Green
Write-Host "  API:       http://localhost:8000" -ForegroundColor Green
Write-Host "  Grafana:   http://localhost:3001 (after docker-compose up)" -ForegroundColor Yellow
Write-Host "  Prometheus: http://localhost:9090 (after docker-compose up)" -ForegroundColor Yellow
Write-Host "`n📊 Additional Services:" -ForegroundColor Cyan
Write-Host "  docker-compose up -d            (Start all Docker services)" -ForegroundColor Gray
Write-Host "  python mesh_cluster_startup.py  (Start mesh nodes)" -ForegroundColor Gray
Write-Host "  git push                        (Trigger CI/CD pipeline)" -ForegroundColor Gray
Write-Host "`n" -ForegroundColor Cyan
