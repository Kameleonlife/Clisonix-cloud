/**
 * ALBI - EEG Analysis Module
 * Neural Frequency Laboratory Director - EEG Processing & Brain Signal Analysis
 * REAL DATA ONLY - No mock or simulated data
 */

"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface AlbiMetrics {
  success: boolean
  service: string
  role: string
  data: {
    operational: boolean
    health: number
    metrics: {
      goroutines: number
      neural_patterns: number
      processing_efficiency: number
      gc_operations: number
    }
    timestamp: string
  }
}

export default function EEGAnalysisPage() {
  const [albiMetrics, setAlbiMetrics] = useState<AlbiMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Fetch REAL ALBI metrics from backend
    const fetchAlbiMetrics = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch('/api/albi/metrics', {
          cache: 'no-store',
        })

        if (!response.ok) {
          throw new Error(`Failed to fetch ALBI metrics: ${response.status}`)
        }

        const data = await response.json()
        setAlbiMetrics(data)
      } catch (err) {
        console.error('ALBI metrics fetch error:', err)
        setError(String(err))
      } finally {
        setLoading(false)
      }
    }

    fetchAlbiMetrics()
    // Refresh every 5 seconds for real-time data
    const interval = setInterval(fetchAlbiMetrics, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading && !albiMetrics) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="text-2xl text-cyan-400 mb-4">⏳ Loading REAL ALBI metrics...</div>
            <div className="text-gray-400">Connecting to backend service</div>
          </div>
        </div>
      </div>
    )
  }

  if (error && !albiMetrics) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-center h-96">
          <div className="text-center bg-red-500/10 rounded-lg p-8 border border-red-500/20">
            <div className="text-2xl text-red-400 mb-4">❌ Connection Error</div>
            <div className="text-gray-300">{error}</div>
            <div className="text-sm text-gray-400 mt-4">Backend service unavailable</div>
          </div>
        </div>
      </div>
    )
  }

  const metrics = albiMetrics?.data.metrics

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2 flex items-center">
            🧠 ALBI - EEG Analysis
          </h1>
          <p className="text-gray-300">{albiMetrics?.role}</p>
          <div className="text-sm text-gray-400 mt-1">
            Specialty: EEG Processing & Brain Signal Analysis
          </div>
        </div>
        <div className="text-right">
          <div className={`text-lg font-semibold ${albiMetrics?.data.operational ? 'text-green-400' : 'text-red-400'}`}>
            {albiMetrics?.data.operational ? 'OPERATIONAL' : 'OFFLINE'}
          </div>
          <div className="text-sm text-gray-400">
            Health: {((albiMetrics?.data.health || 0) * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex space-x-2 text-sm">
        <Link href="/modules" className="text-cyan-400 hover:text-cyan-300">
          Modules
        </Link>
        <span className="text-gray-500">/</span>
        <span className="text-white">EEG Analysis</span>
      </div>

      {/* Real-time EEG Data */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Primary Metrics */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
          <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
            <span className="w-3 h-3 bg-green-500 rounded-full mr-3 animate-pulse"></span>
            Live System Metrics
          </h3>
          
          <div className="space-y-4">
            <div className="bg-black/30 rounded-lg p-4">
              <div className="text-sm text-gray-400 mb-1">Neural Patterns Detected</div>
              <div className="text-3xl font-bold text-cyan-400">
                {metrics?.neural_patterns || 0}
              </div>
              <div className="text-xs text-gray-500 mt-2">Real-time pattern count from ALBI</div>
            </div>

            <div className="bg-black/30 rounded-lg p-4">
              <div className="text-sm text-gray-400 mb-1">Active Goroutines</div>
              <div className="text-3xl font-bold text-blue-400">
                {metrics?.goroutines || 0}
              </div>
              <div className="text-xs text-gray-500 mt-2">Concurrent processing threads</div>
            </div>
          </div>
        </div>

        {/* Processing Stats */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
          <h3 className="text-xl font-semibold text-white mb-4">
            Processing Efficiency
          </h3>
          
          <div className="space-y-4">
            <div className="bg-black/30 rounded-lg p-4">
              <div className="text-sm text-gray-400 mb-1">Processing Efficiency</div>
              <div className="text-3xl font-bold text-yellow-400">
                {((metrics?.processing_efficiency || 0) * 100).toFixed(1)}%
              </div>
              <div className="text-xs text-gray-500 mt-2">Current processing rate</div>
            </div>

            <div className="bg-black/30 rounded-lg p-4">
              <div className="text-sm text-gray-400 mb-1">GC Operations</div>
              <div className="text-3xl font-bold text-purple-400">
                {metrics?.gc_operations || 0}
              </div>
              <div className="text-xs text-gray-500 mt-2">Memory garbage collection cycles</div>
            </div>
          </div>
        </div>
      </div>

      {/* ALBI Statistics */}
      <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
        <h3 className="text-xl font-semibold text-white mb-4">
          🤖 ALBI Performance Dashboard
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-black/30 rounded-lg p-4 text-center border-l-4 border-l-cyan-500">
            <div className="text-2xl font-bold text-cyan-400">
              {metrics?.neural_patterns || 0}
            </div>
            <div className="text-sm text-gray-400 mt-2">Neural Patterns</div>
            <div className="text-xs text-gray-500 mt-1">Learned & Detected</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4 text-center border-l-4 border-l-blue-500">
            <div className="text-2xl font-bold text-blue-400">
              {metrics?.goroutines || 0}
            </div>
            <div className="text-sm text-gray-400 mt-2">Active Goroutines</div>
            <div className="text-xs text-gray-500 mt-1">Concurrent Threads</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4 text-center border-l-4 border-l-yellow-500">
            <div className="text-lg font-bold text-yellow-400">
              {((metrics?.processing_efficiency || 0) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400 mt-2">Efficiency</div>
            <div className="text-xs text-gray-500 mt-1">Processing Rate</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4 text-center border-l-4 border-l-green-500">
            <div className="text-lg font-bold text-green-400">
              {((albiMetrics?.data.health || 0) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400 mt-2">Health</div>
            <div className="text-xs text-gray-500 mt-1">System Status</div>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
        <h3 className="text-xl font-semibold text-white mb-4">
          System Information
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-2">Service</div>
            <div className="text-lg text-white font-mono">{albiMetrics?.service || 'ALBI'}</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-2">Role</div>
            <div className="text-lg text-white font-mono">{albiMetrics?.role || 'Neural Processor'}</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-2">Last Update</div>
            <div className="text-lg text-white font-mono">
              {new Date(albiMetrics?.data.timestamp || '').toLocaleTimeString()}
            </div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-2">Status</div>
            <div className={`text-lg font-mono ${albiMetrics?.data.operational ? 'text-green-400' : 'text-red-400'}`}>
              {albiMetrics?.data.operational ? '✓ ONLINE' : '✗ OFFLINE'}
            </div>
          </div>
        </div>
      </div>

      {/* Data Source Notice */}
      <div className="bg-cyan-500/10 rounded-xl p-4 border border-cyan-500/20">
        <div className="flex items-start space-x-3">
          <div className="text-2xl">📡</div>
          <div>
            <h4 className="text-cyan-400 font-semibold">Real-Time Data Feed</h4>
            <p className="text-sm text-gray-300 mt-1">
              All data displayed is REAL and fetched live from the Prometheus-backed ALBI service running on the backend. 
              This page updates every 5 seconds with actual system metrics - no simulated or mock data.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

