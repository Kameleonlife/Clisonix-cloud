#!/usr/bin/env pwsh
<#
.SYNOPSIS
  CLISONIX CLOUD - SLACK INTEGRATION LAUNCHER
  Start Slack monitoring, alerts, and notifications service

.DESCRIPTION
  Launches the Slack integration service with:
  - Real-time service monitoring
  - Automated health alerts
  - Deployment notifications
  - Custom messaging capabilities

.EXAMPLE
  .\start-slack.ps1
  .\start-slack.ps1 -WebhookUrl "https://hooks.slack.com/services/YOUR/URL"
  .\start-slack.ps1 -Mode "monitor" -Channel "#alerts"
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$WebhookUrl = $env:SLACK_WEBHOOK_URL,
    
    [Parameter(Mandatory = $false)]
    [string]$BotToken = $env:SLACK_BOT_TOKEN,
    
    [Parameter(Mandatory = $false)]
    [string]$Channel = "#clisonix-monitoring",
    
    [Parameter(Mandatory = $false)]
    [ValidateSet("full", "monitor", "test")]
    [string]$Mode = "full",
    
    [Parameter(Mandatory = $false)]
    [int]$Port = 8888,
    
    [Parameter(Mandatory = $false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory = $false)]
    [switch]$Help
)

function Write-Header {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  CLISONIX CLOUD - SLACK INTEGRATION LAUNCHER                  ║" -ForegroundColor Cyan
    Write-Host "║  Real-time Monitoring & Automated Alerts                      ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Section {
    param([string]$Title)
    Write-Host "┌─ $Title" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "│  ℹ️  $Message" -ForegroundColor Gray
}

function Write-Success {
    param([string]$Message)
    Write-Host "│  ✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "│  ⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "│  ❌ $Message" -ForegroundColor Red
}

function Write-Divider {
    Write-Host "└─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
}

function Show-Help {
    Write-Header
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\start-slack.ps1 [Options]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -WebhookUrl <string>   Slack webhook URL (required for messaging)"
    Write-Host "  -BotToken <string>     Slack bot token (optional)"
    Write-Host "  -Channel <string>      Slack channel name (default: #clisonix-monitoring)"
    Write-Host "  -Mode <string>         Operation mode: full|monitor|test (default: full)"
    Write-Host "  -Port <int>            Service port (default: 8888)"
    Write-Host "  -DryRun               Show what would execute without running"
    Write-Host "  -Help                 Show this help message"
    Write-Host ""
    Write-Host "MODES:" -ForegroundColor Yellow
    Write-Host "  full      Start all Slack integration features"
    Write-Host "  monitor   Start service health monitoring only"
    Write-Host "  test      Test Slack connectivity and send test message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\start-slack.ps1 -WebhookUrl 'https://hooks.slack.com/...'"
    Write-Host "  .\start-slack.ps1 -Mode test"
    Write-Host "  .\start-slack.ps1 -Mode monitor -Channel '#alerts' -Port 9888"
    Write-Host ""
    exit 0
}

if ($Help) { Show-Help }

Write-Header

# Pre-flight checks
Write-Section "PRE-FLIGHT CHECKS"

# Check Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Python found: $pythonVersion"
} else {
    Write-Error-Custom "Python not found. Install Python 3.8+"
    exit 1
}

# Check FastAPI
Write-Info "Checking FastAPI..."
$fastApiCheck = pip list 2>&1 | Select-String "fastapi"
if ($fastApiCheck) {
    Write-Success "FastAPI installed"
} else {
    Write-Warning "FastAPI not found. Installing..."
    pip install fastapi uvicorn aiohttp -q
}

# Check for webhook URL
if (-not $WebhookUrl -or $WebhookUrl -eq "") {
    Write-Warning "No Slack webhook URL provided"
    Write-Info "Set via: -WebhookUrl or \$env:SLACK_WEBHOOK_URL"
    Write-Info "Get webhook from: https://api.slack.com/messaging/webhooks"
}

Write-Divider

# Set environment variables
$env:SLACK_WEBHOOK_URL = $WebhookUrl
$env:SLACK_BOT_TOKEN = $BotToken
$env:SLACK_CHANNEL = $Channel
$env:SLACK_PORT = $Port

# Build startup info
Write-Section "CONFIGURATION"
Write-Info "Channel: $Channel"
Write-Info "Port: $Port"
Write-Info "Mode: $Mode"
if ($WebhookUrl -and $WebhookUrl -ne "") {
    Write-Success "Webhook configured"
} else {
    Write-Warning "Webhook not configured"
}
Write-Divider

# Test mode
if ($Mode -eq "test") {
    Write-Section "TEST MODE"
    Write-Info "Testing Slack connectivity..."
    
    $testScript = @"
import asyncio
import aiohttp
import json
from datetime import datetime

async def test_webhook():
    webhook_url = '$WebhookUrl'
    
    if not webhook_url or 'hooks.slack.com' not in webhook_url:
        print('❌ No valid webhook URL provided')
        return False
    
    payload = {
        'text': '✅ Clisonix Cloud Slack Integration Test',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '✅ *Clisonix Cloud* Slack Integration\n*Test Status:* Connected\n*Time:* ' + datetime.utcnow().isoformat()
                }
            }
        ]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as resp:
                if resp.status == 200:
                    print('✅ Webhook test successful')
                    return True
                else:
                    print(f'❌ Webhook returned status {resp.status}')
                    return False
    except Exception as e:
        print(f'❌ Test failed: {e}')
        return False

asyncio.run(test_webhook())
"@
    
    if ($DryRun) {
        Write-Info "DRY RUN - Would execute test"
    } else {
        $testScript | python
    }
    exit 0
}

# Monitor mode
if ($Mode -eq "monitor") {
    Write-Section "MONITOR MODE"
    Write-Info "Starting service health monitoring..."
    Write-Divider
    
    $command = "python slack_integration_service.py"
    
    if ($DryRun) {
        Write-Info "DRY RUN - Command:"
        Write-Info "  $command"
    } else {
        & $command
    }
    exit
}

# Full mode
Write-Section "STARTUP SEQUENCE"

$services = @(
    @{ Name = "Slack Integration Service"; Cmd = "python slack_integration_service.py"; Wait = 3 }
)

foreach ($service in $services) {
    Write-Info "Starting $($service.Name) on port $Port..."
    
    if ($DryRun) {
        Write-Info "  Command: $($service.Cmd)"
        Write-Info "  Port: $Port"
        Write-Info "  Wait: $($service.Wait)s"
    } else {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $service.Cmd -WindowStyle Normal
        Start-Sleep -Seconds $service.Wait
    }
    
    Write-Success "$($service.Name) started"
}

Write-Divider

# Success message
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ SLACK INTEGRATION ONLINE                                  ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host ""
Write-Host "SERVICE ENDPOINTS:" -ForegroundColor Cyan
Write-Host "  📱 Slack Integration    → http://localhost:$Port"
Write-Host "  📡 Health Check         → http://localhost:$Port/health"
Write-Host "  📊 Status Report        → POST http://localhost:$Port/status-report"
Write-Host "  🔔 Send Alert           → POST http://localhost:$Port/send-alert"
Write-Host "  💬 Send Message         → POST http://localhost:$Port/send-message"
Write-Host ""
Write-Host "QUICK COMMANDS:" -ForegroundColor Cyan
Write-Host "  Get Status:"
Write-Host "    curl http://localhost:$Port/service-health"
Write-Host ""
Write-Host "  Send Alert:"
Write-Host "    curl -X POST http://localhost:$Port/send-alert \"
Write-Host '      -H "Content-Type: application/json" \'
Write-Host '      -d ''{ "service": "alba", "severity": "warning", "title": "Test", "message": "Test alert" }'''
Write-Host ""
Write-Host "INTEGRATION FEATURES:" -ForegroundColor Yellow
Write-Host "  🔄 Real-time Service Monitoring (60s interval)"
Write-Host "  🚨 Automated Health Alerts"
Write-Host "  📊 Status Reports"
Write-Host "  🚀 Deployment Notifications"
Write-Host "  📈 Metric Threshold Alerts"
Write-Host "  💬 Custom Messaging"
Write-Host ""
Write-Host "MONITORING SERVICES:" -ForegroundColor Yellow
Write-Host "  🔵 ALBA (Port 5555) - Network Telemetry"
Write-Host "  🟣 ALBI (Port 6666) - Neural Analytics"
Write-Host "  🟡 JONA (Port 7777) - Data Synthesis"
Write-Host "  ⚙️  Orchestrator (Port 9999) - Service Registry"
Write-Host "  📡 API (Port 8000) - Main API"
Write-Host ""
Write-Host "✅ Ready to send Slack notifications!"
Write-Host ""
