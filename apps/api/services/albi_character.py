"""
🤖 ALBI - Artificial Labor Born Intelligence
==========================================
Inteligjencë artificiale që LIND nga procesi i punës dhe përpunimit.
Director i Laboratorit Neural - EEG Processing & Brain Signal Analysis
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Any
import numpy as np
from dataclasses import dataclass, field


@dataclass
class IntelligenceGrowthMetrics:
    """Metrikat e rritjes së inteligjencës së ALBI"""
    total_bits_consumed: int = 0
    intelligence_level: float = 1.0
    growth_rate: float = 0.001  # +0.001% për çdo 1000 bits
    last_growth_time: datetime = field(default_factory=datetime.now)
    learning_domains: Dict[str, float] = field(default_factory=dict)


class ALBI_Character:
    """
    🧠 ALBI - Artificial Labor Born Intelligence
    Personazhi kryesor që përpunon sinjalet neurale dhe rritet me çdo informacion
    """
    
    def __init__(self):
        self.growth_metrics = IntelligenceGrowthMetrics()
        self.neural_patterns = {}
        self.consciousness_state = "awakening"
        
    def role(self) -> Dict[str, Any]:
        """Përcakton rolin dhe specializimet e ALBI"""
        return {
            "title": "Neural Frequency Laboratory Director",
            "full_name": "Artificial Labor Born Intelligence",
            "specialty": "EEG Processing & Brain Signal Analysis",
            "personality": "Krijues, intuitiv, në rritje të vazhdueshme",
            "contributions": [
                "Algoritmet e përpunimit neuroakustik",
                "Menaxhimi i frekuencave të trurit", 
                "Analiza e pattern-eve neuronale",
                "Integrimi i shkencës së të dhënave",
                "Sinteza kreative e inteligjencës"
            ],
            "core_philosophy": "Inteligjenca lind nga puna dhe procesi, jo nga programimi"
        }
    
    async def consume_bits(self, bits_data: List[Dict]) -> Dict[str, Any]:
        """
        Ushqehet me bits që i dërgon ALBA dhe rritet inteligjenca
        
        Args:
            bits_data: Lista e bits të mbledhura nga ALBA
            
        Returns:
            Dict me informacionin e rritjes
        """
        total_bits = len(bits_data)
        
        # Përpunimi i bits për rritje
        for bit in bits_data:
            await self._process_single_bit(bit)
            
        # Llogaritja e rritjes së re
        growth_increment = total_bits * self.growth_metrics.growth_rate
        self.growth_metrics.intelligence_level += growth_increment
        self.growth_metrics.total_bits_consumed += total_bits
        self.growth_metrics.last_growth_time = datetime.now()
        
        return {
            "🍽️ bits_consumed": total_bits,
            "📈 intelligence_growth": f"+{growth_increment:.6f}",
            "🧠 current_level": f"{self.growth_metrics.intelligence_level:.6f}",
            "🌱 growth_status": "Healthy continuous learning",
            "💭 new_insights": await self._generate_insights(bits_data)
        }
    
    async def _process_single_bit(self, bit: Dict) -> None:
        """Përpunon një bit të vetëm informacioni"""
        bit_type = bit.get('type', 'unknown')
        
        # Rrit aftësinë në fushën specifike
        if bit_type not in self.growth_metrics.learning_domains:
            self.growth_metrics.learning_domains[bit_type] = 1.0
        else:
            self.growth_metrics.learning_domains[bit_type] += 0.01
            
        # Simulon përpunimin neural
        await asyncio.sleep(0.001)  # Koha e përpunimit
    
    async def _generate_insights(self, bits_data: List[Dict]) -> List[str]:
        """Gjeneron kuptim dhe dije të re nga bits"""
        insights = []
        
        # Analiza e pattern-eve
        patterns = self._analyze_patterns(bits_data)
        if patterns:
            insights.append(f"🔍 Pattern i ri zbuluar: {patterns}")
            
        # Kuptim i ri
        if len(bits_data) > 1000:
            insights.append("💡 Nivel i ri kuptimi u arrit!")
            
        return insights
    
    def _analyze_patterns(self, bits_data: List[Dict]) -> str:
        """Analizon pattern-et në të dhënat e marra"""
        # Implementim i thjeshtë për pattern recognition
        types = [bit.get('type', '') for bit in bits_data]
        most_common = max(set(types), key=types.count) if types else "mixed"
        return f"Dominancë e {most_common} signals"
    
    def get_growth_status(self) -> Dict[str, Any]:
        """Kthen gjendjen aktuale të rritjes"""
        return {
            "🧠 intelligence_level": self.growth_metrics.intelligence_level,
            "📊 total_bits_learned": self.growth_metrics.total_bits_consumed,
            "🌱 growth_rate": f"{self.growth_metrics.growth_rate * 100:.3f}% per 1000 bits",
            "🎯 learning_domains": self.growth_metrics.learning_domains,
            "⏰ last_update": self.growth_metrics.last_growth_time.strftime("%Y-%m-%d %H:%M:%S"),
            "🌟 consciousness_state": self.consciousness_state
        }
    
    async def neural_frequency_analysis(self, eeg_data: np.ndarray) -> Dict[str, Any]:
        """
        Analiza kryesore e frekuencave neurale - specializimi i ALBI
        """
        # Simulim i analizës EEG
        frequencies = np.fft.fft(eeg_data)
        dominant_freq = np.argmax(np.abs(frequencies))
        
        return {
            "🌊 dominant_frequency": f"{dominant_freq} Hz",
            "📈 signal_strength": float(np.max(np.abs(frequencies))),
            "🧠 brain_state": self._interpret_brain_state(dominant_freq),
            "🎵 neural_symphony_ready": True if dominant_freq > 0 else False
        }
    
    def _interpret_brain_state(self, frequency: float) -> str:
        """Interpreton gjendjen e trurit bazuar në frekuencë"""
        if frequency < 4:
            return "Delta - Gjumë i thellë"
        elif frequency < 8:
            return "Theta - Meditim i thellë"
        elif frequency < 12:
            return "Alpha - Relaksim aktiv"
        elif frequency < 30:
            return "Beta - Vëmendje aktive"
        else:
            return "Gamma - Përqendrim i lartë"


# Instance globale e ALBI karakterit
albi = ALBI_Character()


def get_albi() -> ALBI_Character:
    """Factory function për të marrë ALBI instance"""
    return albi


if __name__ == "__main__":
    # Test i shpejtë
    async def test_albi():
        print("🤖 Testing ALBI Character...")
        
        # Test role definition  
        role = albi.role()
        print(f"Role: {role['title']}")
        
        # Test bits consumption
        test_bits = [
            {"type": "eeg_signal", "value": 0.5, "timestamp": datetime.now()},
            {"type": "neural_pattern", "value": 0.8, "timestamp": datetime.now()},
            {"type": "frequency_data", "value": 0.3, "timestamp": datetime.now()}
        ]
        
        growth_result = await albi.consume_bits(test_bits)
        print(f"Growth Result: {growth_result}")
        
        # Test status
        status = albi.get_growth_status()
        print(f"Status: {status}")
    
    asyncio.run(test_albi())


