# 🔄 SELF-CONSUMPTION & HYBRID API STRATEGY

## 🎯 Koncepti: SELF-EVOLUTION through SELF-USE

**Parimi Kryesor:** Clisonix duhet të jetë konsumatori i parë i API-ve të veta. 
Çdo modul, agent, dhe shërbim duhet të përdorë infrastrukturën tonë të brendshme
PARA se të thërrasë API të jashtme.

---

## 📊 CURRENT STATE (December 2025)

### ✅ Self-Consumption Patterns (EKZISTUESE):
1. **Neuro Engines** → Imported directly në main.py
   - apps.api.neuro.youtube_insight_engine
   - apps.api.neuro.energy_engine
   - apps.api.neuro.moodboard_engine
   - apps.api.neuro.hps_engine
   - apps.api.neuro.brainsync_engine
   - apps.api.neuro.audio_to_midi

2. **Cycle Integration** → Internal API calls
   - blerina_cycle_integration.py → http://clisonix-api:8000
   - cycle_asi_integration.py → http://clisonix-api:8000

3. **Metrics Collection** → Internal endpoints
   - localhost:8000/api/alba/status
   - localhost:8000/asi/status

4. **API Producer/Manager** → Self-registry
   - Producer: POST /register, /publish
   - Manager: Syncs from Producer

### ⚠️ PROBLEMS (GAPS):
- Agents mostly call external APIs directly
- Research modules don't use own data ingestion
- Brain engine doesn't consume own endpoints
- No internal API gateway/router
- Limited inter-agent communication via APIs
- Self-generating API not integrated with registry

---

## 🏗️ HYBRID MODEL ARCHITECTURE

\\\
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  API GATEWAY       │ ◄─── Kong/Internal Router
        │  (Rate Limit,      │
        │   Auth, Routing)   │
        └─────────┬──────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐   ┌──────────┐   ┌──────────┐
│ MAIN  │   │   API    │   │  SELF-   │
│  API  │   │ PRODUCER │   │GENERATING│
│ :8000 │   │  :8001   │   │   API    │
└───┬───┘   └────┬─────┘   └────┬─────┘
    │            │              │
    │ ┌──────────┴──────┬───────┘
    │ │                 │
    ▼ ▼                 ▼
┌─────────────────────────────────┐
│   INTERNAL SERVICE MESH         │
│   ┌──────────────────────┐      │
│   │ 1. Brain Engine      │──┐   │
│   │ 2. Neuro Processors  │  │   │
│   │ 3. ASI Trinity       │  │   │
│   │    (ALBA/ALBI/JONA)  │  │   │
│   │ 4. Research Modules  │  │   │
│   │ 5. Cycle Agents      │  │   │
│   │ 6. SaaS Orchestrator │  │   │
│   └──────────────────────┘  │   │
│          ▲                  │   │
│          └──────────────────┘   │
│          (Self-calling loop)    │
└──────────┬──────────────────────┘
           │
    ┌──────┴───────┐
    │              │
    ▼              ▼
┌─────────┐   ┌──────────────┐
│ HYBRID  │   │   EXTERNAL   │
│  DATA   │   │   OPEN APIs  │
│ SOURCES │   │              │
│         │   │ • OpenAlex   │
│• Local  │   │ • PubMed     │
│  Files  │   │ • OpenFDA    │
│• Cycles │   │ • CoinGecko  │
│• Docs   │   │ • Open-Meteo │
│• Stats  │   │ • etc. (26+) │
└─────────┘   └──────────────┘
\\\

---

## 🔄 SELF-CONSUMPTION RULES

### 1️⃣ **FIRST: Internal APIs**
Çdo modul DUHET të kontrollojë internal endpoints PARA external APIs:

\\\python
# ❌ BAD: Direct external call
response = requests.get('https://api.coingecko.com/...')

# ✅ GOOD: Internal first, fallback to external
try:
    # Try internal cache/aggregator first
    response = requests.get('http://localhost:8000/api/crypto/market')
except:
    # Fallback to external if internal fails
    response = requests.get('https://api.coingecko.com/...')
\\\

### 2️⃣ **SECOND: Hybrid Data Sources**
Kombinim i të dhënave interne + externe:

\\\python
async def get_research_data(query: str):
    # 1. Query internal research modules FIRST
    internal_results = await query_internal_research(query)
    
    # 2. Query own ingestion cache
    cached_results = await query_weaviate_cache(query)
    
    # 3. If not enough data, query external APIs
    if len(internal_results + cached_results) < MIN_RESULTS:
        external_results = await query_openalex(query)
        external_results += await query_pubmed(query)
    
    # 4. Merge and deduplicate
    return merge_results(internal_results, cached_results, external_results)
\\\

### 3️⃣ **THIRD: Agent Inter-Communication**
Agents communicate via internal API endpoints:

\\\python
# ALBA Agent queries ALBI via API (not direct import)
albi_response = await httpx.get('http://localhost:8000/asi/albi/process', 
                                  json={'signal': data})

# Blerina queries Research modules
research_data = await httpx.post('http://localhost:8000/research/query',
                                   json={'topic': 'neural_alignment'})
\\\

### 4️⃣ **FOURTH: Self-Registry**
Çdo API e re regjistrohet automatikisht:

\\\python
# After generating new API
await register_api({
    'name': 'neural_processor_v2',
    'endpoints': ['/process', '/analyze', '/health'],
    'version': '2.0',
    'owner': 'self_generating_engine'
})
\\\

---

## 📦 IMPLEMENTATION PLAN

### Phase 1: Internal API Router (Week 1)
- [ ] Create internal_api_client.py wrapper
- [ ] Implement fallback logic (internal → external)
- [ ] Add circuit breaker for failed internals

### Phase 2: Agent Communication Layer (Week 2)
- [ ] Update ALBA to call ALBI/JONA via APIs
- [ ] Update Blerina to query Research modules via APIs
- [ ] Add internal message queue (Redis Streams)

### Phase 3: Data Source Hybridization (Week 3)
- [ ] Create hybrid_data_collector.py
- [ ] Prioritize: Local Files → Cycles → Weaviate Cache → External APIs
- [ ] Implement caching layer for external API responses

### Phase 4: Self-Registry Integration (Week 4)
- [ ] Connect self_generating_api.py to API Producer
- [ ] Auto-register all endpoints on startup
- [ ] Create API catalog UI

### Phase 5: Metrics & Analytics (Week 5)
- [ ] Track internal vs external API usage
- [ ] Monitor self-consumption ratio (target: 70%+ internal)
- [ ] Generate self-evolution reports

---

## 🎯 SUCCESS METRICS

**Target Self-Consumption Ratios:**
- **Brain Engine:** 80% internal calls (own /brain/*, /neuro/* endpoints)
- **Research Modules:** 60% internal (own Weaviate, cycles, docs)
- **Agents (ALBA/ALBI/JONA):** 90% internal communication
- **Data Ingestion:** 50% hybrid (cache + real-time external)
- **Overall System:** 70%+ self-consumption ratio

**Evolution Indicators:**
- Number of self-generated APIs deployed
- Internal API response times < 50ms
- Cache hit ratio > 80%
- Reduction in external API costs

---

## 🔧 TECHNICAL COMPONENTS

### 1. Internal API Client
\\\python
# apps/api/internal_client.py
class InternalAPIClient:
    BASE_URL = 'http://localhost:8000'
    
    async def get(self, endpoint, fallback_external=None):
        try:
            return await httpx.get(f'{self.BASE_URL}{endpoint}')
        except:
            if fallback_external:
                return await httpx.get(fallback_external)
            raise
\\\

### 2. Hybrid Data Collector
\\\python
# apps/api/hybrid_collector.py
class HybridDataCollector:
    async def collect(self, source_type, query):
        # Priority order
        sources = [
            self.local_files,
            self.cycles_db,
            self.weaviate_cache,
            self.external_apis
        ]
        for source in sources:
            try:
                data = await source.query(query)
                if self.is_sufficient(data):
                    return data
            except:
                continue
\\\

### 3. API Registry
\\\python
# apps/api/registry.py
API_REGISTRY = {
    'brain': ['http://localhost:8000/brain/*'],
    'neuro': ['http://localhost:8000/neuro/*'],
    'asi': ['http://localhost:8000/asi/*'],
    'research': ['http://localhost:8000/research/*'],
}
\\\

---

## 🌐 BENEFITS

1. **Self-Sufficiency:** Reduced dependency on external APIs
2. **Performance:** Internal calls ~10x faster than external
3. **Cost Reduction:** Less external API usage = lower costs
4. **Resilience:** System works even if external APIs fail
5. **Evolution:** System learns from own usage patterns
6. **Data Sovereignty:** Own data stays internal
7. **Security:** Reduced attack surface (fewer external calls)

---

**Last Updated:** December 26, 2025
**Status:** 🟡 Design Phase → Ready for Implementation
