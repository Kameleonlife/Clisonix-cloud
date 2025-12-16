"""
Ultra-Industrial Import/Export Test
Author: Ledjan Ahmati
"""

import unittest
import logging
import json
from API_CONFIG import API_CONFIG

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('UltraIndustrialImportExport')

class TestImportExport(unittest.TestCase):
    def test_export_data(self):
        """Testo eksportimin e të dhënave industriale në formatet e lejuara"""
        data = {
            'id': 1,
            'name': 'Industrial Signal',
            'value': 0.98,
            'meta': {'type': 'EEG', 'source': 'sensor', 'timestamp': '2025-10-12T12:00:00Z'}
        }
        formats = API_CONFIG['data']['formats']
        for fmt in formats:
            if fmt == 'JSON':
                exported = json.dumps(data)
                logger.info('Exported JSON: %s', exported)
                self.assertTrue(exported.startswith('{'))
            elif fmt == 'CSV':
                exported = f"id,name,value,type,source,timestamp\n{data['id']},{data['name']},{data['value']},{data['meta']['type']},{data['meta']['source']},{data['meta']['timestamp']}"
                logger.info('Exported CSV: %s', exported)
                self.assertIn('Industrial Signal', exported)
            elif fmt == 'XML':
                exported = f"<signal><id>{data['id']}</id><name>{data['name']}</name><value>{data['value']}</value><type>{data['meta']['type']}</type><source>{data['meta']['source']}</source><timestamp>{data['meta']['timestamp']}</timestamp></signal>"
                logger.info('Exported XML: %s', exported)
                self.assertIn('<signal>', exported)

    def test_import_data(self):
        """Testo importimin e të dhënave industriale nga formate të ndryshme"""
        json_data = '{"id":2,"name":"Imported Signal","value":0.77,"meta":{"type":"ECG","source":"api","timestamp":"2025-10-12T13:00:00Z"}}'
        csv_data = 'id,name,value,type,source,timestamp\n2,Imported Signal,0.77,ECG,api,2025-10-12T13:00:00Z'
        xml_data = '<signal><id>2</id><name>Imported Signal</name><value>0.77</value><type>ECG</type><source>api</source><timestamp>2025-10-12T13:00:00Z</timestamp></signal>'
        # Import JSON
        imported_json = json.loads(json_data)
        logger.info('Imported JSON: %s', imported_json)
        self.assertEqual(imported_json['name'], 'Imported Signal')
        # Import CSV
        csv_parts = csv_data.split('\n')[1].split(',')
        imported_csv = {
            'id': int(csv_parts[0]),
            'name': csv_parts[1],
            'value': float(csv_parts[2]),
            'meta': {
                'type': csv_parts[3],
                'source': csv_parts[4],
                'timestamp': csv_parts[5]
            }
        }
        logger.info('Imported CSV: %s', imported_csv)
        self.assertEqual(imported_csv['meta']['type'], 'ECG')
        # Import XML (simple parse)
        def extract(tag, xml):
            start = xml.find(f'<{tag}>') + len(tag) + 2
            end = xml.find(f'</{tag}>')
            return xml[start:end]
        imported_xml = {
            'id': int(extract('id', xml_data)),
            'name': extract('name', xml_data),
            'value': float(extract('value', xml_data)),
            'meta': {
                'type': extract('type', xml_data),
                'source': extract('source', xml_data),
                'timestamp': extract('timestamp', xml_data)
            }
        }
        logger.info('Imported XML: %s', imported_xml)
        self.assertEqual(imported_xml['meta']['source'], 'api')

if __name__ == '__main__':
    unittest.main()

