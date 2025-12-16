"""
Ultra-Industrial Config Sync Test
Author: Ledjan Ahmati
"""

import unittest
import logging
import json
from API_CONFIG import API_CONFIG

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('UltraIndustrialConfigSync')

class TestConfigSync(unittest.TestCase):
    def test_sync_core_parameters(self):
        """Testo sinkronizimin e parametrave kryesorë industrial midis backend dhe frontend"""
        # Lexo konfigurimin industrial nga frontend
        with open('frontend/industrial.config.json', 'r', encoding='utf-8') as f:
            frontend_config = json.load(f)
        # Audit
        self.assertTrue(API_CONFIG['audit']['enabled'])
        self.assertTrue(frontend_config['industrialLogging']['enabled'])
        # Tracing
        self.assertTrue(API_CONFIG['tracing']['enabled'])
        self.assertIn('trace', frontend_config['industrialLogging']['logLevels'])
        # Compliance
        self.assertTrue(API_CONFIG['compliance']['reports'])
        self.assertTrue(frontend_config['slaMonitoring']['enabled'])
        # Metrics
        self.assertTrue(API_CONFIG['metrics']['enabled'])
        self.assertTrue(frontend_config['industrialAnalytics']['enabled'])
        # Security
        self.assertTrue(API_CONFIG['security']['backup']['enabled'])
        self.assertTrue(frontend_config['secretsManagement']['enabled'])
        # User Management
        self.assertTrue(API_CONFIG['user_management']['audit_trail'])
        self.assertIn('admin', API_CONFIG['user_management']['roles'])
        # Data Export/Import
        self.assertTrue(API_CONFIG['data']['export_import'])
        self.assertIn('method', frontend_config['autoSynchronization'])
        # Alerting
        self.assertTrue(API_CONFIG['alerting']['enabled'])
        self.assertTrue(frontend_config['industrialAnalytics']['enabled'])
        # Documentation
        self.assertTrue(API_CONFIG['documentation']['api'])
        self.assertIn('location', frontend_config['onboardingDocs'])
        # CI/CD
        self.assertTrue(API_CONFIG['ci_cd']['enabled'])
        self.assertTrue(frontend_config['codeReview']['enabled'])
        logger.info('Konfigurimi industrial backend/frontend është i sinkronizuar.')

if __name__ == '__main__':
    unittest.main()

