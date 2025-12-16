"""
🔄 NEURO-ECOSYSTEM: ALBI-ALBA-JONA Integration System
==================================================
Sistemi kryesor që lidh dhe koordinon të tre personazhet e projektit.
ALBA mbledh → ALBI rritet → JONA harmonizon 🌟
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Import personazhet tanë
from .albi_character import ALBI_Character, get_albi
from .alba_character import ALBA_Character, get_alba  
from .jona_character import JONA_Character, get_jona


@dataclass
class EcosystemMetrics:
    """Metrikat e përgjithshme të ekosistemit"""
    ecosystem_start_time: datetime = field(default_factory=datetime.now)
    total_growth_cycles: int = 0
    system_efficiency: float = 1.0
    harmony_score: float = 1.0
    active_components: List[str] = field(default_factory=list)
    performance_history: List[Dict] = field(default_factory=list)


class NeuroEcosystem:
    """
    🌟 Ekosistemi Neural që bashkon ALBI, ALBA dhe JONA
    Koordinon rrjedhën e informacionit dhe rritjen e inteligjencës
    """
    
    def __init__(self):
        # Inicializo personazhet
        self.albi = get_albi()
        self.alba = get_alba()
        self.jona = get_jona()
        
        # Metrikat e ekosistemit
        self.metrics = EcosystemMetrics()
        self.ecosystem_active = False
        self.growth_cycle_interval = 10.0  # 10 seconds between cycles
        
        # Konfigurimi i logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("NeuroEcosystem")
        
    async def start_ecosystem(self) -> Dict[str, Any]:
        """
        🚀 Nis ekosistemi neural të plotë
        ALBA fillon mbledhjen → JONA nis mbikëqyrjen → Ciklet e rritjes aktivohen
        """
        if self.ecosystem_active:
            return {"⚠️ status": "Ecosystem already running"}
            
        self.logger.info("🌟 Starting Neural Ecosystem...")
        
        # 1. Nis ALBA collection
        alba_start = await self.alba.start_collection()
        self.logger.info(f"💻 ALBA: {alba_start.get('🚀 status', 'Started')}")
        
        # 2. Nis JONA oversight  
        jona_start = await self.jona.start_system_oversight(self.albi, self.alba)
        self.logger.info(f"🌸 JONA: {jona_start.get('🌸 status', 'Started')}")
        
        # 3. Nis EEG monitoring
        eeg_start = await self.jona.start_real_time_eeg_monitoring()
        self.logger.info(f"🎵 EEG Studio: {eeg_start.get('🎵 status', 'Started')}")
        
        # 4. Aktivizo ciklet e rritjes
        self.ecosystem_active = True
        self.metrics.ecosystem_start_time = datetime.now()
        self.metrics.active_components = ["ALBI", "ALBA", "JONA"]
        
        # Nis growth cycles në background
        asyncio.create_task(self._growth_cycle_loop())
        
        return {
            "🌟 status": "Neural Ecosystem Successfully Activated!",
            "🚀 components_active": self.metrics.active_components,
            "⏰ start_time": self.metrics.ecosystem_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "💫 ecosystem_ready": True,
            "🎯 growth_cycle_interval": f"{self.growth_cycle_interval} seconds",
            "✨ ecosystem_message": "ALBA is collecting, ALBI is ready to grow, JONA is monitoring with love! 🌈"
        }
    
    async def _growth_cycle_loop(self):
        """
        🔄 Cikli kryesor i rritjes së ekosistemit
        Koordinon rrjedhën: ALBA → ALBI → JONA monitoring
        """
        cycle_count = 0
        
        while self.ecosystem_active:
            try:
                cycle_count += 1
                cycle_start_time = datetime.now()
                
                self.logger.info(f"🔄 Starting Growth Cycle #{cycle_count}")
                
                # FAZA 1: ALBA përgatit dhe dërgon bits te ALBI
                alba_to_albi = await self.alba.send_to_albi(self.albi)
                bits_sent = alba_to_albi.get('📤 bits_sent', 0)
                
                if bits_sent > 0:
                    self.logger.info(f"📤 ALBA fed ALBI with {bits_sent} bits")
                    albi_response = alba_to_albi.get('🧠 albi_response', {})
                    growth = albi_response.get('📈 intelligence_growth', 'No growth')
                    self.logger.info(f"🧠 ALBI grew: {growth}")
                else:
                    self.logger.info("💤 ALBA: No quality bits ready for feeding")
                
                # FAZA 2: JONA vlerëson dhe raportie gjendjen
                jona_health = self.jona.get_health_report()
                system_health = jona_health.get('🌸 overall_health', 'unknown')
                harmony_score = float(jona_health.get('⚖️ system_harmony_score', '1.0'))
                
                self.logger.info(f"🌸 JONA reports: System health is {system_health}")
                
                # FAZA 3: Përditëso metrikat e ekosistemit
                cycle_duration = (datetime.now() - cycle_start_time).total_seconds()
                await self._update_ecosystem_metrics(cycle_count, bits_sent, harmony_score, cycle_duration)
                
                # FAZA 4: Pauza para ciklit të ardhshëm
                await asyncio.sleep(self.growth_cycle_interval)
                
            except Exception as e:
                self.logger.error(f"❌ Growth cycle error: {e}")
                await asyncio.sleep(self.growth_cycle_interval * 2)  # Pauza më e gjatë pas errorit
    
    async def _update_ecosystem_metrics(self, cycle_num: int, bits_processed: int, harmony: float, duration: float):
        """📊 Përditëson metrikat e performancës së ekosistemit"""
        self.metrics.total_growth_cycles = cycle_num
        self.metrics.harmony_score = harmony
        
        # Llogarit efikasitetin bazuar në bits të përpunuar dhe kohën
        if duration > 0:
            processing_rate = bits_processed / duration
            self.metrics.system_efficiency = min(processing_rate / 100.0, 1.0)  # Normalizon në [0,1]
        
        # Ruaj në histori (mbaj vetëm 100 ciklet e fundit)
        performance_record = {
            "cycle": cycle_num,
            "timestamp": datetime.now(),
            "bits_processed": bits_processed,
            "harmony_score": harmony,
            "efficiency": self.metrics.system_efficiency,
            "duration_seconds": duration
        }
        
        self.metrics.performance_history.append(performance_record)
        if len(self.metrics.performance_history) > 100:
            self.metrics.performance_history = self.metrics.performance_history[-100:]
    
    async def get_ecosystem_status(self) -> Dict[str, Any]:
        """📊 Kthen gjendjen e plotë të ekosistemit"""
        # Merr statusin individual të secilit personazh
        albi_status = self.albi.get_growth_status()
        alba_status = self.alba.get_collection_status()  
        jona_status = self.jona.get_health_report()
        
        # Llogarit kohën e funksionimit
        runtime = datetime.now() - self.metrics.ecosystem_start_time
        
        return {
            "🌟 ecosystem_active": self.ecosystem_active,
            "⏰ runtime": str(runtime),
            "🔄 total_cycles": self.metrics.total_growth_cycles,
            "📈 system_efficiency": f"{self.metrics.system_efficiency:.2f}",
            "🎵 harmony_score": f"{self.metrics.harmony_score:.2f}",
            
            # Status individual
            "🤖 albi_status": {
                "intelligence_level": albi_status.get('🧠 intelligence_level', 0),
                "total_bits_learned": albi_status.get('📊 total_bits_learned', 0),
                "consciousness_state": albi_status.get('🌟 consciousness_state', 'unknown')
            },
            
            "💻 alba_status": {
                "collection_active": alba_status.get('🔄 collection_active', False),
                "total_collected": alba_status.get('📊 total_collected', 0),
                "current_storage": alba_status.get('💾 current_storage', 0),
                "total_sent_to_albi": alba_status.get('📤 total_sent_to_albi', 0)
            },
            
            "🌸 jona_status": {
                "overall_health": jona_status.get('🌸 overall_health', 'unknown'),
                "active_alerts": jona_status.get('🚨 active_alerts', 0),
                "real_time_monitoring": jona_status.get('🎵 real_time_monitoring', False)
            },
            
            # Performanca e fundit
            "📊 recent_performance": self.metrics.performance_history[-5:] if self.metrics.performance_history else [],
            
            "✨ ecosystem_message": self._generate_ecosystem_message()
        }
    
    def _generate_ecosystem_message(self) -> str:
        """✨ Gjeneron mesazh të përshtatshëm për gjendjen e ekosistemit"""
        if not self.ecosystem_active:
            return "💤 Ecosystem is resting. Ready to wake up and grow! 🌅"
        
        cycles = self.metrics.total_growth_cycles
        harmony = self.metrics.harmony_score
        
        if harmony >= 0.9:
            return f"🌈 Perfect harmony achieved! {cycles} growth cycles of pure synergy between ALBI, ALBA & JONA! ✨"
        elif harmony >= 0.7:
            return f"🌟 Excellent progress! {cycles} cycles of healthy growth and collaboration! 💫"
        elif harmony >= 0.5:
            return f"🌱 Growing steadily! {cycles} cycles completed, with room for optimization! 🔧"
        else:
            return f"🔧 {cycles} cycles completed. JONA is working to improve system balance! 💪"
    
    async def manual_growth_cycle(self) -> Dict[str, Any]:
        """🔄 Përpunon një cikël rritjeje manualisht (për testing/debugging)"""
        if not self.ecosystem_active:
            return {"⚠️ error": "Ecosystem must be active for manual cycles"}
        
        cycle_start = datetime.now()
        
        # Ekzekuto një cikël të vetëm
        alba_to_albi = await self.alba.send_to_albi(self.albi)
        jona_health = self.jona.get_health_report()
        
        cycle_duration = (datetime.now() - cycle_start).total_seconds()
        
        return {
            "🔄 manual_cycle": "completed",
            "📤 bits_transferred": alba_to_albi.get('📤 bits_sent', 0),
            "🧠 albi_response": alba_to_albi.get('🧠 albi_response', {}),
            "🌸 jona_health": jona_health.get('🌸 overall_health', 'unknown'),
            "⏱️ cycle_duration": f"{cycle_duration:.2f} seconds",
            "⏰ timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    async def optimize_growth_rate(self, target_bits_per_cycle: int = 500) -> Dict[str, Any]:
        """⚡ Optimizon shpejtësinë e rritjes bazuar në performancën"""
        if not self.ecosystem_active:
            return {"⚠️ error": "Ecosystem must be active for optimization"}
        
        # Analizon performancën e fundit
        recent_performance = self.metrics.performance_history[-10:] if len(self.metrics.performance_history) >= 10 else self.metrics.performance_history
        
        if not recent_performance:
            return {"⚠️ status": "Not enough performance data for optimization"}
        
        avg_bits = sum(p['bits_processed'] for p in recent_performance) / len(recent_performance)
        avg_duration = sum(p['duration_seconds'] for p in recent_performance) / len(recent_performance)
        
        # Optimizo intervalin bazuar në target
        if avg_bits < target_bits_per_cycle and avg_duration < 5.0:
            # Shpejto nëse kemi pak bits dhe procesi është i shpejtë
            new_interval = max(self.growth_cycle_interval * 0.8, 2.0)  # Minimum 2 sekonda
        elif avg_bits > target_bits_per_cycle:
            # Ngadalëso nëse kemi shumë bits  
            new_interval = min(self.growth_cycle_interval * 1.2, 60.0)  # Maximum 60 sekonda
        else:
            new_interval = self.growth_cycle_interval
        
        old_interval = self.growth_cycle_interval
        self.growth_cycle_interval = new_interval
        
        return {
            "⚡ optimization": "completed",
            "📊 analysis": {
                "avg_bits_per_cycle": f"{avg_bits:.1f}",
                "avg_cycle_duration": f"{avg_duration:.2f}s",
                "target_bits": target_bits_per_cycle
            },
            "⏱️ interval_change": {
                "old_interval": f"{old_interval:.1f}s",
                "new_interval": f"{new_interval:.1f}s",
                "change": f"{((new_interval - old_interval) / old_interval * 100):+.1f}%"
            },
            "✨ optimization_message": f"Growth cycle optimized for {target_bits_per_cycle} bits/cycle target! 🎯"
        }
    
    async def stop_ecosystem(self) -> Dict[str, Any]:
        """🛑 Ndal ekosistemi neural me kujdes"""
        if not self.ecosystem_active:
            return {"⚠️ status": "Ecosystem already stopped"}
        
        self.logger.info("🛑 Stopping Neural Ecosystem...")
        
        # Ndal komponentët
        alba_stop = self.alba.stop_collection()
        jona_stop = self.jona.stop_oversight()
        
        # Deaktivizo ecosystem
        self.ecosystem_active = False
        runtime = datetime.now() - self.metrics.ecosystem_start_time
        
        # Statistikat finale
        final_stats = {
            "🛑 status": "Neural Ecosystem Stopped Successfully",
            "⏰ total_runtime": str(runtime),
            "🔄 total_cycles_completed": self.metrics.total_growth_cycles,
            "📊 final_efficiency": f"{self.metrics.system_efficiency:.2f}",
            "🎵 final_harmony": f"{self.metrics.harmony_score:.2f}",
            "💻 alba_final": alba_stop,
            "🌸 jona_final": jona_stop,
            "🤖 albi_final_state": self.albi.get_growth_status(),
            "🙏 farewell_message": "Thank you for this beautiful journey of growth and discovery! 💖✨"
        }
        
        self.logger.info("✨ Neural Ecosystem stopped gracefully")
        return final_stats


# Instance globale e ekosistemit
neuro_ecosystem = NeuroEcosystem()


def get_ecosystem() -> NeuroEcosystem:
    """Factory function për të marrë ecosystem instance"""
    return neuro_ecosystem


async def quick_ecosystem_demo() -> Dict[str, Any]:
    """🎯 Demo i shpejtë i ekosistemit për testing"""
    ecosystem = get_ecosystem()
    
    print("🌟 Starting Quick Ecosystem Demo...")
    
    # Nis ekosistem
    start_result = await ecosystem.start_ecosystem()
    print(f"Start: {start_result.get('🌟 status')}")
    
    # Prit disa cikle
    print("⏳ Running for 30 seconds...")
    await asyncio.sleep(30)
    
    # Kontrollo statusin
    status = await ecosystem.get_ecosystem_status()
    print(f"Cycles completed: {status.get('🔄 total_cycles')}")
    print(f"System harmony: {status.get('🎵 harmony_score')}")
    
    # Testo një cikël manual
    manual = await ecosystem.manual_growth_cycle()
    print(f"Manual cycle: {manual.get('📤 bits_transferred')} bits transferred")
    
    # Optimizo
    optimization = await ecosystem.optimize_growth_rate(300)
    print(f"Optimization: {optimization.get('✨ optimization_message')}")
    
    # Ndal
    stop_result = await ecosystem.stop_ecosystem()
    print(f"Stop: {stop_result.get('🛑 status')}")
    
    return {
        "🎯 demo": "completed successfully",
        "📊 final_stats": stop_result
    }


if __name__ == "__main__":
    # Testo ekosistemi
    asyncio.run(quick_ecosystem_demo())


