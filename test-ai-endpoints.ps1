# Test AI Agent Endpoints
# Run: .\test-ai-endpoints.ps1

$BaseUrl = "http://localhost:8000"
$ErrorActionPreference = "SilentlyContinue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧠 CLISONIX AI AGENTS TEST SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Agents Status
Write-Host "TEST 1: AI Agents Status" -ForegroundColor Yellow
Write-Host "Endpoint: GET /api/ai/agents-status" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/api/ai/agents-status" -UseBasicParsing -TimeoutSec 5
    $data = $response.Content | ConvertFrom-Json
    
    Write-Host "✅ SUCCESS" -ForegroundColor Green
    Write-Host "Frameworks Available:" -ForegroundColor Cyan
    Write-Host "  - CrewAI: $(if($data.frameworks.crewai.available) {'✅ READY'} else {'❌ Not available'})" -ForegroundColor Gray
    Write-Host "  - LangChain: $(if($data.frameworks.langchain.available) {'✅ READY'} else {'❌ Not available'})" -ForegroundColor Gray
    Write-Host "  - Claude Tools: $(if($data.frameworks.claude_tools.available) {'✅ READY'} else {'❌ Not available'})" -ForegroundColor Gray
    Write-Host "  - OpenAI Configured: $(if($data.openai_configured) {'✅ YES'} else {'❌ NO'})" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Trinity Analysis (CrewAI)
Write-Host "TEST 2: CrewAI Trinity Analysis" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/ai/trinity-analysis" -ForegroundColor Gray
try {
    $body = @{
        query = "Analyze ALBA network performance"
        detailed = $false
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$BaseUrl/api/ai/trinity-analysis" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -UseBasicParsing `
        -TimeoutSec 10
    
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ SUCCESS" -ForegroundColor Green
    Write-Host "Status: $($data.status)" -ForegroundColor Cyan
    Write-Host "Source: $($data.source)" -ForegroundColor Cyan
    Write-Host "Message: $($data.message -or $data.analysis -or 'Analysis complete')" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Curiosity Ocean (LangChain)
Write-Host "TEST 3: LangChain Curiosity Ocean" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/ai/curiosity-ocean" -ForegroundColor Gray
try {
    $body = @{
        question = "How does neural synthesis work?"
        conversation_id = "test-$(Get-Random)"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$BaseUrl/api/ai/curiosity-ocean" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -UseBasicParsing `
        -TimeoutSec 10
    
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ SUCCESS" -ForegroundColor Green
    Write-Host "Status: $($data.status)" -ForegroundColor Cyan
    Write-Host "Conversation ID: $($data.conversation_id)" -ForegroundColor Cyan
    Write-Host "Response: $($data.response -or $data.demo_response -or 'Chat response received')" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Quick Interpret (Claude Tools)
Write-Host "TEST 4: Claude Tools - Quick Interpret" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/ai/quick-interpret" -ForegroundColor Gray
try {
    $body = @{
        query = "What does alpha wave dominance indicate?"
        context = "EEG analysis"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$BaseUrl/api/ai/quick-interpret" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -UseBasicParsing `
        -TimeoutSec 10
    
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ SUCCESS" -ForegroundColor Green
    Write-Host "Status: $($data.status)" -ForegroundColor Cyan
    Write-Host "Source: $($data.source)" -ForegroundColor Cyan
    Write-Host "Interpretation: $($data.interpretation -or $data.demo_response -or 'Quick analysis complete')" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ AI ENDPOINTS TEST COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available Endpoints:" -ForegroundColor Yellow
Write-Host "  GET  /api/ai/agents-status" -ForegroundColor Gray
Write-Host "  POST /api/ai/trinity-analysis" -ForegroundColor Gray
Write-Host "  POST /api/ai/curiosity-ocean" -ForegroundColor Gray
Write-Host "  POST /api/ai/quick-interpret" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  📄 AI_AGENT_FRAMEWORKS.md" -ForegroundColor Gray
Write-Host "  📄 N8N_WORKFLOWS.json" -ForegroundColor Gray
Write-Host ""

