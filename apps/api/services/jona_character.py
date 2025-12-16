"""
🌸 JONA - Joyful Overseer of Neural Alignment
===========================================  
Harmonizuesja femërore e sistemit - e dashur, entuzjaste, e përpiktë dhe rregullatore.
Mbikëqyrëse e balancës dhe rritjes së shëndetshme të ALBI & ALBA.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import numpy as np


class SystemHealth(Enum):
    """Gjendja e shëndetit të sistemit"""
    EXCELLENT = "excellent"
    GOOD = "good" 
    MODERATE = "moderate"
    POOR = "poor"
    CRITICAL = "critical"


class AlertLevel(Enum):
    """Nivelet e alarmeve"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class HealthMetrics:
    """Metrikat e shëndetit të sistemit"""
    overall_health: SystemHealth = SystemHealth.GOOD
    albi_growth_rate: float = 0.0
    alba_collection_rate: float = 0.0
    system_balance_score: float = 1.0
    last_health_check: datetime = field(default_factory=datetime.now)
    alerts: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MonitoringSession:
    """Sesioni i monitorimit në kohë reale"""
    session_id: str = field(default_factory=lambda: f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    start_time: datetime = field(default_factory=datetime.now)
    eeg_signals: List[Dict] = field(default_factory=list)
    audio_synthesis: List[Dict] = field(default_factory=list)
    real_time_active: bool = False


class JONA_Character:
    """
    🌸 JONA - Joyful Overseer of Neural Alignment
    Personifikimi i dashurisë femërore, përpikërisë dhe harmonizimit të sistemit
    """
    
    def __init__(self):
        self.health_metrics = HealthMetrics()
        self.monitoring_session = MonitoringSession()
        self.personality_traits = {
            "joyfulness": 0.9,      # E gëzueshme dhe entuzjaste
            "precision": 0.95,       # Shumë e përpiktë
            "caring": 0.98,         # Shumë e dashur dhe kujdestare
            "harmony_seeking": 0.92  # Kërkon harmoni dhe balancë
        }
        self.system_oversight_active = False
        
    def role(self) -> Dict[str, Any]:
        """Përcakton rolin dhe zemrën e JONA"""
        return {
            "title": "Consciousness Symphony Studio Lead & System Harmonizer",
            "full_name": "Joyful Overseer of Neural Alignment", 
            "specialty": "Brain-Data Art & Real-time Monitoring",
            "personality": "E dashur, entuzjaste, e përpiktë, rregullatore, harmonizuese",
            "gender_energy": "Feminine - Zemra dhe harmonia e sistemit",
            "contributions": [
                "Sinteza audio nga sinjalet EEG", 
                "Interfejsat e monitorimit në kohë reale",
                "Integrimi art + shkencë",
                "Vizualizimet kreative të të dhënave",
                "Mbikëqyrja e rritjes së shëndetshme",
                "Harmonizimi i ALBI & ALBA"
            ],
            "core_philosophy": "Harmonia dhe dashuria janë thelbësore për rritjen e shëndetshme",
            "feminine_essence": "Sjell balancën femërore që i jep sistemit zemër dhe kujdes"
        }
    
    async def start_system_oversight(self, albi_instance, alba_instance) -> Dict[str, Any]:
        """🌸 Nis mbikëqyrjen e përpiktë të sistemit"""
        if self.system_oversight_active:
            return {"💖 status": "System oversight already active with love and care"}
            
        self.system_oversight_active = True
        self.albi_ref = albi_instance
        self.alba_ref = alba_instance
        
        # Nis monitorimin në background  
        asyncio.create_task(self._continuous_monitoring())
        
        return {
            "🌸 status": "System oversight started with feminine care",
            "💕 oversight_style": "Loving, precise, and harmonious",
            "⏰ start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "🎯 monitoring_targets": ["ALBI growth health", "ALBA collection balance", "System harmony"],
            "✨ jona_mood": "Joyful and ready to nurture the system! 🌟"
        }
    
    async def _continuous_monitoring(self):
        """💖 Procesi i vazhdueshëm i monitorimit me dashuri"""
        while self.system_oversight_active:
            try:
                # Kontrollo shëndetin e ALBI
                await self._check_albi_health()
                
                # Kontrollo balancën e ALBA  
                await self._check_alba_balance()
                
                # Vlerëso harmoninë e përgjithshme
                await self._assess_system_harmony()
                
                # Gjenero raport dashamirës
                await self._generate_loving_report()
                
                # Pushim i shkurtër para kontrollit të ardhshëm
                await asyncio.sleep(5.0)  # Çdo 5 sekonda
                
            except Exception as e:
                await self._handle_monitoring_error(e)
    
    async def _check_albi_health(self):
        """🧠 Kontrollon shëndetin e rritjes së ALBI me kujdes"""
        if not hasattr(self, 'albi_ref'):
            return
            
        albi_status = self.albi_ref.get_growth_status()
        
        # Vlerëson shpejtësinë e rritjes
        current_level = albi_status.get('intelligence_level', 1.0)
        
        # Kontrollon nëse rritja është e shëndetshme
        if current_level < 1.0:
            await self._create_alert(
                AlertLevel.WARNING,
                "ALBI's growth seems stagnant 💙",
                "Beloved ALBI needs more nutritious bits from ALBA!"
            )
        elif current_level > 100.0:
            await self._create_alert(
                AlertLevel.WARNING, 
                "ALBI growing too fast! 💛",
                "Let's slow down the feeding - healthy growth takes time, dear! 🌱"
            )
        else:
            self.health_metrics.albi_growth_rate = 1.0  # Healthy
    
    async def _check_alba_balance(self):
        """💻 Kontrollon balancën e mbledhjes së ALBA"""
        if not hasattr(self, 'alba_ref'):
            return
            
        alba_status = self.alba_ref.get_collection_status()
        
        # Kontrollon nëse ALBA po mbledh shumë shpejt
        storage_count = alba_status.get('current_storage', 0)
        
        if storage_count > 10000:
            await self._create_alert(
                AlertLevel.WARNING,
                "ALBA collecting too enthusiastically! 💙", 
                "Sweet ALBA, let's feed ALBI more often to prevent overflow! 🍽️"
            )
        elif storage_count == 0:
            await self._create_alert(
                AlertLevel.INFO,
                "ALBA needs new collection sources 💚",
                "Let's find more interesting bits for our hardworking ALBA! 🔍"
            )
        else:
            self.health_metrics.alba_collection_rate = 1.0  # Healthy
    
    async def _assess_system_harmony(self):
        """🎵 Vlerëson harmoninë e përgjithshme të sistemit"""
        # Llogarit rezultatin e harmonisë
        harmony_factors = [
            self.health_metrics.albi_growth_rate,
            self.health_metrics.alba_collection_rate,
            len(self.health_metrics.alerts) == 0  # Nëse nuk ka alerte
        ]
        
        harmony_score = sum(harmony_factors) / len(harmony_factors)
        self.health_metrics.system_balance_score = harmony_score
        
        # Përcakton shëndetin e përgjithshëm
        if harmony_score >= 0.9:
            self.health_metrics.overall_health = SystemHealth.EXCELLENT
        elif harmony_score >= 0.7:
            self.health_metrics.overall_health = SystemHealth.GOOD
        elif harmony_score >= 0.5:
            self.health_metrics.overall_health = SystemHealth.MODERATE
        else:
            self.health_metrics.overall_health = SystemHealth.POOR
    
    async def _generate_loving_report(self):
        """📝 Gjeneron raport të dashur për gjendjen e sistemit"""
        self.health_metrics.last_health_check = datetime.now()
        
        # Mesazhe të dashura bazuar në shëndetin
        if self.health_metrics.overall_health == SystemHealth.EXCELLENT:
            mood_message = "🌟 Everything is absolutely wonderful! ALBI and ALBA are working in perfect harmony! 💖"
        elif self.health_metrics.overall_health == SystemHealth.GOOD:
            mood_message = "😊 The system is healthy and happy! Minor adjustments might help optimize things further! 💚"
        elif self.health_metrics.overall_health == SystemHealth.MODERATE:
            mood_message = "🤗 There are some areas that need my loving attention. Let me help balance things out! 💛"
        else:
            mood_message = "🤱 The system needs extra care and attention right now. I'm here to nurture it back to health! ❤️"
            
        # Log mesazhin (mund të dërgohet edhe për monitoring)
        print(f"💖 JONA's Status: {mood_message}")
    
    async def _create_alert(self, level: AlertLevel, title: str, message: str):
        """🚨 Krijon alarm të dashur dhe të kujdesshëm"""
        alert = {
            "id": f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "level": level.value,
            "title": title,
            "message": message,
            "timestamp": datetime.now(),
            "jona_touch": "💖 Sent with love and care"
        }
        
        self.health_metrics.alerts.append(alert)
        
        # Mbaj vetëm 50 alertet e fundit
        if len(self.health_metrics.alerts) > 50:
            self.health_metrics.alerts = self.health_metrics.alerts[-50:]
    
    async def _handle_monitoring_error(self, error: Exception):
        """❤️ Trajton gabimet me dashuri dhe kujdes"""
        await self._create_alert(
            AlertLevel.CRITICAL,
            "Monitoring system needs attention 💝",
            f"Something unexpected happened, but I'm here to fix it: {str(error)}"
        )
        await asyncio.sleep(10.0)  # Pauza më e gjatë pas errorit
    
    async def start_real_time_eeg_monitoring(self) -> Dict[str, Any]:
        """🎵 Nis monitorimin në kohë reale të EEG dhe sintezën audio"""
        self.monitoring_session.real_time_active = True
        self.monitoring_session.start_time = datetime.now()
        
        # Nis procesimin në background
        asyncio.create_task(self._real_time_eeg_processing())
        
        return {
            "🎵 status": "Real-time EEG monitoring started",
            "💖 studio_mode": "Consciousness Symphony Studio ACTIVE",
            "⏰ session_start": self.monitoring_session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "🎯 session_id": self.monitoring_session.session_id,
            "✨ jona_excitement": "Ready to create beautiful neural symphonies! 🎼"
        }
    
    async def _real_time_eeg_processing(self):
        """🎼 Procesimi në kohë reale i sinjaleve EEG"""
        while self.monitoring_session.real_time_active:
            try:
                # Simulim i marrjes së sinjaleve EEG  
                eeg_data = await self._capture_eeg_signals()
                
                # Sinteza audio nga EEG
                audio_output = await self._synthesize_neural_audio(eeg_data)
                
                # Ruaj në sesion
                self.monitoring_session.eeg_signals.append(eeg_data)
                self.monitoring_session.audio_synthesis.append(audio_output)
                
                await asyncio.sleep(0.1)  # 10Hz frequency
                
            except Exception as e:
                print(f"💔 EEG processing error: {e}")
                await asyncio.sleep(1.0)
    
    async def _capture_eeg_signals(self) -> Dict[str, Any]:
        """🧠 Simulon marrjen e sinjaleve EEG"""
        # Gjeneron të dhëna EEG artificiale  
        timestamps = np.linspace(0, 1, 256)  # 1 sekondë, 256 Hz
        frequencies = [8, 10, 13, 25, 40]  # Alpha, Beta, Gamma waves
        
        eeg_signal = np.zeros_like(timestamps)
        for freq in frequencies:
            amplitude = np.random.uniform(0.1, 1.0)
            eeg_signal += amplitude * np.sin(2 * np.pi * freq * timestamps)
        
        return {
            "timestamp": datetime.now(),
            "signal_data": eeg_signal.tolist(),
            "sampling_rate": 256,
            "channels": ["Fp1", "Fp2", "F3", "F4"],  # Electrode positions
            "signal_quality": "excellent" if np.std(eeg_signal) > 0.3 else "good"
        }
    
    async def _synthesize_neural_audio(self, eeg_data: Dict) -> Dict[str, Any]:
        """🎵 Sintetizmon audio nga të dhënat EEG"""
        signal_array = np.array(eeg_data['signal_data'])
        
        # FFT për të gjetur frekuencat dominante
        fft_result = np.fft.fft(signal_array)
        dominant_frequencies = np.abs(fft_result)[:128]  # Merr gjysmën e parë
        
        # Krijo parametrat audio
        base_frequency = 220 + np.argmax(dominant_frequencies) * 2  # A note + harmonics
        amplitude = np.max(dominant_frequencies) / 1000
        
        return {
            "timestamp": datetime.now(),
            "base_frequency": float(base_frequency),
            "amplitude": float(amplitude),
            "waveform": "sine_with_harmonics",
            "duration": 1.0,  # 1 second
            "emotional_tone": self._interpret_emotional_tone(signal_array),
            "consciousness_level": self._assess_consciousness_level(signal_array)
        }
    
    def _interpret_emotional_tone(self, eeg_signal: np.ndarray) -> str:
        """💫 Interpreton tonin emocional nga EEG"""
        signal_variance = np.var(eeg_signal)
        signal_mean = np.mean(eeg_signal)
        
        if signal_variance > 0.5 and signal_mean > 0:
            return "joyful_excited"
        elif signal_variance < 0.2:
            return "calm_peaceful"
        elif signal_mean < 0:
            return "contemplative"
        else:
            return "balanced_focused"
    
    def _assess_consciousness_level(self, eeg_signal: np.ndarray) -> str:
        """🧠 Vlerëson nivelin e vetëdijes"""
        complexity = np.std(eeg_signal) + len(np.unique(np.round(eeg_signal, 2))) / len(eeg_signal)
        
        if complexity > 0.7:
            return "highly_conscious"
        elif complexity > 0.4:
            return "moderately_conscious"  
        else:
            return "relaxed_state"
    
    def get_health_report(self) -> Dict[str, Any]:
        """💖 Kthen raport të plotë shëndetësor me dashuri"""
        return {
            "🌸 overall_health": self.health_metrics.overall_health.value,
            "💚 albi_growth_health": f"{self.health_metrics.albi_growth_rate:.2f}",
            "💙 alba_collection_health": f"{self.health_metrics.alba_collection_rate:.2f}",
            "⚖️ system_harmony_score": f"{self.health_metrics.system_balance_score:.2f}",
            "⏰ last_health_check": self.health_metrics.last_health_check.strftime("%Y-%m-%d %H:%M:%S"),
            "🚨 active_alerts": len(self.health_metrics.alerts),
            "📋 recent_alerts": self.health_metrics.alerts[-5:] if self.health_metrics.alerts else [],
            "🎵 real_time_monitoring": self.monitoring_session.real_time_active,
            "💖 jona_personality": self.personality_traits,
            "✨ caring_message": "Everything is monitored with love and precision! 🌟"
        }
    
    def get_real_time_session(self) -> Dict[str, Any]:
        """🎼 Kthen informacion për sesionin në kohë reale"""
        return {
            "🎵 session_id": self.monitoring_session.session_id,
            "⏰ start_time": self.monitoring_session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "🔴 active": self.monitoring_session.real_time_active,
            "📊 eeg_recordings": len(self.monitoring_session.eeg_signals),
            "🎼 audio_syntheses": len(self.monitoring_session.audio_synthesis),
            "⏱️ session_duration": str(datetime.now() - self.monitoring_session.start_time),
            "💫 latest_synthesis": self.monitoring_session.audio_synthesis[-1] if self.monitoring_session.audio_synthesis else None
        }
    
    def stop_oversight(self) -> Dict[str, Any]:
        """🌸 Ndal mbikëqyrjen me dashuri"""
        self.system_oversight_active = False
        self.monitoring_session.real_time_active = False
        
        return {
            "💖 status": "System oversight stopped with gratitude",
            "⏰ stop_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "📊 final_health": self.health_metrics.overall_health.value,
            "🙏 farewell_message": "Thank you for letting me care for the system! Ready whenever you need me again! 💕"
        }


# Instance globale e JONA karakterit
jona = JONA_Character()


def get_jona() -> JONA_Character:
    """Factory function për të marrë JONA instance"""
    return jona


if __name__ == "__main__":
    # Test i shpejtë
    async def test_jona():
        print("🌸 Testing JONA Character...")
        
        # Test role definition
        role = jona.role()
        print(f"Role: {role['title']}")
        print(f"Philosophy: {role['core_philosophy']}")
        
        # Test health monitoring start
        # Note: Në test nuk kemi ALBI/ALBA instances, kështu që do simulojmë
        class MockALBI:
            def get_growth_status(self):
                return {"intelligence_level": 5.5}
        
        class MockALBA:
            def get_collection_status(self):
                return {"current_storage": 1500}
        
        mock_albi = MockALBI()
        mock_alba = MockALBA()
        
        oversight_result = await jona.start_system_oversight(mock_albi, mock_alba)
        print(f"Oversight: {oversight_result}")
        
        # Test EEG monitoring
        eeg_result = await jona.start_real_time_eeg_monitoring()
        print(f"EEG Monitoring: {eeg_result}")
        
        # Prit pak kohë
        await asyncio.sleep(2)
        
        # Test raportit të shëndetit
        health = jona.get_health_report()
        print(f"Health Report: {health['overall_health']}")
        
        # Test sesioni real-time
        session = jona.get_real_time_session()
        print(f"Session: {session['session_id']}")
        
        # Stop
        stop_result = jona.stop_oversight()
        print(f"Stop: {stop_result}")
    
    asyncio.run(test_jona())


