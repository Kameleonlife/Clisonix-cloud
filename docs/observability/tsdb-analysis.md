# TSDB Analysis — Grafana Charts Breakdown

**Document Status:** Draft  
**Version:** 1.0.0  
**Last Updated:** December 11, 2025

---

## Executive Summary

This document provides detailed analysis of the 6 Grafana charts exported from Clisonix Cloud's Prometheus TSDB monitoring dashboard.

**Key Findings:**
- ✅ TSDB is healthy with 1053 active series
- ✅ No cardinality explosions detected
- ✅ Linear data growth indicates stable ingestion
- ✅ Memory usage is optimal (~52KB for top label)

---

## Chart 1: Memory Usage by Label Name (Bytes)

![Memory Usage](grafana-dashboards/chart1.png)

### Analysis

**Top Labels by Memory:**
1. `__name__` — **52,000 bytes** (~52KB)
2. `instance` — **25,000 bytes** (~25KB)
3. `job` — **15,000 bytes** (~15KB)
4. `handler` — **8,000 bytes** (~8KB)
5. `le` — **4,000 bytes** (~4KB)

### Interpretation

- **`__name__` dominance:** Expected — stores all metric names
- **Total memory:** ~104KB for label metadata (very efficient)
- **No bloat:** Histogram labels (`le`) remain small
- **Verdict:** 🟢 **Healthy** — memory footprint is minimal

### Recommendations

- Monitor `__name__` growth as new metrics are added
- If adding custom labels, avoid high-cardinality values
- Current state supports 10x scale before optimization needed

---

## Chart 2: Top Label Value Pair Cardinality

![Label Cardinality](grafana-dashboards/chart2.png)

### Analysis

**Top Pairs:**
1. `instance=localhost:9090` — **1013 pairs**
2. `job=prometheus` — **1013 pairs**
3. `__name__=req_dur_bucket` — **130 pairs**
4. `__name__=resp_bucket` — **117 pairs**

### Interpretation

- **Single-instance setup:** All 1013 series tagged with same `instance`
- **Job consistency:** Single Prometheus job tracks all metrics
- **Histogram metrics:** Bucket labels create expected cardinality
- **Verdict:** 🟢 **Expected** — cardinality matches architecture

### Recommendations

- When adding scrape targets, monitor `instance` cardinality
- Future federation will increase this linearly per node
- Avoid user-generated labels (session IDs, request IDs, etc.)

---

## Chart 3: TSDB Time Window Timeline

![TSDB Timeline](grafana-dashboards/chart3.png)

### Analysis

**Time Window:**
- **Min Time:** Position 1.0 (2025-12-10 15:09)
- **Max Time:** Position 2.0 (2025-12-10 16:23)
- **Duration:** ~1 hour 14 minutes
- **Growth:** Linear progression

### Interpretation

- **Steady ingestion:** No gaps or drops in data collection
- **Linear timeline:** Scrapes happening consistently at 15s intervals
- **Active window:** Head block maintaining recent data
- **Verdict:** 🟢 **Stable** — no ingestion issues detected

### Recommendations

- Monitor for gaps during deployments
- Ensure scrape interval consistency in production
- TSDB retention (15d) supports current scale

---

## Chart 4: Top Metric Families by Series Count

![Metric Families](grafana-dashboards/chart4.png)

### Analysis

**Top Families:**
1. `http_req_dur_bucket` — **130 series**
2. `http_resp_size_bucket` — **117 series**
3. `http_requests_total` — **58 series**
4. `target_sync_len` — **45 series**
5. `conntrack_failed` — **43 series**

### Interpretation

- **Histogram dominance:** Bucket metrics create most series (expected)
- **HTTP focus:** Request/response metrics are top priority
- **Distribution:** No single family dominates (healthy diversity)
- **Verdict:** 🟢 **Balanced** — metric distribution is appropriate

### Recommendations

- If adding custom histograms, limit bucket count
- Group related metrics into families
- Avoid per-endpoint histogram metrics (use aggregated)

---

## Chart 5: Label Cardinality

![Label Pairs](grafana-dashboards/chart5.png)

### Analysis

**Total Label Pairs:** **515**

### Interpretation

- **Low cardinality:** 515 pairs across 1053 series = ~0.5 labels/series avg
- **Efficient indexing:** TSDB can query this instantly
- **No explosion risk:** Cardinality growth is controlled
- **Verdict:** 🟢 **Excellent** — far below danger threshold (100K+)

### Recommendations

- Maintain label discipline when adding metrics
- Avoid dynamic labels (timestamps, UUIDs, user IDs)
- Use relabeling rules to normalize label values

---

## Chart 6: Total Active Time Series

![Active Series](grafana-dashboards/chart6.png)

### Analysis

**Active Series:** **1053**

### Interpretation

- **Production-ready:** 1K series supports small-to-medium deployments
- **Scalability:** Prometheus handles 1M+ series, we're at 0.1% capacity
- **Growth potential:** 100x headroom before infrastructure changes needed
- **Verdict:** 🟢 **Optimal** — right-sized for current stage

### Recommendations

- Monitor series growth rate (current: stable)
- Plan for 10K series when adding distributed tracing
- Consider remote storage if exceeding 100K series

---

## Overall TSDB Health Score

| Metric | Current | Threshold | Status |
|--------|---------|-----------|--------|
| **Series Count** | 1,053 | < 10,000 | 🟢 Excellent |
| **Label Pairs** | 515 | < 100,000 | 🟢 Excellent |
| **Memory/Label** | 52KB | < 10MB | 🟢 Excellent |
| **Cardinality** | Low | Medium | 🟢 Healthy |
| **Data Gaps** | None | < 1% | 🟢 Perfect |

**Overall Grade:** **A+ (Production Ready)**

---

## Risk Assessment

### Current Risks
- 🟢 **None detected** — all metrics within healthy ranges

### Future Risks (6-12 months)
- 🟡 **Series growth:** Monitor when adding new services
- 🟡 **Storage:** Plan retention strategy for long-term data
- 🟡 **Federation:** Multi-cluster setup will increase complexity

### Mitigation Strategies
1. Implement recording rules for expensive queries
2. Set up cardinality alerts (> 10K series)
3. Configure remote write to object storage
4. Enable Thanos for long-term retention

---

**Next:** [Cardinality Engineering →](cardinality-engineering.md)
