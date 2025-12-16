#!/usr/bin/env python3
"""
Alba Connection Monitor
Sistemi i monitorimit të lidhjeve për Alba
Përdor ping3 për të monitoruar performancën e rrjetit
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import os

try:
    from ping3 import ping, verbose_ping
    PING3_AVAILABLE = True
except ImportError:
    PING3_AVAILABLE = False
    logging.warning("ping3 nuk është i disponueshëm. Ju lutem instaloni me: pip install ping3")

@dataclass
class ConnectionStats:
    """Statistikat e lidhjes për një host të vetëm"""
    host: str
    ip: Optional[str] = None
    avg_latency: float = 0.0
    min_latency: float = float('inf')
    max_latency: float = 0.0
    packet_loss: float = 0.0
    total_pings: int = 0
    successful_pings: int = 0
    last_ping_time: Optional[str] = None
    last_successful_ping: Optional[str] = None
    status: str = "unknown"  # online, offline, slow, unknown

@dataclass
class NetworkSummary:
    """Përmbledhja e përgjithshme e rrjetit"""
    total_hosts: int = 0
    online_hosts: int = 0
    offline_hosts: int = 0
    avg_network_latency: float = 0.0
    total_monitoring_time: float = 0.0
    last_update: Optional[str] = None

class AlbaConnectionMonitor:
    """
    Sistemi kryesor i monitorimit të lidhjeve për Alba
    Monitoron lidhjet me serverat dhe shërbimet e ndryshme
    """
    
    def __init__(self, config_path: str = "config/alba_network.json"):
        self.config_path = config_path
        self.stats: Dict[str, ConnectionStats] = {}
        self.monitoring_active = False
        self.start_time = time.time()
        
        # Lista e hosteve për monitorim
        self.default_hosts = [
            "google.com",
            "cloudflare.com", 
            "github.com",
            "stackoverflow.com",
            "wikipedia.org",
            "microsoft.com",
            "amazon.com",
            "facebook.com",
            "twitter.com",
            "linkedin.com",
            "youtube.com",
            "instagram.com",
            "reddit.com",
            "pinterest.com",
            "tumblr.com",
            "medium.com",
            "quora.com",
            "8.8.8.8",  # Google DNS
            "1.1.1.1",  # Cloudflare DNS
            "208.67.222.222"  # OpenDNS
        ]
        
        self.load_config()
        self.setup_logging()
    
    def setup_logging(self):
        """Konfigurimi i logging per monitorim"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - Alba Monitor - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/alba_network_monitor.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """Ngarkon konfigurimin e monitorimit"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8-sig') as f:
                    config = json.load(f)
                    self.hosts_to_monitor = config.get('hosts', self.default_hosts)
                    self.ping_interval = config.get('ping_interval', 30)  # sekonda
                    self.timeout = config.get('timeout', 5)
            else:
                self.hosts_to_monitor = self.default_hosts
                self.ping_interval = 30
                self.timeout = 5
                self.save_config()
        except Exception as e:
            self.logger.error(f"Error ne ngarkimin e konfigurimit: {e}")
            self.hosts_to_monitor = self.default_hosts
            self.ping_interval = 30
            self.timeout = 5
    
    def save_config(self):
        """Ruan konfigurimin aktual"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            config = {
                'hosts': self.hosts_to_monitor,
                'ping_interval': self.ping_interval,
                'timeout': self.timeout,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error ne ruajtjen e konfigurimit: {e}")
    
    def ping_host(self, host: str) -> Optional[float]:
        """Ping nje host te vetem dhe kthen latency ne ms"""
        if not PING3_AVAILABLE:
            self.logger.warning("ping3 nuk eshte i disponueshem")
            return None
        
        try:
            result = ping(host, timeout=self.timeout)
            if result is not None:
                return result * 1000  # konverto në millisekonda
            return None
        except Exception as e:
            self.logger.debug(f"Error ne ping per {host}: {e}")
            return None
    
    def update_stats(self, host: str, latency: Optional[float]):
        """Perditeson statistikat per nje host"""
        current_time = datetime.now().isoformat()
        
        if host not in self.stats:
            self.stats[host] = ConnectionStats(host=host)
        
        stats = self.stats[host]
        stats.total_pings += 1
        stats.last_ping_time = current_time
        
        if latency is not None:
            stats.successful_pings += 1
            stats.last_successful_ping = current_time
            
            # Përditëso latency stats
            if stats.min_latency == float('inf'):
                stats.min_latency = latency
            else:
                stats.min_latency = min(stats.min_latency, latency)
            
            stats.max_latency = max(stats.max_latency, latency)
            
            # Llogarit average latency
            old_avg = stats.avg_latency
            stats.avg_latency = ((old_avg * (stats.successful_pings - 1)) + latency) / stats.successful_pings
            
            # Percakto statusin
            if latency < 50:
                stats.status = "excellent"
            elif latency < 100:
                stats.status = "good"
            elif latency < 200:
                stats.status = "fair"
            else:
                stats.status = "slow"
        else:
            stats.status = "offline"
        
        # Llogarit packet loss
        stats.packet_loss = ((stats.total_pings - stats.successful_pings) / stats.total_pings) * 100
    
    async def monitor_host(self, host: str):
        """Monitoron nje host ne menyre te vazhdueshme"""
        while self.monitoring_active:
            try:
                latency = self.ping_host(host)
                self.update_stats(host, latency)
                
                status = "✓" if latency else "✗"
                latency_str = f"{latency:.1f}ms" if latency else "timeout"
                self.logger.info(f"{status} {host}: {latency_str}")
                
            except Exception as e:
                self.logger.error(f"Error ne monitorimin e {host}: {e}")
            
            await asyncio.sleep(self.ping_interval)
    
    async def start_monitoring(self):
        """Fillon monitorimin per te gjitha hostet"""
        if not PING3_AVAILABLE:
            self.logger.error("ping3 nuk eshte i disponueshem. Monitorimi nuk mund te filloje.")
            return
        
        self.monitoring_active = True
        self.start_time = time.time()
        
        self.logger.info(f"Fillimi i monitorimit per {len(self.hosts_to_monitor)} hosts...")
        
        # Krijo task për çdo host
        tasks = []
        for host in self.hosts_to_monitor:
            task = asyncio.create_task(self.monitor_host(host))
            tasks.append(task)
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"Error ne monitorim: {e}")
        finally:
            self.monitoring_active = False
    
    def stop_monitoring(self):
        """Ndal monitorimin"""
        self.monitoring_active = False
        self.logger.info("Monitorimi u ndalua")
    
    def get_network_summary(self) -> NetworkSummary:
        """Kthen përmbledhjen e rrjetit"""
        online_hosts = sum(1 for stats in self.stats.values() if stats.status != "offline")
        offline_hosts = len(self.stats) - online_hosts
        
        # Llogarit average network latency
        successful_hosts = [stats for stats in self.stats.values() if stats.successful_pings > 0]
        avg_latency = sum(stats.avg_latency for stats in successful_hosts) / len(successful_hosts) if successful_hosts else 0
        
        return NetworkSummary(
            total_hosts=len(self.stats),
            online_hosts=online_hosts,
            offline_hosts=offline_hosts,
            avg_network_latency=avg_latency,
            total_monitoring_time=time.time() - self.start_time,
            last_update=datetime.now().isoformat()
        )
    
    def get_stats_json(self) -> str:
        """Kthen statistikat në format JSON"""
        summary = self.get_network_summary()
        
        data = {
            'summary': asdict(summary),
            'hosts': {host: asdict(stats) for host, stats in self.stats.items()}
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def get_top_performers(self, count: int = 5) -> List[ConnectionStats]:
        """Kthen top performers sipas latency"""
        online_hosts = [stats for stats in self.stats.values() if stats.successful_pings > 0]
        return sorted(online_hosts, key=lambda x: x.avg_latency)[:count]
    
    def get_connection_health_score(self) -> float:
        """Llogarit një health score të përgjithshëm (0-100)"""
        if not self.stats:
            return 0.0
        
        summary = self.get_network_summary()
        
        # Factors për health score
        availability_score = (summary.online_hosts / summary.total_hosts) * 40  # 40% weight
        
        # Latency score (më mirë = latency më e ulët)
        if summary.avg_network_latency > 0:
            latency_score = max(0, 60 - (summary.avg_network_latency / 10))  # 60% weight
        else:
            latency_score = 0
        
        return min(100, availability_score + latency_score)

# Funksione utility për përdorim të shpejtë
def quick_ping_test(hosts: List[str] = None) -> Dict[str, Any]:
    """Test i shpejtë ping për listat e hosts"""
    if hosts is None:
        hosts = ["google.com", "github.com", "stackoverflow.com"]
    
    results = {}
    monitor = AlbaConnectionMonitor()
    
    for host in hosts:
        latency = monitor.ping_host(host)
        results[host] = {
            'latency': f"{latency:.1f}ms" if latency else "timeout",
            'status': "online" if latency else "offline",
            'raw_latency': latency
        }
    
    return results

def main():
    """Funksioni kryesor për test"""
    print("Alba Connection Monitor - Sistemi i Monitorimit të Lidhjeve")
    print("=" * 60)
    
    if not PING3_AVAILABLE:
        print("❌ ping3 nuk është i instaluar!")
        print("Instaloni me: pip install ping3")
        return
    
    # Test i shpejtë
    print("🔍 Duke kryer test të shpejtë...")
    results = quick_ping_test()
    
    for host, data in results.items():
        status_icon = "✅" if data['status'] == 'online' else "❌"
        print(f"{status_icon} {host}: {data['latency']}")
    
    print("\n🚀 Për të filluar monitorimin e plotë, përdorni:")
    print("monitor = AlbaConnectionMonitor()")
    print("await monitor.start_monitoring()")

if __name__ == "__main__":
    main()


