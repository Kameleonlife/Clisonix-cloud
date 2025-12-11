'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface BiofeedbackSession {
  id: string;
  timestamp: Date;
  frequency: string;
  duration: number;
  intensity: number;
  coherence: number;
  sessions_completed: number;
}

interface TrainingProgress {
  wave_type: string;
  frequency_range: string;
  sessions: number;
  avg_coherence: number;
  last_session: Date;
}

interface BiofeedbackMetrics {
  alpha_training: TrainingProgress;
  theta_training: TrainingProgress;
  beta_training: TrainingProgress;
  sessions_history: BiofeedbackSession[];
}

export default function NeuralBiofeedback() {
  const [activeTab, setActiveTab] = useState('alpha');
  const [metrics, setMetrics] = useState<BiofeedbackMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [sessionData, setSessionData] = useState<BiofeedbackSession | null>(null);

  // Load synthetic data
  useEffect(() => {
    const loadMetrics = async () => {
      try {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 500));

        // Generate synthetic data
        const now = new Date();
        const data: BiofeedbackMetrics = {
          alpha_training: {
            wave_type: 'Alpha (8-12 Hz)',
            frequency_range: '8-12 Hz',
            sessions: 47,
            avg_coherence: 78.4,
            last_session: new Date(now.getTime() - 2 * 60 * 60 * 1000),
          },
          theta_training: {
            wave_type: 'Theta (4-8 Hz)',
            frequency_range: '4-8 Hz',
            sessions: 32,
            avg_coherence: 82.1,
            last_session: new Date(now.getTime() - 5 * 60 * 60 * 1000),
          },
          beta_training: {
            wave_type: 'Beta (12-30 Hz)',
            frequency_range: '12-30 Hz',
            sessions: 25,
            avg_coherence: 71.6,
            last_session: new Date(now.getTime() - 24 * 60 * 60 * 1000),
          },
          sessions_history: [
            {
              id: '1',
              timestamp: new Date(now.getTime() - 2 * 60 * 60 * 1000),
              frequency: 'Alpha (10 Hz)',
              duration: 45,
              intensity: 85,
              coherence: 79,
              sessions_completed: 47,
            },
            {
              id: '2',
              timestamp: new Date(now.getTime() - 24 * 60 * 60 * 1000),
              frequency: 'Theta (6 Hz)',
              duration: 60,
              intensity: 92,
              coherence: 84,
              sessions_completed: 32,
            },
            {
              id: '3',
              timestamp: new Date(now.getTime() - 48 * 60 * 60 * 1000),
              frequency: 'Beta (20 Hz)',
              duration: 35,
              intensity: 78,
              coherence: 72,
              sessions_completed: 25,
            },
            {
              id: '4',
              timestamp: new Date(now.getTime() - 72 * 60 * 60 * 1000),
              frequency: 'Alpha (9 Hz)',
              duration: 50,
              intensity: 88,
              coherence: 77,
              sessions_completed: 46,
            },
            {
              id: '5',
              timestamp: new Date(now.getTime() - 96 * 60 * 60 * 1000),
              frequency: 'Theta (5 Hz)',
              duration: 55,
              intensity: 90,
              coherence: 81,
              sessions_completed: 31,
            },
          ],
        };

        setMetrics(data);
        setSessionData(data.sessions_history[0]);
      } catch (error) {
        console.error('Error loading biofeedback metrics:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadMetrics();
  }, []);

  const getTabConfig = () => {
    if (!metrics) return null;
    
    const configs = {
      alpha: {
        title: 'Alpha Training',
        emoji: '🌊',
        description: 'Relaxation & calm focus',
        color: 'cyan',
        data: metrics.alpha_training,
      },
      theta: {
        title: 'Theta Training',
        emoji: '🧠',
        description: 'Deep meditation states',
        color: 'violet',
        data: metrics.theta_training,
      },
      beta: {
        title: 'Beta Training',
        emoji: '⚡',
        description: 'Focus & concentration',
        color: 'amber',
        data: metrics.beta_training,
      },
    };

    return (configs as any)[activeTab] || configs.alpha;
  };

  const config = getTabConfig();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4 animate-pulse">🧠</div>
          <h2 className="text-3xl font-bold mb-2">Loading Neural Biofeedback</h2>
          <p className="text-gray-300">Initializing brainwave sensors...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4 text-teal-400 hover:text-teal-300 transition-colors">
            ← Back to Clisonix Cloud
          </Link>
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center">
            🧘 Neural Biofeedback Training
            <span className="ml-3 w-4 h-4 bg-teal-400 rounded-full animate-pulse"></span>
          </h1>
          <p className="text-xl text-blue-300 mb-2">
            Real-time Brainwave Optimization • EEG-Guided Training
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 mb-8">
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <button
              onClick={() => setActiveTab('alpha')}
              className={`flex-1 p-4 rounded-lg transition-all border ${
                activeTab === 'alpha'
                  ? 'bg-cyan-500/30 border-cyan-400 text-white'
                  : 'bg-white/5 border-white/20 text-gray-300 hover:bg-white/10'
              }`}
            >
              <div className="text-3xl mb-2">🌊</div>
              <div className="font-semibold">Alpha Training</div>
              <div className="text-sm">Relaxation & calm focus</div>
            </button>
            <button
              onClick={() => setActiveTab('theta')}
              className={`flex-1 p-4 rounded-lg transition-all border ${
                activeTab === 'theta'
                  ? 'bg-violet-500/30 border-violet-400 text-white'
                  : 'bg-white/5 border-white/20 text-gray-300 hover:bg-white/10'
              }`}
            >
              <div className="text-3xl mb-2">🧠</div>
              <div className="font-semibold">Theta Training</div>
              <div className="text-sm">Deep meditation states</div>
            </button>
            <button
              onClick={() => setActiveTab('beta')}
              className={`flex-1 p-4 rounded-lg transition-all border ${
                activeTab === 'beta'
                  ? 'bg-amber-500/30 border-amber-400 text-white'
                  : 'bg-white/5 border-white/20 text-gray-300 hover:bg-white/10'
              }`}
            >
              <div className="text-3xl mb-2">⚡</div>
              <div className="font-semibold">Beta Training</div>
              <div className="text-sm">Focus & concentration</div>
            </button>
          </div>

          {/* Tab Content */}
          {config && (
            <div className="space-y-6">
              {/* Training Stats */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                  <div className="text-sm text-gray-400 mb-2">Wave Type</div>
                  <div className="text-2xl font-bold text-white">{config.data.wave_type}</div>
                </div>
                <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                  <div className="text-sm text-gray-400 mb-2">Sessions</div>
                  <div className="text-2xl font-bold text-white">{config.data.sessions}</div>
                </div>
                <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                  <div className="text-sm text-gray-400 mb-2">Avg Coherence</div>
                  <div className="text-2xl font-bold text-teal-400">{config.data.avg_coherence.toFixed(1)}%</div>
                </div>
                <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                  <div className="text-sm text-gray-400 mb-2">Last Session</div>
                  <div className="text-xl font-bold text-white">{config.data.last_session.toLocaleTimeString()}</div>
                </div>
              </div>

              {/* Real-time Visualization */}
              <div className="bg-white/5 rounded-lg p-6 border border-white/20">
                <h3 className="text-lg font-semibold text-white mb-4">{config.emoji} Live Training Data</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-400">Brain Coherence</span>
                      <span className="text-teal-400 font-semibold">{config.data.avg_coherence.toFixed(1)}%</span>
                    </div>
                    <div className="bg-black/30 rounded-full h-3 overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-teal-500 to-cyan-500 transition-all duration-300"
                        style={{ width: `${config.data.avg_coherence}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-400">Training Intensity</span>
                      <span className="text-amber-400 font-semibold">{Math.floor(Math.random() * 20 + 80)}%</span>
                    </div>
                    <div className="bg-black/30 rounded-full h-3 overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-amber-500 to-orange-500 transition-all duration-300"
                        style={{ width: `${Math.floor(Math.random() * 20 + 80)}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-400">Neural Synchronization</span>
                      <span className="text-violet-400 font-semibold">{Math.floor(Math.random() * 15 + 75)}%</span>
                    </div>
                    <div className="bg-black/30 rounded-full h-3 overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-violet-500 to-indigo-500 transition-all duration-300"
                        style={{ width: `${Math.floor(Math.random() * 15 + 75)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Session Controls */}
              <div className="grid grid-cols-2 gap-4">
                <button className="bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-700 hover:to-cyan-700 text-white font-semibold py-3 rounded-lg transition-all">
                  ▶️ Start Training
                </button>
                <button className="bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white font-semibold py-3 rounded-lg transition-all">
                  ⏹️ Stop Session
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Recent Sessions */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
          <h3 className="text-lg font-semibold text-white mb-4">📊 Recent Sessions</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {metrics?.sessions_history.map((session) => (
              <div key={session.id} className="bg-black/20 rounded-lg p-4 border border-white/10 hover:border-teal-500/50 transition-all">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="text-white font-semibold">{session.frequency}</div>
                    <div className="text-gray-400 text-sm">
                      {session.timestamp.toLocaleTimeString()} • Duration: {session.duration} min • Coherence: {session.coherence}%
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-teal-400">{session.intensity}%</div>
                    <div className="text-xs text-gray-400">Intensity</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
