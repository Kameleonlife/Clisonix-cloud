# 🔐 Setup Docker Secrets
# Creates secret files from .secrets file
# Run this before docker-compose up with secrets

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "`n🔐 Docker Secrets Setup Script" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if .secrets file exists
if (-not (Test-Path ".secrets")) {
    Write-Host "❌ Error: .secrets file not found!" -ForegroundColor Red
    Write-Host "`nPlease create .secrets file first:" -ForegroundColor Yellow
    Write-Host "  1. Copy .secrets.template to .secrets" -ForegroundColor Yellow
    Write-Host "  2. Fill in all secret values" -ForegroundColor Yellow
    Write-Host "  3. Run this script again`n" -ForegroundColor Yellow
    exit 1
}

# Create secrets directory
$secretsDir = "secrets"
if (-not (Test-Path $secretsDir)) {
    New-Item -ItemType Directory -Path $secretsDir | Out-Null
    Write-Host "✓ Created secrets/ directory" -ForegroundColor Green
}

# Load .secrets file
Write-Host "📖 Reading .secrets file..." -ForegroundColor Yellow
$secrets = @{}
Get-Content ".secrets" | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
        $parts = $line.Split("=", 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim()
        if ($value) {
            $secrets[$key] = $value
        }
    }
}

Write-Host "✓ Found $($secrets.Count) secrets`n" -ForegroundColor Green

# Required secrets mapping
$requiredSecrets = @{
    "postgres_password" = "POSTGRES_PASSWORD"
    "redis_password" = "REDIS_PASSWORD"
    "minio_root_password" = "MINIO_ROOT_PASSWORD"
    "elasticsearch_password" = "ELASTICSEARCH_PASSWORD"
    "grafana_admin_password" = "GF_SECURITY_ADMIN_PASSWORD"
    "jwt_secret_key" = "JWT_SECRET_KEY"
    "stripe_secret_key" = "STRIPE_SECRET_KEY"
    "sepa_iban" = "SEPA_IBAN"
}

# Create secret files
Write-Host "📝 Creating secret files...`n" -ForegroundColor Yellow

$created = 0
$skipped = 0
$errors = 0

foreach ($secretFile in $requiredSecrets.Keys) {
    $envVar = $requiredSecrets[$secretFile]
    $filePath = Join-Path $secretsDir "$secretFile.txt"
    
    if ($secrets.ContainsKey($envVar)) {
        $value = $secrets[$envVar]
        
        # Check if file already exists
        if ((Test-Path $filePath) -and -not $Force) {
            Write-Host "  ⏭️  Skipped: $secretFile (already exists)" -ForegroundColor Gray
            $skipped++
        } else {
            # Create secret file
            $value | Out-File -FilePath $filePath -NoNewline -Encoding UTF8
            
            # Set restrictive permissions (Windows)
            $acl = Get-Acl $filePath
            $acl.SetAccessRuleProtection($true, $false)
            $adminRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                "Administrators", "FullControl", "Allow"
            )
            $acl.SetAccessRule($adminRule)
            Set-Acl $filePath $acl
            
            Write-Host "  ✓ Created: $secretFile" -ForegroundColor Green
            $created++
        }
    } else {
        Write-Host "  ❌ Missing: $envVar in .secrets file" -ForegroundColor Red
        $errors++
    }
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✓ Created: $created" -ForegroundColor Green
Write-Host "⏭️  Skipped: $skipped" -ForegroundColor Gray
Write-Host "❌ Errors: $errors`n" -ForegroundColor Red

if ($errors -gt 0) {
    Write-Host "⚠️  Some secrets are missing. Please add them to .secrets file.`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ All secrets configured successfully!`n" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify secrets/ directory is in .gitignore" -ForegroundColor Yellow
Write-Host "  2. Run: docker-compose -f docker-compose.secrets.yml up -d`n" -ForegroundColor Yellow

