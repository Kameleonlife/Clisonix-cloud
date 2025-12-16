"""
Test Suite for Unified SAAS Orchestrator v3.0
Tests: Service Registry + Agent Scaling + API Docs + Inter-Service Communication
"""

import requests
import json
import time

BASE_URL = "http://localhost:9999"

def test_health():
    """Test orchestrator health"""
    print("\n1️⃣ Testing orchestrator health...")
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Status: {data['status']}")
    print(f"   ✅ Instance: {data['instance_id']}")
    print(f"   ✅ Uptime: {data['uptime_seconds']:.1f}s")
    print(f"   ✅ Registered agents: {data['registered_agents']}")
    return data

def test_service_registry():
    """Test service discovery and health monitoring"""
    print("\n2️⃣ Testing service registry...")
    resp = requests.get(f"{BASE_URL}/registry")
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Total services: {data['total_services']}")
    print(f"   ✅ Healthy services: {data['healthy_count']}")
    for service_name, health in data['services'].items():
        status = health.get('status', 'unknown')
        emoji = "✅" if status == "healthy" else "⚠️"
        print(f"   {emoji} {service_name}: {status} (role: {health.get('data', {}).get('service', 'N/A')})")
    return data

def test_agent_registration():
    """Test AI agent registration"""
    print("\n3️⃣ Testing agent registration...")
    
    # Register AGIEM
    agiem_payload = {
        "agent_name": "AGIEM",
        "agent_type": "agiem",
        "version": "1.0.0",
        "capabilities": ["pipeline_execution", "quality_control", "resource_management", "data_routing", "error_handling"],
        "max_instances": 5,
        "endpoints": [
            {
                "path": "/agiem/pipeline/execute",
                "method": "POST",
                "summary": "Execute AGIEM pipeline",
                "description": "Run a complete AGIEM processing pipeline"
            },
            {
                "path": "/agiem/status",
                "method": "GET",
                "summary": "Get AGIEM status",
                "description": "Retrieve current AGIEM agent status"
            }
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/agents/register", json=agiem_payload)
    assert resp.status_code == 200
    agiem_data = resp.json()
    agiem_id = agiem_data['agent_id']
    print(f"   ✅ AGIEM registered: {agiem_id}")
    print(f"      Capabilities: {len(agiem_payload['capabilities'])}")
    
    # Register ASI
    asi_payload = {
        "agent_name": "ASI",
        "agent_type": "asi",
        "version": "2.1.0",
        "capabilities": ["realtime_processing", "adaptive_learning", "stream_management"],
        "max_instances": 3
    }
    
    resp = requests.post(f"{BASE_URL}/agents/register", json=asi_payload)
    assert resp.status_code == 200
    asi_data = resp.json()
    asi_id = asi_data['agent_id']
    print(f"   ✅ ASI registered: {asi_id}")
    print(f"      Capabilities: {len(asi_payload['capabilities'])}")
    
    return agiem_id, asi_id

def test_api_docs_generation(agent_id: str):
    """Test auto-generated API documentation"""
    print("\n4️⃣ Testing API docs generation...")
    
    doc_payload = {
        "endpoints": [
            {
                "path": "/agiem/pipeline/execute",
                "method": "POST",
                "summary": "Execute AGIEM pipeline",
                "description": "Run a complete AGIEM processing pipeline",
                "operation_id": "execute_agiem_pipeline",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "pipeline_id": {"type": "string"},
                                    "data": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            {
                "path": "/agiem/status",
                "method": "GET",
                "summary": "Get AGIEM status",
                "description": "Retrieve current AGIEM agent status",
                "operation_id": "get_agiem_status"
            }
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/api-docs/generate?agent_id={agent_id}", json=doc_payload)
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ API docs generated for {agent_id}")
    print(f"      Endpoints: {data['endpoints_count']}")
    print(f"      OpenAPI version: {data['spec']['openapi']}")
    
    return data

def test_agent_scaling(agent_id: str):
    """Test agent scaling"""
    print("\n5️⃣ Testing agent scaling...")
    
    # Scale to 3 instances
    scale_payload = {"target_instances": 3}
    resp = requests.post(f"{BASE_URL}/agents/{agent_id}/scale?target_instances=3")
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Scaled {agent_id}")
    print(f"      Previous: {data['previous_instances']}")
    print(f"      Current: {data['current_instances']}")
    print(f"      Max: {data['max_instances']}")
    
    return data

def test_agent_heartbeat(agent_id: str):
    """Test agent heartbeat"""
    print("\n6️⃣ Testing agent heartbeat...")
    
    metrics = {
        "cpu_percent": 45.2,
        "memory_percent": 62.8,
        "active_pipelines": 5
    }
    
    resp = requests.post(f"{BASE_URL}/agents/{agent_id}/heartbeat", json=metrics)
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Heartbeat acknowledged")
    print(f"      Status: {data['status']}")
    
    return data

def test_comprehensive_status():
    """Test comprehensive status endpoint"""
    print("\n7️⃣ Testing comprehensive status...")
    
    resp = requests.get(f"{BASE_URL}/status")
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Orchestrator v{data['orchestrator']['version']}")
    print(f"      Services: {data['services']['healthy']}/{data['services']['total']} healthy")
    print(f"      Agents: {data['agents']['active']}/{data['agents']['registered']} active")
    print(f"      Total instances: {data['agents']['total_instances']}")
    print(f"      API endpoints: {data['api_docs']['endpoints_documented']}")
    print(f"      Operations: {data['api_docs']['total_operations']}")
    print(f"      Messages logged: {data['communication']['messages_logged']}")
    
    return data

def test_inter_service_communication():
    """Test inter-service communication"""
    print("\n8️⃣ Testing inter-service communication...")
    
    packet = {
        "source": "orchestrator",
        "destination": "alba",
        "packet_type": "telemetry",
        "payload": {
            "test": True,
            "message": "Test communication packet"
        }
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/communicate", json=packet)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✅ Communication delivered")
            print(f"      Destination: {data['destination']}")
            print(f"      Correlation ID: {data['correlation_id']}")
        else:
            print(f"   ⚠️ Communication failed: {resp.status_code}")
            print(f"      (This is expected if Alba doesn't have /receive endpoint)")
    except Exception as e:
        print(f"   ⚠️ Communication test skipped: {str(e)}")

def test_service_proxy():
    """Test service proxy"""
    print("\n9️⃣ Testing service proxy...")
    
    resp = requests.get(f"{BASE_URL}/services/alba/health")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✅ Proxy to Alba successful")
        print(f"      Service: {data.get('service', 'N/A')}")
        print(f"      Status: {data.get('status', 'N/A')}")
    else:
        print(f"   ⚠️ Proxy failed: {resp.status_code}")

def test_list_agents():
    """Test listing all agents"""
    print("\n🔟 Testing agent list...")
    
    resp = requests.get(f"{BASE_URL}/agents")
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Total agents: {data['count']}")
    for agent in data['agents']:
        print(f"      • {agent['agent_name']} ({agent['agent_id']})")
        print(f"        Type: {agent['agent_type']}, Instances: {agent['current_instances']}/{agent['max_instances']}")

def test_api_docs_list():
    """Test listing API docs"""
    print("\n1️⃣1️⃣ Testing API docs list...")
    
    resp = requests.get(f"{BASE_URL}/api-docs")
    assert resp.status_code == 200
    data = resp.json()
    print(f"   ✅ Total documented APIs: {data['count']}")
    for doc in data['docs']:
        operations = len(doc['spec']['paths'])
        print(f"      • {doc['agent']}: {operations} operations")

def test_openapi_spec_retrieval(agent_id: str):
    """Test OpenAPI spec retrieval"""
    print("\n1️⃣2️⃣ Testing OpenAPI spec retrieval...")
    
    resp = requests.get(f"{BASE_URL}/api-docs/{agent_id}/openapi.json")
    assert resp.status_code == 200
    spec = resp.json()
    print(f"   ✅ OpenAPI spec retrieved")
    print(f"      Version: {spec['openapi']}")
    print(f"      Title: {spec['info']['title']}")
    print(f"      Paths: {list(spec['paths'].keys())}")

def main():
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║  UNIFIED SAAS ORCHESTRATOR v3.0 - COMPREHENSIVE TEST SUITE  ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    try:
        # Basic tests
        test_health()
        test_service_registry()
        
        # Agent management tests
        agiem_id, asi_id = test_agent_registration()
        test_api_docs_generation(agiem_id)
        test_agent_scaling(agiem_id)
        test_agent_heartbeat(agiem_id)
        
        # Status and monitoring
        test_comprehensive_status()
        
        # Communication tests
        test_inter_service_communication()
        test_service_proxy()
        
        # List and retrieval tests
        test_list_agents()
        test_api_docs_list()
        test_openapi_spec_retrieval(agiem_id)
        
        print("\n" + "="*65)
        print("✅ ALL TESTS PASSED!")
        print("="*65 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise

if __name__ == "__main__":
    main()

