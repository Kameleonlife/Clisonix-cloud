# Prometheus Metrics Reference

**Document Status:** Draft  
**Version:** 1.0.0  
**Last Updated:** December 11, 2025

---

## Prometheus Internal Metrics

This document details all Prometheus self-monitoring metrics.

---

## HTTP Metrics

### `prometheus_http_requests_total`
- **Type:** Counter
- **Labels:** `code`, `handler`
- **Description:** Total HTTP requests to Prometheus server

### `prometheus_http_request_duration_seconds`
- **Type:** Histogram
- **Labels:** `handler`
- **Buckets:** Multiple quantiles
- **Description:** HTTP request latency

### `prometheus_http_response_size_bytes`
- **Type:** Histogram
- **Labels:** `handler`
- **Description:** HTTP response payload size

---

## TSDB Metrics

### Head Block Metrics

**`prometheus_tsdb_head_series`**
- Current: **1053**
- Description: Active time series in head block

**`prometheus_tsdb_head_chunks`**
- Current: **1053**
- Description: Total chunks in head block

**`prometheus_tsdb_head_samples_appended_total`**
- Description: Total samples appended to head

### Storage Metrics

**`prometheus_tsdb_storage_blocks_bytes`**
- Description: Total disk space used by blocks

**`prometheus_tsdb_lowest_timestamp_seconds`**
- Current: **2025-12-10 15:09**
- Description: Oldest data point in TSDB

**`prometheus_tsdb_head_max_time_seconds`**
- Current: **2025-12-10 16:23**
- Description: Newest data point in TSDB

### Compaction Metrics

**`prometheus_tsdb_compactions_total`**
- Description: Successful compactions

**`prometheus_tsdb_compaction_duration_seconds`**
- Description: Time spent in compaction

---

## Scrape Metrics

**`prometheus_target_scrapes_total`**
- Description: Total scrape attempts

**`prometheus_target_scrape_duration_seconds`**
- Description: Scrape operation latency

**`prometheus_target_scrape_samples_scraped`**
- Description: Samples collected per scrape

---

## Rule Evaluation Metrics

**`prometheus_rule_evaluations_total`**
- Description: Total rule evaluations

**`prometheus_rule_evaluation_duration_seconds`**
- Description: Rule evaluation latency

**`prometheus_rule_evaluation_failures_total`**
- Description: Failed rule evaluations

---

## Query Metrics

**`prometheus_engine_queries`**
- Description: Active PromQL queries

**`prometheus_engine_query_duration_seconds`**
- Description: Query execution time

**`prometheus_engine_queries_concurrent_max`**
- Description: Max concurrent queries allowed

---

## Label Cardinality Metrics

**`prometheus_tsdb_symbol_table_size_bytes`**
- Current: **~52KB** for `__name__` label
- Description: Memory used by label value storage

**Top Label Pairs (Current State):**
- `instance=localhost:9090`: **1013 series**
- `job=prometheus`: **1013 series**

---

## Alert Metrics

**`prometheus_notifications_sent_total`**
- Labels: `alertmanager`
- Description: Notifications sent to Alertmanager

**`prometheus_notifications_dropped_total`**
- Description: Dropped notifications

---

## Network Metrics

**`prometheus_remote_storage_samples_total`**
- Description: Samples sent to remote storage (if configured)

**`net_conntrack_dialer_conn_failed_total`**
- Description: Failed outbound connections

---

## Performance Benchmarks

Based on current deployment:

| Metric | Value | Status |
|--------|-------|--------|
| Series Count | 1053 | 🟢 Healthy |
| Chunks | 1053 | 🟢 Optimal |
| Label Pairs | 515 | 🟢 Low Cardinality |
| Memory/Label | 52KB (`__name__`) | 🟢 Efficient |
| Scrape Interval | 15s | 🟢 Standard |

---

## Recommended Alerts

```yaml
groups:
  - name: prometheus
    rules:
      - alert: PrometheusHighCardinality
        expr: prometheus_tsdb_head_series > 10000
        for: 5m
        annotations:
          summary: "TSDB series count exceeding 10K"

      - alert: PrometheusCompactionSlow
        expr: prometheus_tsdb_compaction_duration_seconds > 300
        for: 10m
        annotations:
          summary: "Compaction taking longer than 5 minutes"
```

---

**Next:** [TSDB Analysis →](tsdb-analysis.md)
