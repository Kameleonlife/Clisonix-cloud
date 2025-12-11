#!/usr/bin/env python3
"""
Import ASI Trinity Dashboard into Grafana
"""
import requests
import json
import sys

# Grafana configuration
GRAFANA_URL = "http://localhost:3001"
GRAFANA_API_KEY = "admin"  # Default admin user
GRAFANA_USERNAME = "admin"
GRAFANA_PASSWORD = "admin"

def create_grafana_dashboard():
    """Create ASI Trinity dashboard in Grafana"""
    
    try:
        # Read the dashboard JSON
        with open('grafana-asi-trinity-dashboard.json', 'r') as f:
            dashboard_data = json.load(f)
        
        # Grafana API endpoint
        url = f"{GRAFANA_URL}/api/dashboards/db"
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GRAFANA_API_KEY}"
        }
        
        # Prepare payload
        payload = {
            "dashboard": dashboard_data.get("dashboard", dashboard_data),
            "overwrite": True
        }
        
        print("📊 Attempting to create Grafana dashboard...")
        print(f"Grafana URL: {GRAFANA_URL}")
        print(f"Dashboard title: {payload['dashboard'].get('title', 'Unknown')}")
        
        # Send request
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code in [200, 201]:
            result = response.json()
            dashboard_id = result.get('id', 'unknown')
            dashboard_url = result.get('url', f"/d/{dashboard_id}")
            print(f"\n✅ Dashboard created successfully!")
            print(f"Dashboard ID: {dashboard_id}")
            print(f"URL: {GRAFANA_URL}{dashboard_url}")
            return True
        else:
            print(f"\n❌ Failed to create dashboard")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except FileNotFoundError:
        print("❌ Dashboard JSON file not found")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_prometheus_datasource():
    """Verify Prometheus is configured as datasource"""
    try:
        url = f"{GRAFANA_URL}/api/datasources"
        headers = {
            "Authorization": f"Bearer {GRAFANA_API_KEY}"
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            datasources = response.json()
            prometheus_found = any(ds.get('type') == 'prometheus' for ds in datasources)
            
            if prometheus_found:
                print("✅ Prometheus datasource is configured")
                return True
            else:
                print("⚠️  Prometheus datasource not found - creating...")
                return create_prometheus_datasource()
        else:
            print(f"⚠️  Could not verify datasources: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Error checking datasources: {e}")
        return False

def create_prometheus_datasource():
    """Create Prometheus datasource in Grafana"""
    try:
        url = f"{GRAFANA_URL}/api/datasources"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GRAFANA_API_KEY}"
        }
        
        payload = {
            "name": "Prometheus",
            "type": "prometheus",
            "url": "http://localhost:9090",
            "access": "proxy",
            "isDefault": True
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code in [200, 201]:
            print("✅ Prometheus datasource created")
            return True
        else:
            print(f"⚠️  Failed to create datasource: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️  Error creating datasource: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ASI Trinity Grafana Dashboard Setup")
    print("=" * 60)
    print()
    
    # Verify Prometheus
    if verify_prometheus_datasource():
        # Create dashboard
        if create_grafana_dashboard():
            print("\n" + "=" * 60)
            print("✅ Dashboard setup complete!")
            print("=" * 60)
            print(f"\n📊 Access Grafana at: {GRAFANA_URL}")
            print("   Username: admin")
            print("   Password: admin")
            print("\n🎯 View the ASI Trinity dashboard from the Dashboards menu")
            sys.exit(0)
        else:
            print("\n❌ Failed to create dashboard")
            sys.exit(1)
    else:
        print("\n⚠️  Could not verify Prometheus - setup may be incomplete")
        sys.exit(1)
