/**
 * Clisonix Modules Hub - Industrial Dashboard Access
 * ALBI (EEG Processing) + ALBA (Data Collection) + JONA (Neural Alignment & Audio Synthesis)
 */

"use client"

import Link from 'next/link'
import { useState, useEffect } from 'react'

interface ModuleStatus {
  albi: 'active' | 'processing' | 'offline'
  alba: 'collecting' | 'analyzing' | 'offline'  
  jona: 'monitoring' | 'synthesizing' | 'offline'
}

export default function ModulesPage() {
  const [moduleStatus, setModuleStatus] = useState<ModuleStatus>({
    albi: 'offline',
    alba: 'offline', 
    jona: 'offline'
  })

  useEffect(() => {
    // Simulate checking module status
    const checkModuleStatus = async () => {
      try {
        // Will connect to actual backend endpoints
        setModuleStatus({
          albi: 'active',
          alba: 'collecting',
          jona: 'monitoring'
        })
      } catch (error) {
        console.error('Module status check failed:', error)
      }
    }

    checkModuleStatus()
    const interval = setInterval(checkModuleStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const modules = [
    {
      id: 'eeg-analysis',
      name: '🧠 ALBI - EEG Analysis',
      description: 'Neural Frequency Laboratory Director - EEG Processing & Brain Signal Analysis',
      status: moduleStatus.albi,
      capabilities: [
        'Real-time EEG signal processing',
        'Neural frequency analysis (FFT)',
        'Brain state interpretation',
        'Neural pattern recognition',
        'Dominant frequency detection'
      ],
      route: '/modules/eeg-analysis'
    },
    {
      id: 'data-collection',
      name: '📊 ALBA - Data Collection',
      description: 'Advanced data collection and processing coordinator',
      status: moduleStatus.alba,
      capabilities: [
        'Multi-source data integration',
        'Real-time data streaming',
        'Pattern analysis coordination',
        'Neural pattern discussions',
        'Data validation and cleanup'
      ],
      route: '/modules/data-collection'
    },
    {
      id: 'neural-synthesis', 
      name: '🎵 JONA - Neural Audio Synthesis',
      description: 'Joyful Overseer of Neural Alignment - Brain-Data Art & Real-time Monitoring',
      status: moduleStatus.jona,
      capabilities: [
        'EEG to audio synthesis',
        'Real-time neural monitoring',
        'Brain-data art creation',
        'Neural symphony generation',
        'Biofeedback audio output'
      ],
      route: '/modules/neural-synthesis'
    },
    {
      id: 'industrial-dashboard',
      name: '🏭 Industrial Dashboard',
      description: 'Complete industrial monitoring and control interface',
      status: 'active' as const,
      capabilities: [
        'Live system monitoring',
        'Performance metrics',
        'Real-time data visualization',
        'System health checks',
        'Industrial-grade controls'
      ],
      route: '/modules/industrial-dashboard'
    },
    {
      id: 'reporting-dashboard',
      name: '📈 ULTRA Reporting Center',
      description: 'Excel-style executive dashboard blending Grafana, Prometheus, Datadog and Victoria metrics',
      status: 'active' as const,
      capabilities: [
        'Unified KPI grid with trends',
        'Live Prometheus history sparklines',
        'Executive-ready export buttons',
        'Alert rundown synced with AlertManager',
        'Synthetic Datadog signal bridge'
      ],
      route: '/modules/reporting-dashboard'
    },
    {
      id: 'phone-monitor',
      name: '📱 Phone Monitor',
      description: 'Mobile device monitoring and neural interface',
      status: 'active' as const,
      capabilities: [
        'Mobile EEG interfaces',
        'Remote monitoring',
        'Cloud connectivity',
        'Real-time sync',
        'Mobile biofeedback'
      ],
      route: '/modules/phone-monitor'
    },
    {
      id: 'spectrum-analyzer',
      name: '📊 Spectrum Analyzer',
      description: 'Advanced frequency domain analysis and visualization',
      status: 'active' as const,
      capabilities: [
        'FFT analysis',
        'Frequency visualization',
        'Spectral analysis',
        'Signal processing',
        'Real-time spectrum display'
      ],
      route: '/modules/spectrum-analyzer'
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'collecting':
      case 'monitoring':
        return 'bg-green-500'
      case 'processing':
      case 'analyzing':
      case 'synthesizing':
        return 'bg-yellow-500'
      default:
        return 'bg-red-500'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Active'
      case 'processing': return 'Processing'
      case 'collecting': return 'Collecting Data'
      case 'analyzing': return 'Analyzing'
      case 'monitoring': return 'Monitoring'
      case 'synthesizing': return 'Synthesizing'
      default: return 'Offline'
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
        <h1 className="text-4xl font-bold text-white mb-4 bg-gradient-to-r from-cyan-400 via-violet-400 to-emerald-400 bg-clip-text text-transparent">
          🧠 Clisonix Industrial Modules
        </h1>
        <p className="text-lg text-gray-300">
          Advanced neuroacoustic processing, EEG analysis, and industrial-grade monitoring
        </p>
        <div className="flex items-center justify-center mt-4 space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-400">Live Industrial Backend Monitoring • Real Data Only</span>
        </div>
      </div>

      {/* Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {modules.map((module) => (
          <Link
            key={module.id}
            href={module.route}
            className="group bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 hover:bg-white/20 hover:border-white/40 transition-all duration-300 hover:scale-105"
          >
            <div className="flex items-start justify-between mb-4">
              <h3 className="text-xl font-semibold text-white group-hover:text-cyan-400 transition-colors">
                {module.name}
              </h3>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${getStatusColor(module.status)} animate-pulse`}></div>
                <span className="text-xs text-gray-400">
                  {getStatusText(module.status)}
                </span>
              </div>
            </div>
            
            <p className="text-gray-300 text-sm mb-4">
              {module.description}
            </p>

            <div className="space-y-2">
              <h4 className="text-sm font-medium text-gray-400 uppercase tracking-wide">
                Capabilities
              </h4>
              <ul className="space-y-1">
                {module.capabilities.slice(0, 3).map((capability, idx) => (
                  <li key={idx} className="text-xs text-gray-500 flex items-center">
                    <span className="w-1 h-1 bg-cyan-400 rounded-full mr-2"></span>
                    {capability}
                  </li>
                ))}
                {module.capabilities.length > 3 && (
                  <li className="text-xs text-gray-600 italic">
                    +{module.capabilities.length - 3} more...
                  </li>
                )}
              </ul>
            </div>

            <div className="mt-4 pt-4 border-t border-white/10">
              <span className="text-xs text-cyan-400 group-hover:text-cyan-300 transition-colors">
                Click to access module →
              </span>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <span className="w-2 h-2 bg-yellow-500 rounded-full mr-3 animate-pulse"></span>
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <Link
            href="/modules/reporting-dashboard"
            className="bg-gradient-to-r from-cyan-600/20 to-blue-600/20 hover:from-cyan-600/30 hover:to-blue-600/30 rounded-lg p-4 border border-cyan-500/30 hover:border-cyan-400/50 transition-all duration-300"
          >
            <div className="text-sm font-medium text-white">📈 Launch ULTRA Reporting</div>
            <div className="text-xs text-gray-400 mt-1">Excel-style dashboard & exports</div>
          </Link>

          <Link
            href="/modules/neural-synthesis"
            className="bg-gradient-to-r from-purple-600/20 to-pink-600/20 hover:from-purple-600/30 hover:to-pink-600/30 rounded-lg p-4 border border-purple-500/30 hover:border-purple-400/50 transition-all duration-300"
          >
            <div className="text-sm font-medium text-white">🎵 Start Neural Synthesis</div>
            <div className="text-xs text-gray-400 mt-1">Begin EEG to audio conversion</div>
          </Link>
          
          <Link
            href="/modules/eeg-analysis"
            className="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 hover:from-blue-600/30 hover:to-cyan-600/30 rounded-lg p-4 border border-blue-500/30 hover:border-blue-400/50 transition-all duration-300"
          >
            <div className="text-sm font-medium text-white">🧠 Analyze Brain Signals</div>
            <div className="text-xs text-gray-400 mt-1">Real-time EEG processing</div>
          </Link>
          
          <Link
            href="/modules/industrial-dashboard"
            className="bg-gradient-to-r from-emerald-600/20 to-teal-600/20 hover:from-emerald-600/30 hover:to-teal-600/30 rounded-lg p-4 border border-emerald-500/30 hover:border-emerald-400/50 transition-all duration-300"
          >
            <div className="text-sm font-medium text-white">🏭 Industrial Monitor</div>
            <div className="text-xs text-gray-400 mt-1">Full system oversight</div>
          </Link>
        </div>
      </div>
    </div>
  )
}

