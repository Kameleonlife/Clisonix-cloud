# DNS IPv4-Only Verification Script
# Run this AFTER removing AAAA records from DNS

Write-Host "
╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     DNS IPv4-Only Verification Test                     ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# Test 1: DNS Lookup
Write-Host "1️⃣ DNS LOOKUP TEST:" -ForegroundColor Yellow
Write-Host "   Testing: www.clisonix.com
" -ForegroundColor Gray

$dnsResult = nslookup www.clisonix.com 2>&1 | Out-String

if ($dnsResult -match "AAAA") {
    Write-Host "   ❌ WARNING: AAAA record still exists!" -ForegroundColor Red
    Write-Host "   → Wait 5-10 more minutes for DNS propagation
" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Good: No AAAA record found" -ForegroundColor Green
}

if ($dnsResult -match "157\.90\.234\.158") {
    Write-Host "   ✅ IPv4 A record found: 157.90.234.158
" -ForegroundColor Green
} else {
    Write-Host "   ❌ IPv4 A record not found!
" -ForegroundColor Red
}

# Test 2: HTTP Connection
Write-Host "2️⃣ HTTP CONNECTION TEST:" -ForegroundColor Yellow
Write-Host "   Testing: http://www.clisonix.com
" -ForegroundColor Gray

try {
    $response = Invoke-WebRequest -Uri "http://www.clisonix.com" -TimeoutSec 10 -UseBasicParsing
    Write-Host "   ✅ HTTP connection successful!" -ForegroundColor Green
    Write-Host "   Status Code: $($response.StatusCode)" -ForegroundColor Gray
    Write-Host "   Content Length: $($response.Content.Length) bytes
" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ HTTP connection failed!" -ForegroundColor Red
    Write-Host "   Error: $_
" -ForegroundColor Red
}

# Test 3: HTTPS Connection
Write-Host "3️⃣ HTTPS CONNECTION TEST:" -ForegroundColor Yellow
Write-Host "   Testing: https://www.clisonix.com
" -ForegroundColor Gray

try {
    $response = Invoke-WebRequest -Uri "https://www.clisonix.com" -TimeoutSec 10 -UseBasicParsing
    Write-Host "   ✅ HTTPS connection successful!" -ForegroundColor Green
    Write-Host "   Status Code: $($response.StatusCode)" -ForegroundColor Gray
    Write-Host "   SSL: Valid
" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ HTTPS connection failed!" -ForegroundColor Red
    Write-Host "   Error: $_
" -ForegroundColor Red
}

# Test 4: DNS Propagation Check
Write-Host "4️⃣ DNS PROPAGATION CHECK:" -ForegroundColor Yellow
Write-Host "   Checking multiple DNS servers
" -ForegroundColor Gray

$dnsServers = @(
    @{Name="Google DNS"; IP="8.8.8.8"},
    @{Name="Cloudflare DNS"; IP="1.1.1.1"},
    @{Name="Quad9 DNS"; IP="9.9.9.9"}
)

foreach ($dns in $dnsServers) {
    try {
        $result = Resolve-DnsName -Name "www.clisonix.com" -Server $dns.IP -Type A -ErrorAction Stop
        if ($result) {
            Write-Host "   ✅ $($dns.Name): $($result.IPAddress)" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ⚠️ $($dns.Name): Not yet propagated" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "
╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    TEST SUMMARY                          ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

if ($dnsResult -notmatch "AAAA" -and $dnsResult -match "157\.90\.234\.158") {
    Write-Host "   🎉 SUCCESS! IPv4-only DNS is working!" -ForegroundColor Green
    Write-Host "   ✅ AAAA records removed" -ForegroundColor Green
    Write-Host "   ✅ A record active" -ForegroundColor Green
    Write-Host "   ✅ www.clisonix.com should work in browser now
" -ForegroundColor Green
} else {
    Write-Host "   ⏳ DNS changes still propagating..." -ForegroundColor Yellow
    Write-Host "   → Wait 5-10 more minutes and run this script again
" -ForegroundColor Yellow
}

Write-Host "   Run this script again with:" -ForegroundColor Gray
Write-Host "   .\test-dns-ipv4.ps1
" -ForegroundColor Cyan
