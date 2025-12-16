<#
 PowerShell helper to apply Cloudflare settings examples.
 Edit $ZoneId and $ApiToken before running.

 Usage:
  .\scripts\cloudflare_apply_examples.ps1 -ZoneId <zone> -ApiToken <token>
#>

param(
    [string]$ZoneId = $null,
    [string]$ApiToken = $null,
    [string]$ApiUrl = '*/api/ask*',
    [switch]$DryRun
)

function Set-CFUnderAttack {
    param($ZoneId, $ApiToken, [switch]$DryRun)
    $uri = "https://api.cloudflare.com/client/v4/zones/$ZoneId/settings/security_level"
    $body = @{ value = 'under_attack' } | ConvertTo-Json
    Write-Host "Setting security_level -> under_attack for zone $ZoneId"
    $headers = @{ "Authorization" = "Bearer $ApiToken"; "Content-Type" = "application/json" }
    if ($DryRun.IsPresent) {
        Write-Host "[DryRun] PATCH $uri"
        Write-Host "Headers: " ($headers | ConvertTo-Json)
        Write-Host "Body: " ($body | ConvertTo-Json)
        return
    }
    try {
        Invoke-RestMethod -Method Patch -Uri $uri -Headers $headers -Body $body
    } catch {
        Write-Error "Failed to set Under Attack: $_"
    }
}

function New-CFFirewallRuleAdminLock {
    param($ZoneId, $ApiToken, $OfficeIp, [switch]$DryRun)
    $uri = "https://api.cloudflare.com/client/v4/zones/$ZoneId/firewall/rules"
    # Cloudflare expression requires the IP(s) inside braces: {1.2.3.4/32}
    $expr = '(http.request.uri.path contains "/admin") and not ip.src in {{{0}}}' -f $OfficeIp
    $rule = @{
        action = 'block';
        filter = @{ expression = $expr; paused = $false; description = 'Block admin except office' };
        description = 'Block admin paths from non-office IPs'
    }
    $payload = @($rule) | ConvertTo-Json -Depth 6
    Write-Host "Creating firewall rule (admin lock)"
    $headers = @{ "Authorization" = "Bearer $ApiToken"; "Content-Type" = "application/json" }
    if ($DryRun.IsPresent) {
        Write-Host "[DryRun] POST $uri"
        Write-Host "Headers: " ($headers | ConvertTo-Json)
        Write-Host "Body: " ($payload | ConvertTo-Json)
        return
    }
    try {
        Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $payload
    } catch {
        Write-Error "Failed to create firewall rule: $_"
    }
}

function New-CFRateLimitApiAsk
 {
    param($ZoneId, $ApiToken, [switch]$DryRun)
    $uri = "https://api.cloudflare.com/client/v4/zones/$ZoneId/rate_limits"
    $payload = @{ 
        threshold = 10;
        period = 10;
        action = @{ mode = 'block'; timeout = 60 };
        match = @{ request = @{ methods = @('POST'); schemes = @('HTTP','HTTPS'); url = $ApiUrl } };
        enabled = $true;
        description = 'Protect /api/ask'
    } | ConvertTo-Json -Depth 6
    Write-Host "Creating rate-limit for /api/ask"
    $headers = @{ "Authorization" = "Bearer $ApiToken"; "Content-Type" = "application/json" }
    if ($DryRun.IsPresent) {
        Write-Host "[DryRun] POST $uri"
        Write-Host "Headers: " ($headers | ConvertTo-Json)
        Write-Host "Body: " ($payload | ConvertTo-Json)
        return
    }
    try {
        Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $payload
    } catch {
        Write-Error "Failed to create rate limit: $_"
    }
}

# Example usage - uncomment the calls you want to run
# Set-CFUnderAttack -ZoneId $ZoneId -ApiToken $ApiToken
# New-CFFirewallRuleAdminLock -ZoneId $ZoneId -ApiToken $ApiToken -OfficeIp '1.2.3.4/32'
# New-CFRateLimitApiAsk -ZoneId $ZoneId -ApiToken $ApiToken

Write-Host "Script loaded. Provide -ZoneId and -ApiToken and uncomment desired function calls at bottom or call functions interactively."

function Invoke-CFApplyAll {
    param($ZoneId, $ApiToken, $OfficeIp, [switch]$DryRun)
    Write-Host "Applying Cloudflare baseline (UnderAttack, Admin lock, RateLimit) - DryRun=$($DryRun.IsPresent)"
    Set-CFUnderAttack -ZoneId $ZoneId -ApiToken $ApiToken -DryRun:$DryRun
    New-CFFirewallRuleAdminLock -ZoneId $ZoneId -ApiToken $ApiToken -OfficeIp $OfficeIp -DryRun:$DryRun
    New-CFRateLimitApiAsk -ZoneId $ZoneId -ApiToken $ApiToken -DryRun:$DryRun
}

