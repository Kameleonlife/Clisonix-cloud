# Clisonix Cloud - Start All Services Script
# Stops all processes, cleans caches, then starts dev stack

Write-Host "[START-ALL] Initializing..." -ForegroundColor Cyan

# Kill existing Node processes
Write-Host "[CLEANUP] Stopping Node processes..." -ForegroundColor Yellow
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Kill existing Python processes
Write-Host "[CLEANUP] Stopping Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait for graceful shutdown
Start-Sleep -Seconds 2

# Navigate to project directory
Set-Location "C:\neurosonix-cloud"
Write-Host "[PATH] Working directory: $(Get-Location)" -ForegroundColor Cyan

# Clean Next.js cache
Write-Host "[CACHE] Cleaning Next.js build cache..." -ForegroundColor Yellow
Remove-Item -Path "apps/web/.next" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "[CACHE] Next.js cache cleaned" -ForegroundColor Green

# Clean npm cache (optional - faster startup)
Write-Host "[NPM] Using npm cache" -ForegroundColor Cyan

# Display startup info
Write-Host "" 
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "[READY] Starting Clisonix services..." -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Start dev stack (concurrent frontend + backend)
Write-Host "[RUN] Executing: npm run dev" -ForegroundColor Green
npm run dev
