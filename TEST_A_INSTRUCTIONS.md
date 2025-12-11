# 🧪 TEST A - PROMETHEUS TARGETS VALIDATION

## Overview
**Objective**: Verify that all Prometheus targets (services) are being scraped successfully

**Expected Result**: All services should show `UP` status in Prometheus targets endpoint

---

## Steps to Run TEST A

### Step 1: Start the Docker Stack
```powershell
cd c:\neurosonix-cloud
docker-compose -f docker-compose.prod.yml up -d
```

**What starts**:
- PostgreSQL (5432)
- PostgreSQL Exporter (9187) ← **NEW**
- Redis (6379)
- Redis Exporter (9121) ← **NEW**
- Prometheus (9090)
- VictoriaMetrics (8428)
- Grafana (3001)
- And other services...

**Wait**: ~30 seconds for all containers to be healthy

---

### Step 2: Verify Exporters Are Running
```powershell
# Check postgres-exporter is responding
curl http://localhost:9187/metrics | Select-Object -First 10

# Check redis-exporter is responding
curl http://localhost:9121/metrics | Select-Object -First 10
```

**Expected Output**:
```
# HELP pg_up Whether the last scrape of the PostgreSQL server was successful
# TYPE pg_up gauge
pg_up 1
```

---

### Step 3: Run the Test Suite
```powershell
cd c:\neurosonix-cloud
.\test-monitoring.ps1
```

**This will**:
1. Query `http://localhost:9090/api/v1/targets`
2. Display each target's status (UP/DOWN)
3. Count total UP and DOWN targets
4. Validate key metrics are being collected

**Expected Output**:
```
[TEST 1/4] Prometheus Targets Status...

  Total Targets: 10
  ╔════════════════════════════════════════════╗
  ║ [✓] prometheus : up
  ║ [✓] api : up
  ║ [✓] postgres : up                ← NEW
  ║ [✓] redis : up                   ← NEW
  ║ [✓] alba : up
  ║ [✓] albi : up
  ║ [✓] jona : up
  ║ [✓] orchestrator : up
  ║ [✓] slack : up
  ║ [✓] elasticsearch : up
  ╚════════════════════════════════════════════╝

  Summary: 10 UP, 0 DOWN
```

---

### Step 4: View Targets in Prometheus UI
Open in browser:
```
http://localhost:9090/targets
```

**Look for**:
- `postgres-exporter` job with state `UP` ← **NEW**
- `redis-exporter` job with state `UP` ← **NEW**
- All other jobs showing `UP`
- No `DOWN` targets

**Screenshot Reference**:
```
Job             Instance                 State  Scrapes  Errors  Last Scrape
─────────────────────────────────────────────────────────────────────────────
prometheus      localhost:9090           UP     45       0       2s ago
api             localhost:8000           UP     42       0       3s ago
postgres        postgres-exporter:9187   UP     41       0       5s ago   ← NEW
redis           redis-exporter:9121      UP     39       0       7s ago   ← NEW
alba            alba:5555                UP     38       0       8s ago
albi            albi:6666                UP     35       0       12s ago
jona            jona:7777                UP     32       0       15s ago
orchestrator    orchestrator:9999        UP     28       0       18s ago
slack           slack:8888               UP     25       0       22s ago
elasticsearch   elasticsearch:9200       UP     20       0       25s ago
```

---

## Critical Metrics to Verify

### PostgreSQL Metrics (should exist)
```
pg_up{instance="postgres-exporter:9187"}
pg_stat_activity_count
pg_database_size_bytes
pg_stat_database_tup_returned
```

**How to check**:
1. Go to `http://localhost:9090`
2. Click "Metrics" (top menu)
3. Search for `pg_up`
4. Should see `pg_up{instance="postgres-exporter:9187"}` listed

### Redis Metrics (should exist)
```
redis_up{instance="redis-exporter:9121"}
redis_connected_clients
redis_memory_used_bytes
redis_keyspace_hits_total
redis_keyspace_misses_total
```

**How to check**:
1. Go to `http://localhost:9090`
2. Click "Metrics"
3. Search for `redis_up`
4. Should see `redis_up{instance="redis-exporter:9121"}` listed

---

## Troubleshooting

### Problem: postgres-exporter shows DOWN
```
postgres-exporter job is DOWN in Prometheus targets
```

**Solution**:
1. Check postgres-exporter logs:
```powershell
docker logs clisonix-postgres-exporter
```

2. Check PostgreSQL is running:
```powershell
docker logs clisonix-postgres
```

3. Verify connection string (should be in docker-compose):
```
DATA_SOURCE_NAME: "postgresql://clisonix:clisonix@postgres:5432/clisonixdb?sslmode=disable"
```

---

### Problem: redis-exporter shows DOWN
```
redis-exporter job is DOWN in Prometheus targets
```

**Solution**:
1. Check redis-exporter logs:
```powershell
docker logs clisonix-redis-exporter
```

2. Check Redis is running:
```powershell
docker logs clisonix-redis
```

3. Verify Redis connection:
```powershell
docker exec clisonix-redis redis-cli ping
# Should return: PONG
```

---

### Problem: No metrics available
```
Prometheus shows 0 metrics collected
```

**Solution**:
1. Wait 30+ seconds (Prometheus needs time to scrape all targets)
2. Check Prometheus logs:
```powershell
docker logs clisonix-prometheus-collector
```

3. Verify scrape configs (should see in logs):
```
level=info msg="Starting Prometheus" ...
level=info msg="Listening on address ..." ...
```

---

## Success Criteria ✅

You've passed TEST A when:

- [ ] All 10+ targets show `UP` status in Prometheus
- [ ] PostgreSQL exporter is `UP`
- [ ] Redis exporter is `UP`
- [ ] `pg_up` metric exists and equals 1
- [ ] `redis_up` metric exists and equals 1
- [ ] Test suite shows "MONITORING STACK READY"
- [ ] Zero `DOWN` targets

---

## Output Example (SUCCESS)
```
╔════════════════════════════════════════════════════════════╗
║  CLISONIX MONITORING STACK - PRE-DEPLOYMENT TEST          ║
╚════════════════════════════════════════════════════════════╝

[TEST 1/4] Prometheus Targets Status...
  Total Targets: 10
  ║ [✓] prometheus : up
  ║ [✓] api : up
  ║ [✓] postgres : up              ← PostgreSQL Exporter
  ║ [✓] redis : up                 ← Redis Exporter
  ║ [✓] alba : up
  ║ [✓] albi : up
  ║ [✓] jona : up
  ║ [✓] orchestrator : up
  Summary: 10 UP, 0 DOWN

[TEST 2/4] API Metrics Collection...
  Sending test requests to API...
    ✓ Request 1 completed
    ✓ Request 2 completed
    ✓ Request 3 completed
    ✓ Request 4 completed
    ✓ Request 5 completed
  Fetching API metrics...
  Checking for key metrics:
    ✓ http_requests_total : FOUND
    ✓ http_request_duration_seconds : FOUND
    ✓ active_connections : FOUND
    ✓ api_calls_total : FOUND

[TEST 3/4] PostgreSQL Exporter...
  Testing postgres-exporter endpoint...
  Checking PostgreSQL metrics:
    ✓ pg_up : FOUND
    ✓ pg_stat_activity_count : FOUND
    ✓ pg_database_size_bytes : FOUND
    ✓ pg_stat_database_tup_returned : FOUND
  Result: 4/4 metrics available

[TEST 4/4] Redis Exporter...
  Testing redis-exporter endpoint...
  Checking Redis metrics:
    ✓ redis_up : FOUND
    ✓ redis_connected_clients : FOUND
    ✓ redis_memory_used_bytes : FOUND
    ✓ redis_keyspace_hits_total : FOUND
    ✓ redis_keyspace_misses_total : FOUND
    ✓ redis_evicted_keys_total : FOUND
  Result: 6/6 metrics available

╔════════════════════════════════════════════════════════════╗
║  TEST SUMMARY                                              ║
╚════════════════════════════════════════════════════════════╝

  Prometheus Targets: 10 UP, 0 DOWN
  API Metrics Found: 4 metrics
  PostgreSQL Exporter: Connected ✓
  Redis Exporter: Connected ✓

📊 MONITORING STACK READY FOR DEPLOYMENT
```

---

## Next: Send Results to Me

After TEST A passes, send me:

1. **Prometheus Targets JSON**:
```powershell
Invoke-WebRequest "http://localhost:9090/api/v1/targets" -UseBasicParsing | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

2. **Test Script Output**:
```powershell
.\test-monitoring.ps1 | Tee-Object test-results.txt
```

3. **Screenshots**:
   - Prometheus /targets page
   - Prometheus graph showing `pg_up` = 1
   - Prometheus graph showing `redis_up` = 1

**Then I'll do the performance optimization analysis!** 🚀
