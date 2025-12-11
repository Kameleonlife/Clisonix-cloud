'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Heart, Zap, TrendingUp, Award, Users, Target, Flame } from 'lucide-react';

interface UserProfile {
  id: string;
  name: string;
  age: number;
  level: string;
  totalWorkouts: number;
  streakDays: number;
}

interface BiometricReading {
  heartRate: number;
  calories: number;
  stress: number;
  emotion: string;
}

interface Exercise {
  id: string;
  name: string;
  duration: number;
  calories: number;
  formScore: number;
  feedback: string;
}

export default function FitnessDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [biometrics, setBiometrics] = useState<BiometricReading>({
    heartRate: 72,
    calories: 245,
    stress: 35,
    emotion: 'focused',
  });
  const exercises: Exercise[] = [
    {
      id: '1',
      name: 'Push-ups',
      duration: 10,
      calories: 45,
      formScore: 92,
      feedback: 'Great form! Keep your core engaged.',
    },
    {
      id: '2',
      name: 'Squats',
      duration: 15,
      calories: 65,
      formScore: 88,
      feedback: 'Lower deeper for better activation.',
    },
  ];

  useEffect(() => {
    // Simulate API call to fetch user profile
    setUserProfile({
      id: 'user-001',
      name: 'Arben',
      age: 28,
      level: 'Intermediate',
      totalWorkouts: 42,
      streakDays: 7,
    });

    // Simulate real-time biometric updates
    const interval = setInterval(() => {
      setBiometrics((prev) => ({
        ...prev,
        heartRate: Math.floor(Math.random() * (100 - 60) + 60),
        calories: prev.calories + Math.floor(Math.random() * 10),
        stress: Math.max(0, prev.stress - Math.floor(Math.random() * 5)),
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'workouts', label: 'Workouts', icon: Flame },
    { id: 'nutrition', label: 'Nutrition', icon: Target },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'achievements', label: 'Achievements', icon: Award },
    { id: 'social', label: 'Social', icon: Users },
  ];

  const emotionColors: Record<string, string> = {
    energized: 'bg-green-500',
    focused: 'bg-blue-500',
    calm: 'bg-purple-500',
    anxious: 'bg-orange-500',
    tired: 'bg-gray-500',
  };

  const stressLevel = biometrics.stress < 30 ? 'Low' : biometrics.stress < 60 ? 'Moderate' : 'High';
  const stressColor = biometrics.stress < 30 ? 'text-green-400' : biometrics.stress < 60 ? 'text-yellow-400' : 'text-red-400';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 text-white">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-slate-700/50 backdrop-blur-xl bg-slate-950/80">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Fitness Hub</h1>
              <p className="text-xs text-slate-400">Neural-Powered Training</p>
            </div>
          </div>
          {userProfile && (
            <div className="text-right">
              <p className="font-medium">{userProfile.name}</p>
              <p className="text-sm text-slate-400">{userProfile.level}</p>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Biometric Cards Row */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Heart Rate Card */}
          <motion.div
            className="bg-gradient-to-br from-red-900/40 to-red-950/40 border border-red-500/30 rounded-2xl p-6 hover:border-red-500/60 transition-colors"
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-sm font-medium text-slate-300">Heart Rate</h3>
              <Heart className="w-5 h-5 text-red-400" />
            </div>
            <p className="text-3xl font-bold mb-2">{biometrics.heartRate}</p>
            <p className="text-xs text-slate-400">bpm • Normal range</p>
          </motion.div>

          {/* Calories Card */}
          <motion.div
            className="bg-gradient-to-br from-orange-900/40 to-orange-950/40 border border-orange-500/30 rounded-2xl p-6 hover:border-orange-500/60 transition-colors"
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-sm font-medium text-slate-300">Calories Burned</h3>
              <Flame className="w-5 h-5 text-orange-400" />
            </div>
            <p className="text-3xl font-bold mb-2">{biometrics.calories}</p>
            <p className="text-xs text-slate-400">kcal • Today</p>
          </motion.div>

          {/* Stress Level Card */}
          <motion.div
            className="bg-gradient-to-br from-purple-900/40 to-purple-950/40 border border-purple-500/30 rounded-2xl p-6 hover:border-purple-500/60 transition-colors"
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-sm font-medium text-slate-300">Stress Level</h3>
              <Zap className="w-5 h-5 text-purple-400" />
            </div>
            <p className={`text-3xl font-bold mb-2 ${stressColor}`}>{biometrics.stress}</p>
            <p className={`text-xs ${stressColor}`}>{stressLevel}</p>
          </motion.div>

          {/* Emotion Card */}
          <motion.div
            className="bg-gradient-to-br from-cyan-900/40 to-cyan-950/40 border border-cyan-500/30 rounded-2xl p-6 hover:border-cyan-500/60 transition-colors"
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-sm font-medium text-slate-300">Emotion</h3>
              <span className={`w-3 h-3 rounded-full ${emotionColors[biometrics.emotion] || 'bg-slate-500'}`} />
            </div>
            <p className="text-xl font-bold capitalize mb-2">{biometrics.emotion}</p>
            <p className="text-xs text-slate-400">Real-time detection</p>
          </motion.div>
        </motion.div>

        {/* Tabs Navigation */}
        <div className="mb-8 border-b border-slate-700/50">
          <div className="flex gap-2 overflow-x-auto pb-4">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <motion.button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600/40 text-blue-300 border border-blue-500/50'
                      : 'text-slate-400 hover:text-slate-300'
                  }`}
                  whileHover={{ scale: 1.05 }}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </motion.button>
              );
            })}
          </div>
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'overview' && (
            <motion.div
              key="overview"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              {/* User Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                  <p className="text-slate-400 text-sm mb-2">Total Workouts</p>
                  <p className="text-2xl font-bold">{userProfile?.totalWorkouts || 0}</p>
                </div>
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                  <p className="text-slate-400 text-sm mb-2">Current Streak</p>
                  <p className="text-2xl font-bold text-green-400">{userProfile?.streakDays || 0} days</p>
                </div>
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                  <p className="text-slate-400 text-sm mb-2">Personal Best</p>
                  <p className="text-2xl font-bold text-cyan-400">92%</p>
                </div>
              </div>

              {/* AI Coaching */}
              <div className="bg-gradient-to-br from-slate-800/40 to-blue-900/20 border border-slate-700/50 rounded-2xl p-8">
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
                    <Zap className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold mb-2">AI Coaching Analysis</h3>
                    <p className="text-slate-300 mb-4">
                      Your last workout showed excellent form on squats! Keep maintaining that depth and remember to breathe steadily.
                      Try adding 5 more reps next session.
                    </p>
                    <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors">
                      View Detailed Analysis
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'workouts' && (
            <motion.div
              key="workouts"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-4"
            >
              {exercises.map((exercise, idx) => (
                <motion.div
                  key={exercise.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6 hover:border-slate-600/50 transition-colors"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h4 className="font-semibold text-lg">{exercise.name}</h4>
                      <p className="text-slate-400 text-sm">{exercise.duration} min • {exercise.calories} kcal</p>
                    </div>
                    <span className="px-3 py-1 bg-green-900/40 border border-green-500/30 rounded-lg text-green-300 text-sm font-medium">
                      {exercise.formScore}% Form
                    </span>
                  </div>
                  <p className="text-slate-300 text-sm">{exercise.feedback}</p>
                </motion.div>
              ))}
            </motion.div>
          )}

          {activeTab === 'nutrition' && (
            <motion.div
              key="nutrition"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Macros Today</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-slate-300">Protein</span>
                      <span className="text-sm font-medium">145g / 150g</span>
                    </div>
                    <div className="w-full bg-slate-700/50 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{ width: '97%' }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-slate-300">Carbs</span>
                      <span className="text-sm font-medium">180g / 250g</span>
                    </div>
                    <div className="w-full bg-slate-700/50 rounded-full h-2">
                      <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '72%' }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-slate-300">Fats</span>
                      <span className="text-sm font-medium">45g / 60g</span>
                    </div>
                    <div className="w-full bg-slate-700/50 rounded-full h-2">
                      <div className="bg-orange-500 h-2 rounded-full" style={{ width: '75%' }} />
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Meal Recommendations</h3>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li>🥗 Greek yogurt with berries</li>
                  <li>🍗 Grilled chicken breast with quinoa</li>
                  <li>🥑 Avocado toast on whole grain bread</li>
                  <li>🥤 Protein shake with banana</li>
                </ul>
              </div>
            </motion.div>
          )}

          {activeTab === 'analytics' && (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Weekly Progress</h3>
                <div className="flex items-end gap-2 h-32">
                  {[45, 60, 55, 75, 70, 85, 90].map((val, i) => (
                    <div key={i} className="flex-1 bg-blue-600/40 rounded-t h-full" style={{ height: `${(val / 100) * 100}%` }} />
                  ))}
                </div>
              </div>

              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Performance Metrics</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-300">Avg HR</span>
                    <span className="font-medium">72 bpm</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-300">Avg Duration</span>
                    <span className="font-medium">35 min</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-300">Avg Intensity</span>
                    <span className="font-medium">High</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'achievements' && (
            <motion.div
              key="achievements"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="grid grid-cols-1 md:grid-cols-3 gap-4"
            >
              {[
                { icon: '🔥', title: '7-Day Streak', desc: 'Worked out 7 days in a row' },
                { icon: '💪', title: 'Form Master', desc: '90%+ form score 10 times' },
                { icon: '🎯', title: 'Goal Crusher', desc: 'Reached 250 calories burned' },
              ].map((achievement, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-gradient-to-br from-yellow-900/40 to-yellow-950/40 border border-yellow-500/30 rounded-2xl p-6 text-center hover:border-yellow-500/60 transition-colors"
                >
                  <p className="text-4xl mb-2">{achievement.icon}</p>
                  <h4 className="font-semibold mb-1">{achievement.title}</h4>
                  <p className="text-xs text-slate-400">{achievement.desc}</p>
                </motion.div>
              ))}
            </motion.div>
          )}

          {activeTab === 'social' && (
            <motion.div
              key="social"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Friends</h3>
                <div className="space-y-3">
                  {['Drita', 'Genti', 'Ariana'].map((friend, i) => (
                    <div key={i} className="flex justify-between items-center">
                      <span className="text-slate-300">{friend}</span>
                      <span className="text-xs text-green-400">Online</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Leaderboard</h3>
                <ol className="space-y-2 text-sm">
                  <li>1. Arben - 2,450 kcal 🥇</li>
                  <li>2. Drita - 2,100 kcal 🥈</li>
                  <li>3. Genti - 1,950 kcal 🥉</li>
                </ol>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
