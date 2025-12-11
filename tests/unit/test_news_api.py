"""
Ultra-Industrial Infinite Information Source & Fast Intelligence API Test
Author: Ledjan Ahmati
"""

import unittest
import logging
import json
import random
from API_CONFIG import API_CONFIG

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('UltraIndustrialNewsAPI')

class InfiniteInfoSource:
    """Simulon burim informacioni pa fund (news, data, signals)"""
    def __init__(self):
        self.topics = ['ai', 'industry', 'health', 'energy', 'finance', 'security', 'iot', 'cloud', 'robotics', 'quantum']
    def stream(self, n=100):
        for _ in range(n):
            topic = random.choice(self.topics)
            yield {
                'topic': topic,
                'timestamp': '2025-10-12T12:00:00Z',
                'payload': {
                    'headline': f'Ultra-{topic}-update',
                    'data': random.random(),
                    'meta': {'source': 'nanogrid-nrg', 'format': 'json'}
                }
            }

class FastIntelligenceAPI:
    """Simulon API të shpejtë inteligjence, output CBOR/JSON/Nanogrid NRG"""
    def __init__(self, format='json'):
        self.format = format
    def get_signal(self, info):
        # Krijo sinjal të ri nga informacioni
        signal = {
            'nrg_id': f'nrg-{random.randint(1000,9999)}',
            'topic': info['topic'],
            'value': info['payload']['data'],
            'meta': info['payload']['meta'],
            'timestamp': info['timestamp']
        }
        if self.format == 'json':
            return json.dumps(signal)
        elif self.format == 'cbor':
            try:
                import cbor2
                return cbor2.dumps(signal)
            except ImportError:
                logger.warning('CBOR2 library not installed, returning JSON')
                return json.dumps(signal)
        elif self.format == 'nanogrid-nrg':
            # Simulo format të veçantë industrial
            return f"NRG|{signal['nrg_id']}|{signal['topic']}|{signal['value']}|{signal['timestamp']}"
        else:
            return signal

class TestUltraIndustrialNewsAPI(unittest.TestCase):
    def test_infinite_info_stream(self):
        """Testo burimin e informacionit pa fund"""
        source = InfiniteInfoSource()
        stream = list(source.stream(10))
        logger.info('Streamed info: %s', stream)
        self.assertEqual(len(stream), 10)
        for info in stream:
            self.assertIn('topic', info)
            self.assertIn('payload', info)
            self.assertIn('timestamp', info)

    def test_fast_intelligence_api_json(self):
        """Testo Fast Intelligence API me output JSON"""
        source = InfiniteInfoSource()
        info = next(source.stream(1))
        api = FastIntelligenceAPI(format='json')
        signal = api.get_signal(info)
        logger.info('JSON signal: %s', signal)
        self.assertTrue(signal.startswith('{'))

    def test_fast_intelligence_api_cbor(self):
        """Testo Fast Intelligence API me output CBOR"""
        source = InfiniteInfoSource()
        info = next(source.stream(1))
        api = FastIntelligenceAPI(format='cbor')
        signal = api.get_signal(info)
        logger.info('CBOR signal: %s', signal)
        self.assertTrue(signal is not None)

    def test_fast_intelligence_api_nanogrid_nrg(self):
        """Testo Fast Intelligence API me format industrial nanogrid-nrg"""
        source = InfiniteInfoSource()
        info = next(source.stream(1))
        api = FastIntelligenceAPI(format='nanogrid-nrg')
        signal = api.get_signal(info)
        logger.info('Nanogrid NRG signal: %s', signal)
        self.assertTrue(signal.startswith('NRG|'))

if __name__ == '__main__':
    unittest.main()
