# -*- coding: utf-8 -*-
"""Real-time Clisonix Telemetry Analysis with Live API Integration"""

from __future__ import annotations

import json
import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClisonixTelemetryAnalyzer:
    """Real-time telemetry analysis with live API integration"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.log_file = Path(r"C:\Clisonix-cloud\logs\telemetry.jsonl")
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_live_system_metrics(self) -> Dict:
        """Get real system metrics from Clisonix API"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                health_data = await response.json()
            
            async with self.session.get(f"{self.base_url}/status") as response:
                status_data = await response.json()
            
            async with self.session.get(f"{self.base_url}/api/alba/metrics") as response:
                alba_metrics = await response.json()
                
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "health": health_data,
                "status": status_data,
                "alba_metrics": alba_metrics,
                "source": "live_api"
            }
        except Exception as e:
            logger.error(f"Failed to fetch live metrics: {e}")
            return {}
    
    async def get_real_time_performance(self) -> Dict:
        """Get real-time performance data from running services"""
        endpoints = [
            "/api/alba/status",
            "/asi/status", 
            "/api/performance-metrics",
            "/api/system-status"
        ]
        
        performance_data = {}
        for endpoint in endpoints:
            try:
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    data = await response.json()
                    performance_data[endpoint.replace('/', '_')] = {
                        "response_time_ms": response.elapsed.total_seconds() * 1000,
                        "data": data
                    }
            except Exception as e:
                logger.warning(f"Failed to fetch {endpoint}: {e}")
                
        return performance_data
    
    def load_telemetry_logs(self) -> pd.DataFrame:
        """Load and parse real telemetry data from JSONL files"""
        records: List[dict] = []
        
        if not self.log_file.exists():
            logger.warning(f"Telemetry log file not found: {self.log_file}")
            return pd.DataFrame()

        try:
            with open(self.log_file, "r", encoding="utf-8") as handle:
                for line_num, line in enumerate(handle, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        # Add parsing timestamp if not present
                        if 'timestamp' in record:
                            record['parsed_timestamp'] = datetime.fromisoformat(
                                record['timestamp'].replace('Z', '+00:00')
                            )
                        records.append(record)
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON parse error line {line_num}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Failed to read log file: {e}")
            
        return pd.DataFrame(records)
    
    def analyze_performance_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze real performance trends from telemetry data"""
        if df.empty:
            return {}
        
        analysis = {}
        
        # Convert timestamp to datetime for time series analysis
        if 'parsed_timestamp' in df.columns:
            df = df.sort_values('parsed_timestamp')
            df['hour'] = df['parsed_timestamp'].dt.floor('H')
            
            # Performance trends over time
            hourly_stats = df.groupby('hour').agg({
                'duration_ms': ['mean', 'std', 'count'],
                'success': 'mean'
            }).round(2)
            
            analysis['hourly_performance'] = hourly_stats
            
            # Detect performance anomalies
            duration_zscore = np.abs(stats.zscore(df['duration_ms'].dropna()))
            anomalies = df[duration_zscore > 3]
            analysis['performance_anomalies'] = anomalies.to_dict('records')
        
        # Function performance analysis
        function_stats = df.groupby('function').agg({
            'duration_ms': ['count', 'mean', 'std', 'min', 'max'],
            'success': 'mean',
            'input_bytes': 'mean',
            'output_bytes': 'mean'
        }).round(2)
        
        analysis['function_performance'] = function_stats
        
        # Error analysis
        if 'error' in df.columns:
            error_analysis = df[df['error'].notna()].groupby('function').agg({
                'error': 'count',
                'duration_ms': 'mean'
            }).round(2)
            analysis['error_analysis'] = error_analysis
        
        return analysis
    
    def generate_real_time_visualizations(self, df: pd.DataFrame, live_metrics: Dict):
        """Generate comprehensive visualizations with real data"""
        if df.empty and not live_metrics:
            print("No data available for visualization")
            return
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 15))
        
        if not df.empty:
            # 1. Performance trends over time
            if 'parsed_timestamp' in df.columns:
                ax1 = plt.subplot(3, 3, 1)
                hourly_avg = df.groupby(df['parsed_timestamp'].dt.floor('H'))['duration_ms'].mean()
                hourly_avg.plot(ax=ax1, title='Average Response Time Trend', color='blue')
                ax1.set_ylabel('Duration (ms)')
                ax1.grid(True)
            
            # 2. Function performance comparison
            ax2 = plt.subplot(3, 3, 2)
            function_avg = df.groupby('function')['duration_ms'].mean().sort_values()
            function_avg.plot(kind='barh', ax=ax2, title='Average Duration by Function')
            ax2.set_xlabel('Duration (ms)')
            
            # 3. Success rate analysis
            ax3 = plt.subplot(3, 3, 3)
            if 'success' in df.columns:
                success_rates = df.groupby('function')['success'].mean().sort_values()
                success_rates.plot(kind='barh', ax=ax3, title='Success Rate by Function', color='green')
                ax3.set_xlabel('Success Rate')
            
            # 4. Data throughput analysis
            ax4 = plt.subplot(3, 3, 4)
            if all(col in df.columns for col in ['input_bytes', 'output_bytes']):
                throughput = df.groupby('function').agg({
                    'input_bytes': 'mean',
                    'output_bytes': 'mean'
                })
                throughput.plot(kind='bar', ax=ax4, title='Average Data Throughput')
                ax4.set_ylabel('Bytes')
            
            # 5. Performance distribution
            ax5 = plt.subplot(3, 3, 5)
            df['duration_ms'].hist(bins=50, ax=ax5, alpha=0.7)
            ax5.set_title('Response Time Distribution')
            ax5.set_xlabel('Duration (ms)')
            ax5.set_ylabel('Frequency')
            
            # 6. Error correlation heatmap
            ax6 = plt.subplot(3, 3, 6)
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                correlation_matrix = df[numeric_cols].corr()
                sns.heatmap(correlation_matrix, annot=True, ax=ax6, cmap='coolwarm', center=0)
                ax6.set_title('Performance Metrics Correlation')
        
        # 7. Live system status
        if live_metrics:
            ax7 = plt.subplot(3, 3, 7)
            if 'health' in live_metrics and 'status' in live_metrics:
                status_data = []
                labels = []
                
                # Extract key metrics
                health = live_metrics['health']
                status = live_metrics['status']
                
                if 'system' in status and 'cpu_percent' in status['system']:
                    status_data.append(status['system']['cpu_percent'])
                    labels.append('CPU %')
                
                if 'system' in status and 'memory_percent' in status['system']:
                    status_data.append(status['system']['memory_percent'])
                    labels.append('Memory %')
                
                if status_data:
                    ax7.bar(labels, status_data, color=['red', 'blue', 'green'])
                    ax7.set_title('Live System Metrics')
                    ax7.set_ylabel('Percentage')
        
        # 8. ALBA metrics if available
        if live_metrics and 'alba_metrics' in live_metrics:
            ax8 = plt.subplot(3, 3, 8)
            alba_data = live_metrics['alba_metrics']
            if 'active_streams' in alba_data and 'total_data_points' in alba_data:
                alba_metrics = [alba_data.get('active_streams', 0), 
                              alba_data.get('total_data_points', 0) / 1000]  # Scale for visibility
                alba_labels = ['Active Streams', 'Data Points (K)']
                ax8.bar(alba_labels, alba_metrics, color=['purple', 'orange'])
                ax8.set_title('ALBA Live Metrics')
        
        plt.tight_layout()
        plt.show()
    
    def generate_performance_report(self, df: pd.DataFrame, analysis: Dict, live_metrics: Dict) -> str:
        """Generate comprehensive performance report"""
        report = []
        report.append("=" * 60)
        report.append("Clisonix REAL-TIME PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.utcnow().isoformat()}")
        report.append(f"Data Points: {len(df)}")
        report.append("")
        
        if not df.empty:
            # Summary statistics
            report.append("SUMMARY STATISTICS:")
            report.append("-" * 40)
            report.append(f"Total function calls: {len(df)}")
            report.append(f"Time range: {df['parsed_timestamp'].min()} to {df['parsed_timestamp'].max()}")
            report.append(f"Average response time: {df['duration_ms'].mean():.2f} ms")
            report.append(f"Success rate: {df['success'].mean() * 100:.1f}%" if 'success' in df.columns else "Success rate: N/A")
            report.append("")
            
            # Top performing functions
            report.append("TOP PERFORMING FUNCTIONS:")
            report.append("-" * 40)
            function_stats = df.groupby('function')['duration_ms'].agg(['count', 'mean', 'std']).round(2)
            for func, stats in function_stats.sort_values('mean').head(10).iterrows():
                report.append(f"{func}: {stats['mean']}ms (n={stats['count']})")
            report.append("")
            
            # Performance issues
            if 'performance_anomalies' in analysis and analysis['performance_anomalies']:
                report.append("PERFORMANCE ANOMALIES DETECTED:")
                report.append("-" * 40)
                for anomaly in analysis['performance_anomalies'][:5]:
                    report.append(f"{anomaly.get('function', 'Unknown')}: {anomaly.get('duration_ms', 0):.2f}ms")
                report.append("")
        
        if live_metrics:
            report.append("LIVE SYSTEM STATUS:")
            report.append("-" * 40)
            if 'health' in live_metrics:
                report.append(f"Service status: {live_metrics['health'].get('status', 'Unknown')}")
            if 'status' in live_metrics and 'system' in live_metrics['status']:
                system = live_metrics['status']['system']
                report.append(f"CPU usage: {system.get('cpu_percent', 'N/A')}%")
                report.append(f"Memory usage: {system.get('memory_percent', 'N/A')}%")
        
        return "\n".join(report)

async def main():
    """Main analysis function with real API integration"""
    print("ðŸš€ Clisonix Real-Time Telemetry Analysis")
    print("Connecting to live services...")
    
    async with ClisonixTelemetryAnalyzer() as analyzer:
        try:
            # Get live data from running services
            print("ðŸ“¡ Fetching live system metrics...")
            live_metrics = await analyzer.get_live_system_metrics()
            
            print("âš¡ Fetching real-time performance data...")
            real_time_perf = await analyzer.get_real_time_performance()
            
            # Load historical telemetry data
            print("ðŸ“Š Loading telemetry logs...")
            df = analyzer.load_telemetry_logs()
            
            if not df.empty:
                print("ðŸ” Analyzing performance trends...")
                analysis = analyzer.analyze_performance_trends(df)
                
                # Generate comprehensive report
                report = analyzer.generate_performance_report(df, analysis, live_metrics)
                print("\n" + report)
                
                # Create visualizations
                print("ðŸ“ˆ Generating visualizations...")
                analyzer.generate_real_time_visualizations(df, live_metrics)
                
            else:
                print("â„¹ï¸ No historical telemetry data found")
                
            if live_metrics:
                print("âœ… Live system metrics captured successfully")
            else:
                print("âš ï¸ Could not connect to live services")
                
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            print(f"âŒ Analysis error: {e}")

if __name__ == "__main__":
    # Run the analysis
    asyncio.run(main())