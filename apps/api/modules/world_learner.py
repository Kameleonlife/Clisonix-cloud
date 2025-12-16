#!/usr/bin/env python3
"""
World Learner Module - Sistemi i te mesuarit te botes
Modul i dedikuar per zhvillim dhe testim
"""

import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class WorldLearner:
    """
    Sistemi kryesor i te mesuarit te botes
    Analiza dhe modelimi i realitetit permes te dhenave
    """
    
    def __init__(self, config_path: str = "config/world_learner.json"):
        self.config_path = config_path
        self.learning_active = False
        self.knowledge_base = {}
        self.observations = []
        self.patterns = {}
        
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        """Konfigurimi i logging per World Learner"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - WorldLearner - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/world_learner.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Ngarkon konfigurimin e World Learner"""
        default_config = {
            "learning_domains": [
                "network_analysis",
                "system_behavior", 
                "user_patterns",
                "performance_metrics",
                "error_patterns",
                "optimization_opportunities"
            ],
            "observation_interval": 60,  # sekonda
            "pattern_threshold": 0.8,
            "max_observations": 1000,
            "auto_learning": True
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.config = {**default_config, **config}
            else:
                self.config = default_config
                self.save_config()
                
        except Exception as e:
            self.logger.error(f"Error ne ngarkimin e konfigurimit: {e}")
            self.config = default_config
            
    def save_config(self):
        """Ruan konfigurimin aktual"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error ne ruajtjen e konfigurimit: {e}")
            
    def observe_world(self, domain: str, data: Dict[str, Any]):
        """Verejtje te reja te botes ne nje domain te caktuar"""
        observation = {
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "data": data,
            "id": len(self.observations)
        }
        
        self.observations.append(observation)
        self.logger.info(f"Observation ne {domain}: {len(data)} data points")
        
        # Mbajtja e numrit te observationeve ne limite
        if len(self.observations) > self.config["max_observations"]:
            self.observations = self.observations[-self.config["max_observations"]:]
            
        # Auto-learning nese eshte aktivizuar
        if self.config["auto_learning"]:
            self.analyze_patterns(domain)
            
    def analyze_patterns(self, domain: str):
        """Analizon patternat ne nje domain te caktuar"""
        domain_observations = [obs for obs in self.observations if obs["domain"] == domain]
        
        if len(domain_observations) < 5:  # Duhen te pakten 5 observations
            return
            
        patterns_found = self.detect_patterns(domain_observations)
        
        if domain not in self.patterns:
            self.patterns[domain] = []
            
        for pattern in patterns_found:
            if pattern["confidence"] >= self.config["pattern_threshold"]:
                self.patterns[domain].append(pattern)
                self.logger.info(f"Pattern i ri ne {domain}: {pattern['description']}")
                
    def detect_patterns(self, observations: List[Dict]) -> List[Dict]:
        """Zbulimi i patternave ne observations"""
        patterns = []
        
        # Pattern 1: Frequency patterns
        frequency_pattern = self.analyze_frequency_patterns(observations)
        if frequency_pattern:
            patterns.append(frequency_pattern)
            
        # Pattern 2: Trend patterns  
        trend_pattern = self.analyze_trend_patterns(observations)
        if trend_pattern:
            patterns.append(trend_pattern)
            
        # Pattern 3: Correlation patterns
        correlation_pattern = self.analyze_correlation_patterns(observations)
        if correlation_pattern:
            patterns.append(correlation_pattern)
            
        return patterns
        
    def analyze_frequency_patterns(self, observations: List[Dict]) -> Optional[Dict]:
        """Analizon patternat e frekuences"""
        if len(observations) < 10:
            return None
            
        # Analizon frekuencen e observationeve ne kohe
        timestamps = [obs["timestamp"] for obs in observations]
        
        # Thjesht per demo - ne realitet do ishte me kompleks
        avg_interval = len(observations) / max(1, len(set(ts[:10] for ts in timestamps)))
        
        if avg_interval > 2:
            return {
                "type": "frequency",
                "description": f"High frequency activity detected: {avg_interval:.2f} events/period",
                "confidence": min(0.9, avg_interval / 10),
                "timestamp": datetime.now().isoformat()
            }
        return None
        
    def analyze_trend_patterns(self, observations: List[Dict]) -> Optional[Dict]:
        """Analizon patternat e trendeve"""
        if len(observations) < 5:
            return None
            
        # Analizon trendin e te dhenave numerike
        numeric_values = []
        for obs in observations:
            if isinstance(obs["data"], dict):
                for key, value in obs["data"].items():
                    if isinstance(value, (int, float)):
                        numeric_values.append(value)
                        
        if len(numeric_values) >= 3:
            # Trend thjesht bazuar ne vlerat e fundit vs te parat
            recent_avg = sum(numeric_values[-3:]) / 3
            old_avg = sum(numeric_values[:3]) / 3
            
            if recent_avg > old_avg * 1.2:
                return {
                    "type": "trend", 
                    "description": f"Increasing trend detected: {recent_avg:.2f} vs {old_avg:.2f}",
                    "confidence": min(0.9, (recent_avg - old_avg) / old_avg),
                    "timestamp": datetime.now().isoformat()
                }
        return None
        
    def analyze_correlation_patterns(self, observations: List[Dict]) -> Optional[Dict]:
        """Analizon korrelaciionet midis te dhenave"""
        if len(observations) < 5:
            return None
            
        # Analizon korrelacionet e thjeshta
        keys_frequency = {}
        for obs in observations:
            if isinstance(obs["data"], dict):
                for key in obs["data"].keys():
                    keys_frequency[key] = keys_frequency.get(key, 0) + 1
                    
        # Gjej keys qe shfaqen se bashku shpesh
        common_keys = [k for k, v in keys_frequency.items() if v >= len(observations) * 0.7]
        
        if len(common_keys) >= 2:
            return {
                "type": "correlation",
                "description": f"Strong correlation between: {', '.join(common_keys[:3])}",
                "confidence": len(common_keys) / max(1, len(keys_frequency)),
                "timestamp": datetime.now().isoformat()
            }
        return None
        
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Kthen permbledhjen e njohurive te mbledhura"""
        summary = {
            "total_observations": len(self.observations),
            "domains": list(set(obs["domain"] for obs in self.observations)),
            "patterns_discovered": len(sum(self.patterns.values(), [])),
            "learning_active": self.learning_active,
            "last_observation": self.observations[-1]["timestamp"] if self.observations else None,
            "config": self.config
        }
        
        # Statistika per domain
        domain_stats = {}
        for domain in summary["domains"]:
            domain_obs = [obs for obs in self.observations if obs["domain"] == domain]
            domain_stats[domain] = {
                "observations": len(domain_obs),
                "patterns": len(self.patterns.get(domain, [])),
                "last_activity": domain_obs[-1]["timestamp"] if domain_obs else None
            }
        summary["domain_statistics"] = domain_stats
        
        return summary
        
    def export_knowledge(self, filepath: str):
        """Eksporton njohurite ne file"""
        knowledge_export = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "total_observations": len(self.observations)
            },
            "observations": self.observations,
            "patterns": self.patterns,
            "knowledge_base": self.knowledge_base,
            "config": self.config
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(knowledge_export, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Knowledge exported to {filepath}")
        except Exception as e:
            self.logger.error(f"Error ne eksportimin e knowledge: {e}")
            
    def import_knowledge(self, filepath: str):
        """Importon njohurite nga file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                knowledge_import = json.load(f)
                
            # Merge observations
            imported_obs = knowledge_import.get("observations", [])
            self.observations.extend(imported_obs)
            
            # Merge patterns
            imported_patterns = knowledge_import.get("patterns", {})
            for domain, patterns in imported_patterns.items():
                if domain not in self.patterns:
                    self.patterns[domain] = []
                self.patterns[domain].extend(patterns)
                
            # Merge knowledge base
            imported_kb = knowledge_import.get("knowledge_base", {})
            self.knowledge_base.update(imported_kb)
            
            self.logger.info(f"Knowledge imported from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error ne importimin e knowledge: {e}")
            
    async def continuous_learning(self):
        """Mesimi i vazhdueshem ne background"""
        self.learning_active = True
        self.logger.info("Continuous learning started")
        
        while self.learning_active:
            try:
                # Analizon te gjitha domain-et
                for domain in self.config["learning_domains"]:
                    self.analyze_patterns(domain)
                    
                # Pastron observations te vjetra
                cutoff_time = time.time() - (24 * 3600)  # 24 ore
                self.observations = [
                    obs for obs in self.observations 
                    if datetime.fromisoformat(obs["timestamp"]).timestamp() > cutoff_time
                ]
                
                await asyncio.sleep(self.config["observation_interval"])
                
            except Exception as e:
                self.logger.error(f"Error ne continuous learning: {e}")
                await asyncio.sleep(60)  # Recovery delay
                
    def stop_learning(self):
        """Ndal mesimin e vazhdueshem"""
        self.learning_active = False
        self.logger.info("Continuous learning stopped")
        
    def demo_world_learning(self):
        """Demo per testimin e funksionalitetit"""
        print("🌍 World Learner Demo")
        print("=" * 50)
        
        # Simulon observations
        demo_observations = [
            {"domain": "network_analysis", "data": {"latency": 12.5, "hosts_online": 18}},
            {"domain": "network_analysis", "data": {"latency": 11.8, "hosts_online": 19}},
            {"domain": "system_behavior", "data": {"cpu_usage": 45.2, "memory_usage": 67.8}},
            {"domain": "user_patterns", "data": {"requests_per_minute": 125, "active_users": 45}},
            {"domain": "network_analysis", "data": {"latency": 13.1, "hosts_online": 17}},
        ]
        
        for obs in demo_observations:
            self.observe_world(obs["domain"], obs["data"])
            time.sleep(1)
            
        # Shfaq summary
        summary = self.get_knowledge_summary()
        print(f"\n📊 Knowledge Summary:")
        print(f"   Total Observations: {summary['total_observations']}")
        print(f"   Domains: {len(summary['domains'])}")
        print(f"   Patterns Discovered: {summary['patterns_discovered']}")
        
        for domain, stats in summary["domain_statistics"].items():
            print(f"   📈 {domain}: {stats['observations']} obs, {stats['patterns']} patterns")
            
        return summary

def main():
    """Funksioni kryesor per dev dhe test"""
    print("🌍 World Learner - Development Module")
    print("=" * 60)
    
    learner = WorldLearner()
    
    # Demo run
    summary = learner.demo_world_learning()
    
    print(f"\n🚀 World Learner ready for development!")
    print(f"   Config: {learner.config_path}")
    print(f"   Logs: logs/world_learner.log")
    
    return learner

if __name__ == "__main__":
    learner = main()


