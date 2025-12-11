#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start Clisonix Slack Integration Service with Production/Development modes

.DESCRIPTION
    Launches the Slack integration service with real-time monitoring capabilities.
    Supports multiple modes: full, monitor, test, deploy.

.PARAMETER WebhookUrl
    Your Slack webhook URL (from https://api.slack.com/messaging/webhooks)

.PARAMETER Mode
    Operation mode: full|monitor|test|deploy
    - full: Start service with all features
    - monitor: Monitor services only
    - test: Test webhook connectivity
    - deploy: Production deployment mode

.PARAMETER Environment
    Environment: production|development
    Default: production

.PARAMETER Channel
    Slack channel for notifications (default: #clisonix-monitoring)

.EXAMPLE
    .\start-slack.ps1 -WebhookUrl "https://hooks.slack.com/services/..." -Mode full

.EXAMPLE
    .\start-slack.ps1 -Mode test -WebhookUrl "your-webhook-url"

#>

param(
    [Parameter(Mandatory=$true)]
    [string]$WebhookUrl,

    [Parameter(Mandatory=$false)]
    [ValidateSet("full", "monitor", "test", "deploy")]
    [string]$Mode = "full",

    [Parameter(Mandatory=$false)]
    [ValidateSet("production", "development")]
    [string]$Environment = "production",

    [Parameter(Mandatory=$false)]
    [string]$Channel = "#clisonix-monitoring",

    [Parameter(Mandatory=$false)]
    [int]$Port = 8888
)

# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

function Write-Header {
    Write-Host "`n╔════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  CLISONIX SLACK INTEGRATION LAUNCHER      ║" -ForegroundColor Cyan
    Write-Host "║  v2.0.0 (FastAPI Lifespan Events)        ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error2 {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning2 {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Section {
    param([string]$Title)
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "  $Title" -ForegroundColor White -BackgroundColor DarkBlue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
}

function Test-WebhookUrl {
    param([string]$Url)
    
    if (-not $Url -or $Url -eq "") {
        return $false
    }
    
    if ($Url -notlike "https://hooks.slack.com/services/*") {
        return $false
    }
    
    return $true
}

function Test-Port-Available {
    param([int]$Port)
    
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("127.0.0.1", $Port)
        $connection.Close()
        return $false  # Port is in use
    }
    catch {
        return $true   # Port is available
    }
}

function Test-Dependencies {
    Write-Section "Checking Dependencies"
    
    $missing = @()
    
    # Check Python
    try {
        $python = python --version 2>&1
        Write-Success "Python: $python"
    }
    catch {
        $missing += "Python"
        Write-Error2 "Python not found"
    }
    
    # Check FastAPI
    try {
        python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')" 2>&1 | ForEach-Object {
            if ($_ -match "FastAPI") {
                Write-Success "FastAPI installed"
            }
        }
    }
    catch {
        $missing += "FastAPI"
        Write-Warning2 "FastAPI not installed (will be auto-installed)"
    }
    
    # Check aiohttp
    try {
        python -c "import aiohttp; print(f'aiohttp {aiohttp.__version__}')" 2>&1 | ForEach-Object {
            if ($_ -match "aiohttp") {
                Write-Success "aiohttp installed"
            }
        }
    }
    catch {
        $missing += "aiohttp"
        Write-Warning2 "aiohttp not installed (will be auto-installed)"
    }
    
    # Check pydantic
    try {
        python -c "import pydantic; print(f'Pydantic {pydantic.__version__}')" 2>&1 | ForEach-Object {
            if ($_ -match "Pydantic") {
                Write-Success "Pydantic installed"
            }
        }
    }
    catch {
        $missing += "Pydantic"
        Write-Warning2 "Pydantic not installed (will be auto-installed)"
    }
    
    if ($missing.Count -gt 0) {
        Write-Info "Installing missing dependencies..."
        pip install fastapi aiohttp pydantic uvicorn 2>&1 | Out-Null
        Write-Success "Dependencies installed"
    }
    
    return $true
}

function Test-Webhook-Connectivity {
    param([string]$WebhookUrl, [string]$Channel)
    
    Write-Section "Testing Webhook Connectivity"
    Write-Info "Sending test message to Slack..."
    
    $testPayload = @{
        channel = $Channel
        text = "✅ Clisonix Slack Integration - Webhook Test"
        blocks = @(
            @{
                type = "section"
                text = @{
                    type = "mrkdwn"
                    text = "*🧪 Webhook Connectivity Test*`nTime: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')`nStatus: ✅ OK"
                }
            }
        )
    }
    
    try {
        $response = curl -s -X POST -H 'Content-type: application/json' `
            --data ($testPayload | ConvertTo-Json -Depth 10) `
            $WebhookUrl
        
        Start-Sleep -Milliseconds 500
        
        if ($response -eq "ok") {
            Write-Success "Webhook connectivity verified ✅"
            return $true
        }
        else {
            Write-Error2 "Webhook test failed: $response"
            return $false
        }
    }
    catch {
        Write-Error2 "Webhook test error: $_"
        return $false
    }
}

function Start-Slack-Service {
    param(
        [string]$WebhookUrl,
        [string]$Channel,
        [string]$Environment,
        [int]$Port
    )
    
    Write-Section "Starting Slack Integration Service"
    
    # Set environment variables
    $env:SLACK_WEBHOOK_URL = $WebhookUrl
    $env:SLACK_CHANNEL = $Channel
    $env:SERVICE_MODE = $Environment
    $env:SLACK_PORT = $Port
    
    Write-Info "Configuration:"
    Write-Info "  Channel: $Channel"
    Write-Info "  Environment: $Environment"
    Write-Info "  Port: $Port"
    Write-Info "  Webhook: $(if ($WebhookUrl.Length -gt 50) { $WebhookUrl.Substring(0, 50) + '...' } else { $WebhookUrl })"
    
    # Start service in new window
    try {
        Write-Info "Launching service in new PowerShell window..."
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python slack_integration_service.py" -WindowStyle Normal
        
        Start-Sleep -Seconds 3
        Write-Success "Service started (PID in new window)"
        
        # Test health endpoint
        Start-Sleep -Seconds 2
        Write-Info "Verifying service health..."
        
        try {
            $health = curl -s http://localhost:$Port/health | ConvertFrom-Json
            Write-Success "Service is operational"
            Write-Success "Status: $($health.status)"
            Write-Success "Mode: $($health.mode)"
            return $true
        }
        catch {
            Write-Warning2 "Could not verify service health (it may still be starting)"
            return $true
        }
    }
    catch {
        Write-Error2 "Failed to start service: $_"
        return $false
    }
}

function Show-Configuration {
    param(
        [string]$WebhookUrl,
        [string]$Channel,
        [string]$Environment,
        [int]$Port
    )
    
    Write-Section "📋 Current Configuration"
    
    Write-Host "Webhook URL:      $(if ($WebhookUrl.Length -gt 60) { $WebhookUrl.Substring(0, 60) + '...' } else { $WebhookUrl })" -ForegroundColor White
    Write-Host "Channel:          $Channel" -ForegroundColor White
    Write-Host "Environment:      $Environment" -ForegroundColor White
    Write-Host "Port:             $Port" -ForegroundColor White
    Write-Host "Service Mode:     $Mode" -ForegroundColor White
    
    Write-Host ""
}

function Show-Endpoints {
    param([int]$Port)
    
    Write-Section "📍 API Endpoints"
    
    Write-Host "Base URL:                  http://localhost:$Port" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Health Check:              GET  /health" -ForegroundColor Green
    Write-Host "Service Health:            GET  /service-health" -ForegroundColor Green
    Write-Host "Status Report:             GET  /status-report" -ForegroundColor Green
    Write-Host "Send Alert:                POST /send-alert" -ForegroundColor Green
    Write-Host "Send Message:              POST /send-message" -ForegroundColor Green
    Write-Host "Metric Alert:              POST /metric-alert" -ForegroundColor Green
    Write-Host "Deployment Notification:   POST /notify-deployment" -ForegroundColor Green
    Write-Host ""
    Write-Host "API Docs:                  http://localhost:$Port/docs" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Next-Steps {
    Write-Section "🚀 Next Steps"
    
    Write-Host "1. Monitor in Slack:"
    Write-Host "   Check your Slack channel for alerts and status messages" -ForegroundColor DarkGray
    Write-Host ""
    
    Write-Host "2. Test endpoints:"
    Write-Host "   curl http://localhost:8888/health" -ForegroundColor DarkGray
    Write-Host "   curl http://localhost:8888/service-health" -ForegroundColor DarkGray
    Write-Host ""
    
    Write-Host "3. Send test message:"
    Write-Host "   curl http://localhost:8888/status-report" -ForegroundColor DarkGray
    Write-Host ""
    
    Write-Host "4. View API documentation:"
    Write-Host "   Open http://localhost:8888/docs in your browser" -ForegroundColor DarkGray
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════

Write-Header

# Validate webhook URL
if (-not (Test-WebhookUrl $WebhookUrl)) {
    Write-Error2 "Invalid webhook URL"
    Write-Info "Expected format: https://hooks.slack.com/services/T.../B.../X..."
    exit 1
}

# Check dependencies
Test-Dependencies | Out-Null

# Show configuration
Show-Configuration -WebhookUrl $WebhookUrl -Channel $Channel -Environment $Environment -Port $Port

# Handle different modes
switch ($Mode) {
    "test" {
        Write-Section "🧪 Testing Mode"
        if (Test-Webhook-Connectivity -WebhookUrl $WebhookUrl -Channel $Channel) {
            Write-Success "Webhook test successful"
        }
        exit 0
    }
    
    "monitor" {
        Write-Section "👀 Monitor Only Mode"
        Write-Info "Service will monitor but not send to Slack"
        Start-Slack-Service -WebhookUrl "" -Channel $Channel -Environment $Environment -Port $Port | Out-Null
    }
    
    "deploy" {
        Write-Section "🚀 Production Deploy Mode"
        Write-Info "Production configuration with webhook enabled"
        Start-Slack-Service -WebhookUrl $WebhookUrl -Channel $Channel -Environment "production" -Port $Port | Out-Null
    }
    
    default {
        # Full mode
        if (Test-Webhook-Connectivity -WebhookUrl $WebhookUrl -Channel $Channel) {
            Start-Slack-Service -WebhookUrl $WebhookUrl -Channel $Channel -Environment $Environment -Port $Port | Out-Null
        }
        else {
            Write-Error2 "Webhook test failed - cannot proceed"
            exit 1
        }
    }
}

# Show endpoints and next steps
Show-Endpoints -Port $Port
Show-Next-Steps

Write-Host ""
Write-Host "Service is now running. Press Ctrl+C in the service window to stop." -ForegroundColor Yellow
Write-Host ""
