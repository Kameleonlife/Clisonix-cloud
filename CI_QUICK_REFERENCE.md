# 🚀 Clisonix Cloud - Quick Reference Guide

## Pipeline Status at a Glance

```
ci.yml (Smart Pipeline - ACTIVE)
├── 🎯 Code Quality & Tests          [⚠️  warnings = continue]
├── 🔍 CodeQL v3 Analysis            [⚠️  warnings = continue]
├── 🔐 Secret Detection              [🔴 FAIL immediately]
├── ⚙️  Environment Variables        [🔴 FAIL critical only]
├── 🐳 Container Security (Trivy)    [🔴 FAIL CRITICAL/HIGH]
├── 🛡️  Policy Compliance (OPA)     [⚠️  warnings = continue]
└── 📊 Security Report Summary        [Report only]

ultra-security.yml (Weekly Supply Chain - ACTIVE)
├── 📦 Dependency Intelligence (CodeQL v3)
├── 🔍 Secret Detection (Gitleaks + TruffleHog)
├── 🛡️  Policy Gates (OPA/Conftest)
├── 🐳 Container Image Security (Trivy)
├── 📋 SBOM & Provenance (Syft + SLSA)
├── ⚙️  Environment Guardrails
└── 📊 Build Summary Report
```

---

## What Blocks the Pipeline (🔴 Critical)

1. **Secrets Detected**
   - Any pattern matching Gitleaks rules
   - → Instant fail (0 second SLA)

2. **Critical Environment Variables Missing**
   - DB_HOST, DB_USER, DB_PASSWORD, JWT_SECRET, API_KEY
   - → Instant fail

3. **CRITICAL or HIGH Vulnerabilities**
   - Container CVE ≥ 7.0 (HIGH) or ≥ 9.0 (CRITICAL)
   - → Instant fail

4. **CodeQL Critical Issues**
   - SAST findings (Python/JavaScript)
   - → May fail depending on severity

---

## What Warns But Doesn't Block (⚠️ Non-blocking)

1. **Linting Issues**
   - Code style violations
   - → Logged in report

2. **Unit Test Failures**
   - Test failures
   - → Logged in report

3. **Optional Environment Variables**
   - STRIPE_API_KEY, SENTRY_DSN, SLACK_WEBHOOK missing
   - → Logged as warning

4. **MEDIUM/LOW Vulnerabilities**
   - CVE score < 7.0
   - → Logged in report

5. **Policy Violations**
   - OPA/Conftest findings (e.g., non-root user)
   - → Logged but non-blocking

---

## Critical Environment Variables

| Variable | Purpose | Where | Example |
|----------|---------|-------|---------|
| DB_HOST | Database hostname | .env | localhost or 157.90.234.158 |
| DB_USER | Database username | .env | clisonix_user |
| DB_PASSWORD | Database password | .env | $(openssl rand -base64 32) |
| JWT_SECRET | JWT signing key | .env | $(openssl rand -base64 48) |
| API_KEY | Internal API key | .env | Generated |

All others are **optional** and trigger warnings only.

---

## How to Add Environment Variables

1. **Add to .env.example**
   ```bash
   echo "NEW_VAR=value_or_placeholder" >> .env.example
   git add .env.example
   ```

2. **Add to local .env** (never commit)
   ```bash
   echo "NEW_VAR=your_actual_value" >> .env
   # .env is in .gitignore, safe
   ```

3. **Add to GitHub Actions Secrets** (for CI/CD)
   - GitHub → Settings → Secrets and variables → Actions
   - Name: `PROD_NEW_VAR` or `STAGING_NEW_VAR`
   - Value: Your actual secret

4. **Reference in workflow**
   ```yaml
   env:
     NEW_VAR: ${{ secrets.PROD_NEW_VAR }}
   ```

---

## Commit Message Convention

```bash
git commit -m "type: Short description

Optional longer description with details.

[BREAKING CHANGE: description if API changed]"
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `chore:` Dependencies, config
- `refactor:` Code restructure
- `perf:` Performance improvement
- `sec:` Security fix

**Example:**
```bash
git commit -m "feat: Add JWT token validation

- Added JwtMiddleware to verify tokens
- Tokens expire after 24 hours
- Added /auth/refresh endpoint for renewal

[BREAKING CHANGE: /api/protected now requires Authorization header]"
```

---

## Debug Failed Pipeline

### If **Secrets Detected** ❌
1. Check Gitleaks output in GitHub Actions
2. Find the line with the exposed secret
3. Remove it and force-push: `git push --force-with-lease`
4. Rotate the exposed secret immediately (use SECURITY.md protocol)

### If **Critical Var Missing** ❌
1. Add to .env locally
2. Add to GitHub Secrets
3. Commit code with var reference
4. Check SECURITY.md for var definition

### If **Vulnerability Found** ❌
1. View Trivy report in GitHub Security tab
2. Update vulnerable dependency to patched version
3. Run: `pip install --upgrade <package>` or `npm update <package>`
4. Test locally, commit, push

### If **CodeQL Issue** ⚠️
1. View in GitHub Security → Code scanning
2. Click issue to see code and suggestion
3. Fix the code issue
4. Commit and push

---

## SARIF Reports (GitHub Security Tab)

All security findings upload to **GitHub → Security → Code scanning**:
- CodeQL findings (SAST)
- Trivy findings (container vulnerabilities)
- Secret detection (if found)

**To view:**
1. Go to repo → Security tab
2. Click "Code scanning" → "Alerts"
3. Filter by severity: CRITICAL, HIGH, MEDIUM, LOW
4. Click alert to see code context and remediation

---

## Policies & Standards

- **OWASP**: Secure supply chain (SBOM, signatures, provenance)
- **ISO 27001**: Information security (secret management, audit logs)
- **GDPR**: Personal data protection (PII redaction in logs)
- **PCI-DSS**: Payment card security (credential encryption)

See **SECURITY.md** for complete policy document.

---

## Emergency Contacts

| Issue | Contact | Response Time |
|-------|---------|---|
| Secret exposed | security@clisonix.com | < 1 hour |
| Critical vuln | devops@clisonix.com | < 4 hours |
| Policy question | team-lead@clisonix.com | < 24 hours |

---

## Useful Commands

```bash
# Test pipeline locally
npm run lint && npm test

# Build Docker image locally
docker build -t clisonix-cloud:test .

# Scan image locally (if Trivy installed)
trivy image clisonix-cloud:test

# Check for secrets locally (if Gitleaks installed)
gitleaks detect --source local --verbose

# View all GitHub Actions runs
gh run list --branch main

# View latest run details
gh run view -w ci.yml

# Cancel running workflow
gh run cancel <run-id>

# View security alerts
gh secret-scanning list
```

---

**Last Updated:** December 18, 2025  
**Version:** 1.0 (Production Ready)
