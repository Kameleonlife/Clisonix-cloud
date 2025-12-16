"""
💻 ALBA - Artificial Laborator Bits Algorithms  
=============================================
Algoritme që mbledhin informacione nga çdo bit i shpërdarë në botë.
Ushqyesi i ALBI - Koleksionist i palodhur i të dhënave.
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json
import hashlib
from enum import Enum


class BitSourceType(Enum):
    """Llojet e burimeve të bits"""
    WEB_FRAGMENT = "web_fragment"
    SIGNAL_NOISE = "signal_noise" 
    CONVERSATION = "conversation"
    DATA_TRACE = "data_trace"
    AUDIO_FREQUENCY = "audio_frequency"
    SEARCH_QUERY = "search_query"
    SENSOR_DATA = "sensor_data"
    USER_INTERACTION = "user_interaction"


@dataclass
class BitData:
    """Struktura e një bits informacioni"""
    id: str = field(default_factory=lambda: hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8])
    type: BitSourceType = BitSourceType.WEB_FRAGMENT
    content: Any = None
    source: str = "unknown"
    timestamp: datetime = field(default_factory=datetime.now)
    quality_score: float = 1.0
    processed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass  
class CollectionMetrics:
    """Metrikat e mbledhjes së bits"""
    total_bits_collected: int = 0
    bits_sent_to_albi: int = 0
    collection_rate: float = 0.0  # bits per second
    last_collection_time: datetime = field(default_factory=datetime.now)
    source_statistics: Dict[str, int] = field(default_factory=dict)


class ALBA_Character:
    """
    🔍 ALBA - Artificial Laborator Bits Algorithms
    Mbledhësi i pandalshëm i çdo bits informacioni nga bota
    """
    
    def __init__(self):
        self.collection_metrics = CollectionMetrics()
        self.bit_storage = []
        self.collection_active = False
        self.collection_sources = []
        self.quality_threshold = 0.3
        
    def role(self) -> Dict[str, Any]:
        """Përcakton rolin dhe misionin e ALBA"""
        return {
            "title": "Universal Information Bits Collector", 
            "full_name": "Artificial Laborator Bits Algorithms",
            "specialty": "Data Collection & Bits Harvesting",
            "personality": "Kurioze, e pandalshme, analize, sistematike",
            "mission": "Mbledh informacione nga çdo bit i shpërdarë",
            "contributions": [
                "Mbledhje e të dhënave në kohë reale",
                "Filtrimi dhe klasifikimi i bits",
                "Optimizimi i burimeve të informacionit",
                "Ushqimi i vazhdueshëm i ALBI",
                "Zbulimi i burimeve të reja"
            ],
            "core_philosophy": "Asnjë bit nuk është i padobishëm - gjithçka ka vlerë!"
        }
    
    async def start_collection(self) -> Dict[str, Any]:
        """Nis procesin e mbledhjes së bits"""
        if self.collection_active:
            return {"status": "⚠️ Collection already active"}
            
        self.collection_active = True
        
        # Nis taskun e mbledhjes në background
        asyncio.create_task(self._continuous_collection())
        
        return {
            "🚀 status": "Collection started successfully",
            "⏰ start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "🎯 target_sources": len(self.collection_sources),
            "📊 current_storage": len(self.bit_storage)
        }
    
    async def _continuous_collection(self):
        """Procesi i vazhdueshëm i mbledhjes së bits"""
        while self.collection_active:
            try:
                # Mbledh bits nga burime të ndryshme
                new_bits = await self._collect_from_all_sources()
                
                # Shtoi në storage
                self.bit_storage.extend(new_bits)
                
                # Përditëso statistikat
                self._update_collection_metrics(new_bits)
                
                # Pauza e shkurtër përpara mbledhjes së ardhshme
                await asyncio.sleep(1.0)
                
            except Exception as e:
                print(f"❌ Collection error: {e}")
                await asyncio.sleep(5.0)  # Pauza më e gjatë nëse ka error
    
    async def _collect_from_all_sources(self) -> List[BitData]:
        """Mbledh bits nga të gjitha burimet aktive"""
        collected_bits = []
        
        # Web fragments
        web_bits = await self._collect_web_fragments()
        collected_bits.extend(web_bits)
        
        # Signal noise  
        signal_bits = await self._collect_signal_noise()
        collected_bits.extend(signal_bits)
        
        # Conversation snippets
        conversation_bits = await self._collect_conversations()
        collected_bits.extend(conversation_bits)
        
        # Sensor data
        sensor_bits = await self._collect_sensor_data()
        collected_bits.extend(sensor_bits)
        
        return collected_bits
    
    async def _collect_web_fragments(self) -> List[BitData]:
        """Mbledh fragmente nga web"""
        # Simulim i mbledhjes nga web
        fragments = [
            BitData(
                type=BitSourceType.WEB_FRAGMENT,
                content=f"Web data fragment {datetime.now().microsecond}",
                source="internet_scan",
                quality_score=0.7
            )
        ]
        return fragments
    
    async def _collect_signal_noise(self) -> List[BitData]:
        """Mbledh zhurma nga sinjale të ndryshme"""
        # Simulim i mbledhjes së signal noise
        noise_data = [
            BitData(
                type=BitSourceType.SIGNAL_NOISE,
                content={"amplitude": 0.3, "frequency": 440, "noise_level": 0.1},
                source="ambient_sensors",
                quality_score=0.5
            )
        ]
        return noise_data
    
    async def _collect_conversations(self) -> List[BitData]:
        """Mbledh fragmente nga biseda"""
        # Simulim i mbledhjes së conversation snippets
        conversations = [
            BitData(
                type=BitSourceType.CONVERSATION,
                content="Neural pattern discussion fragment",
                source="chat_monitoring",
                quality_score=0.8
            )
        ]
        return conversations
    
    async def _collect_sensor_data(self) -> List[BitData]:
        """Mbledh të dhëna nga sensorë"""
        # Simulim i të dhënave nga sensorët
        sensor_data = [
            BitData(
                type=BitSourceType.SENSOR_DATA,
                content={"temperature": 23.5, "humidity": 45, "pressure": 1013},
                source="environmental_sensors",
                quality_score=0.9
            )
        ]
        return sensor_data
    
    def _update_collection_metrics(self, new_bits: List[BitData]):
        """Përditëson metrikat e mbledhjes"""
        self.collection_metrics.total_bits_collected += len(new_bits)
        self.collection_metrics.last_collection_time = datetime.now()
        
        # Përditëso statistikat e burimeve
        for bit in new_bits:
            source_name = bit.source
            if source_name not in self.collection_metrics.source_statistics:
                self.collection_metrics.source_statistics[source_name] = 0
            self.collection_metrics.source_statistics[source_name] += 1
    
    async def prepare_bits_for_albi(self, batch_size: int = 1000) -> List[Dict[str, Any]]:
        """
        Përgatit bits për t'i dërguar te ALBI
        Filtron dhe optimizon të dhënat
        """
        if len(self.bit_storage) < batch_size:
            return []
        
        # Merr bits të cilësisë së mirë
        quality_bits = [
            bit for bit in self.bit_storage 
            if bit.quality_score >= self.quality_threshold and not bit.processed
        ]
        
        # Merr batch-in e parë
        selected_bits = quality_bits[:batch_size]
        
        # Shënoi si të përpunuar
        for bit in selected_bits:
            bit.processed = True
        
        # Konverto për ALBI  
        formatted_bits = []
        for bit in selected_bits:
            formatted_bits.append({
                "id": bit.id,
                "type": bit.type.value,
                "content": bit.content,
                "source": bit.source,
                "timestamp": bit.timestamp,
                "quality": bit.quality_score,
                "metadata": bit.metadata
            })
        
        return formatted_bits
    
    async def send_to_albi(self, albi_instance) -> Dict[str, Any]:
        """
        📤 PROCESI KRYESOR: Dërgon bits tek ALBI për rritje
        """
        # Përgatit batch-in e bits
        prepared_bits = await self.prepare_bits_for_albi()
        
        if not prepared_bits:
            return {
                "📭 status": "No quality bits ready for sending",
                "📊 storage_count": len(self.bit_storage),
                "⏰ timestamp": datetime.now()
            }
        
        # Dërgon tek ALBI për konsumim dhe rritje
        growth_result = await albi_instance.consume_bits(prepared_bits)
        
        # Përditëso metrikat
        self.collection_metrics.bits_sent_to_albi += len(prepared_bits)
        
        # Pastro storage-in nga bits e përpunuar
        self.bit_storage = [bit for bit in self.bit_storage if not bit.processed]
        
        return {
            "📤 bits_sent": len(prepared_bits),
            "🧠 albi_response": growth_result,
            "📊 remaining_storage": len(self.bit_storage),
            "📈 total_sent_lifetime": self.collection_metrics.bits_sent_to_albi,
            "✨ feeding_status": "Successfully nourished ALBI's intelligence!"
        }
    
    def get_collection_status(self) -> Dict[str, Any]:
        """Kthen gjendjen aktuale të mbledhjes"""
        return {
            "🔄 collection_active": self.collection_active,
            "📊 total_collected": self.collection_metrics.total_bits_collected,
            "📤 total_sent_to_albi": self.collection_metrics.bits_sent_to_albi,
            "💾 current_storage": len(self.bit_storage),
            "📈 collection_rate": self.collection_metrics.collection_rate,
            "🎯 quality_threshold": self.quality_threshold,
            "📍 source_stats": self.collection_metrics.source_statistics,
            "⏰ last_collection": self.collection_metrics.last_collection_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def stop_collection(self) -> Dict[str, Any]:
        """Ndal procesin e mbledhjes"""
        self.collection_active = False
        return {
            "🛑 status": "Collection stopped",
            "📊 final_count": self.collection_metrics.total_bits_collected,
            "⏰ stop_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# Instance globale e ALBA karakterit  
alba = ALBA_Character()


def get_alba() -> ALBA_Character:
    """Factory function për të marrë ALBA instance"""
    return alba


if __name__ == "__main__":
    # Test i shpejtë
    async def test_alba():
        print("💻 Testing ALBA Character...")
        
        # Test role definition
        role = alba.role()
        print(f"Role: {role['title']}")
        
        # Test collection start
        start_result = await alba.start_collection()
        print(f"Collection Start: {start_result}")
        
        # Prit pak kohë për mbledhje
        await asyncio.sleep(3)
        
        # Test status
        status = alba.get_collection_status()
        print(f"Status: {status}")
        
        # Test bits preparation
        prepared = await alba.prepare_bits_for_albi(10)
        print(f"Prepared bits: {len(prepared)}")
        
        # Stop collection
        stop_result = alba.stop_collection()
        print(f"Stop: {stop_result}")
    
    asyncio.run(test_alba())


