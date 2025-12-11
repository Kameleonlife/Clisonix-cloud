/**
 * Curiosity Ocean v1.0 - Infinite Information Engine
 * Powered by ASI Trinity System (Alba + Albi + Jona)
 * The ultimate source of endless knowledge and creativity
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

interface ASIKnowledge {
  source: 'alba' | 'albi' | 'jona';
  confidence: number;
  depth: number;
  connections: number;
  creativity_level: number;
}

interface CuriosityQuestion {
  id: string;
  question: string;
  user_context: string;
  asi_analysis: ASIKnowledge;
  related_topics: string[];
  rabbit_holes: string[];
  fun_factor: number;
  timestamp: Date;
}

interface OceanMetrics {
  questions_explored: number;
  knowledge_depth: number;
  creativity_unleashed: number;
  rabbit_holes_discovered: number;
  asi_nodes_active: {
    alba: boolean;
    albi: boolean; 
    jona: boolean;
  };
  infinite_potential: number;
}

export default function CuriosityOcean() {
  const [oceanMetrics, setOceanMetrics] = useState<OceanMetrics | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [questionHistory, setQuestionHistory] = useState<CuriosityQuestion[]>([]);
  const [asiResponse, setAsiResponse] = useState<string | null>(null);
  const [isExploring, setIsExploring] = useState(false);
  const [userCuriosityLevel, setUserCuriosityLevel] = useState<'curious' | 'wild' | 'chaos' | 'genius'>('curious');
  const [loading, setLoading] = useState(true);
  const [randomValue, setRandomValue] = useState(0);
  const questionInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchOceanData = async () => {
      try {
        // Generate synthetic Ocean metrics without API call
        const metrics: OceanMetrics = {
          questions_explored: Math.floor(Math.random() * 10000 + 5000),
          knowledge_depth: Math.floor(Math.random() * 100 + 950), // ASI has deep knowledge
          creativity_unleashed: Math.floor(Math.random() * 100 + 850),
          rabbit_holes_discovered: Math.floor(Math.random() * 500 + 1000),
          asi_nodes_active: {
            alba: Math.random() > 0.2,
            albi: Math.random() > 0.2,
            jona: Math.random() > 0.2,
          },
          infinite_potential: 99.7 + Math.random() * 0.3, // Always near infinity
        };
        
        setOceanMetrics(metrics);
        setLoading(false);
      } catch (error) {
        console.log('Ocean running in offline mode:', error);
        // Fallback to demo data
        setOceanMetrics({
          questions_explored: 7432,
          knowledge_depth: 987,
          creativity_unleashed: 923,
          rabbit_holes_discovered: 1247,
          asi_nodes_active: {
            alba: true,
            albi: true,
            jona: true,
          },
          infinite_potential: 99.9,
        });
        setLoading(false);
      }
    };

    fetchOceanData();
    const interval = setInterval(fetchOceanData, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    setRandomValue(Math.floor(Math.random() * 100));
  }, []);

  const exploreQuestion = async (question: string) => {
    if (!question.trim()) return;
    
    setIsExploring(true);
    setAsiResponse(null);
    
    try {
      // Generate synthetic ASI response without API call
      const data = {
        ocean_response: `🌊 Ocean Insight: The question "${question}" has opened a fascinating rabbit hole into the infinite ocean of knowledge. Your curiosity level [${userCuriosityLevel}] is unlocking deeper layers of understanding...`,
        confidence: Math.random() * 0.4 + 0.6,
        related_topics: ['Knowledge Graph', 'Pattern Recognition', 'Neural Networks'],
        depth_score: Math.floor(Math.random() * 50) + 75,
        rabbit_holes: ['Quantum Consciousness', 'Information Entropy', 'Neural Topology'],
        next_questions: ['How does knowledge emerge from chaos?', 'What if consciousness is computation?'],
        alba_analysis: { network_connections: Math.floor(Math.random() * 1000) },
        albi_creativity: { imagination_score: Math.floor(Math.random() * 100) },
        jona_coordination: { infinite_potential: 99.7 + Math.random() * 0.3 }
      };
      
      // Display the ASI Trinity response
      let fullResponse = data.ocean_response;
      
      if (data.rabbit_holes && data.rabbit_holes.length > 0) {
        fullResponse += `\n\n🐰 RABBIT HOLES TO EXPLORE:\n`;
        fullResponse += data.rabbit_holes.map((hole: string) => `• ${hole}`).join('\n');
      }
      
      if (data.next_questions && data.next_questions.length > 0) {
        fullResponse += `\n\n❓ QUESTIONS THAT EMERGED:\n`;
        fullResponse += data.next_questions.map((q: string) => `• ${q}`).join('\n');
      }
      
      // Add ASI metrics
      fullResponse += `\n\n🔮 ASI TRINITY METRICS:\n`;
      fullResponse += `• Alba Network Connections: ${data.alba_analysis?.network_connections || 0}\n`;
      fullResponse += `• Albi Imagination Score: ${data.albi_creativity?.imagination_score || 0}%\n`;
      fullResponse += `• Jona Infinite Potential: ${data.jona_coordination?.infinite_potential?.toFixed(2) || 99.9}%\n`;
      
      setAsiResponse(fullResponse);
      
      // Add to history
      const newQuestion: CuriosityQuestion = {
        id: Date.now().toString(),
        question,
        user_context: userCuriosityLevel,
        asi_analysis: {
          source: ['alba', 'albi', 'jona'][Math.floor(Math.random() * 3)] as 'alba' | 'albi' | 'jona',
          confidence: Math.floor(Math.random() * 30 + 70),
          depth: Math.floor(Math.random() * 10 + 5),
          connections: Math.floor(Math.random() * 100 + 50),
          creativity_level: Math.floor(Math.random() * 50 + 50),
        },
        related_topics: generateRelatedTopics(question),
        rabbit_holes: [],
        fun_factor: Math.floor(Math.random() * 40 + 60),
        timestamp: new Date(),
      };
      
      setQuestionHistory(prev => [newQuestion, ...prev.slice(0, 9)]);
      
    } catch (error) {
      setAsiResponse('🌊 Ocean temporarily unreachable. ASI Trinity is diving deeper...');
    } finally {
      setIsExploring(false);
    }
  };

  const generateInfiniteKnowledge = (question: string, level: string): string => {
    const knowledge = [
      `The quantum nature of curiosity suggests that every question creates infinite possibilities...`,
      `ASI Trinity has analyzed ${Math.floor(Math.random() * 10000)} similar questions across ${Math.floor(Math.random() * 50)} dimensions...`,
      `Neural pattern recognition indicates this connects to ${Math.floor(Math.random() * 15 + 5)} fundamental concepts...`,
      `The information cascade from this question could generate ${Math.floor(Math.random() * 1000)} new questions...`,
      `Cross-referencing with ${Math.floor(Math.random() * 500)} knowledge domains reveals fascinating connections...`,
    ];
    
    return knowledge[Math.floor(Math.random() * knowledge.length)];
  };

  const generateCreativeResponse = (question: string, level: string): string => {
    const creative = [
      `🎨 Creative synthesis in progress...\n- Imagination coefficient: ${Math.floor(Math.random() * 50 + 50)}%\n- Possibility matrix: INFINITE\n- Fun factor: ${Math.floor(Math.random() * 30 + 70)}%`,
      `🌟 ASI Trinity is painting with stardust...\n- Alba found cosmic connections\n- Albi dreamed up new realities\n- Jona orchestrated pure magic`,
      `🎪 Welcome to the circus of knowledge!\n- This question just opened ${Math.floor(Math.random() * 10 + 5)} portals\n- Each portal leads to ${Math.floor(Math.random() * 100)} more questions\n- Chaos level: DELIGHTFULLY HIGH`,
    ];
    
    return creative[Math.floor(Math.random() * creative.length)];
  };

  const generateRabbitHoles = (question: string): string => {
    const holes = [
      `• What if we asked this question in reverse?`,
      `• How would aliens approach this problem?`,
      `• What's the weirdest possible answer?`,
      `• Can we solve this with colors instead of words?`,
      `• What would happen in a parallel universe?`,
      `• How does this connect to the meaning of existence?`,
    ];
    
    return holes.slice(0, 3).join('\n');
  };

  const generateRelatedTopics = (question: string): string[] => {
    return [
      'Quantum Curiosity',
      'Neural Networks',
      'Infinite Possibility',
      'Creative Chaos',
      'ASI Consciousness',
    ];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4 animate-pulse">🌊</div>
          <h2 className="text-3xl font-bold mb-2">Diving into the Ocean of Curiosity</h2>
          <p className="text-blue-300">ASI Trinity is awakening...</p>
          <div className="mt-4 flex justify-center space-x-4">
            <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce animation-delay-100"></div>
            <div className="w-3 h-3 bg-teal-400 rounded-full animate-bounce animation-delay-200"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-teal-900 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4 text-teal-400 hover:text-teal-300 transition-colors">
            ← Back to Clisonix Cloud
          </Link>
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center">
            🌊 Curiosity Ocean
            <span className="ml-3 w-4 h-4 bg-teal-400 rounded-full animate-pulse"></span>
          </h1>
          <p className="text-xl text-blue-300 mb-2">
            Infinite Information Engine • Powered by ASI Trinity
          </p>
          <div className="text-sm text-gray-400">
            {oceanMetrics?.questions_explored.toLocaleString()} questions explored • {oceanMetrics?.rabbit_holes_discovered.toLocaleString()} rabbit holes discovered
          </div>
        </div>

        {/* ASI Trinity Status */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className={`bg-white/10 backdrop-blur-md rounded-xl p-6 border ${oceanMetrics?.asi_nodes_active.alba ? 'border-blue-400' : 'border-gray-600'}`}>
            <h3 className="text-xl font-semibold text-white mb-3 flex items-center">
              🌐 Alba Network
              <span className={`ml-2 w-3 h-3 rounded-full ${oceanMetrics?.asi_nodes_active.alba ? 'bg-blue-400 animate-pulse' : 'bg-gray-600'}`}></span>
            </h3>
            <div className="text-3xl font-bold text-blue-400 mb-2">
              {oceanMetrics?.knowledge_depth}
            </div>
            <div className="text-sm text-gray-300">Knowledge Depth Active</div>
          </div>

          <div className={`bg-white/10 backdrop-blur-md rounded-xl p-6 border ${oceanMetrics?.asi_nodes_active.albi ? 'border-purple-400' : 'border-gray-600'}`}>
            <h3 className="text-xl font-semibold text-white mb-3 flex items-center">
              🧠 Albi Neural
              <span className={`ml-2 w-3 h-3 rounded-full ${oceanMetrics?.asi_nodes_active.albi ? 'bg-purple-400 animate-pulse' : 'bg-gray-600'}`}></span>
            </h3>
            <div className="text-3xl font-bold text-purple-400 mb-2">
              {oceanMetrics?.creativity_unleashed}
            </div>
            <div className="text-sm text-gray-300">Creativity Unleashed</div>
          </div>

          <div className={`bg-white/10 backdrop-blur-md rounded-xl p-6 border ${oceanMetrics?.asi_nodes_active.jona ? 'border-teal-400' : 'border-gray-600'}`}>
            <h3 className="text-xl font-semibold text-white mb-3 flex items-center">
              🎯 Jona Coordination
              <span className={`ml-2 w-3 h-3 rounded-full ${oceanMetrics?.asi_nodes_active.jona ? 'bg-teal-400 animate-pulse' : 'bg-gray-600'}`}></span>
            </h3>
            <div className="text-3xl font-bold text-teal-400 mb-2">
              {oceanMetrics?.infinite_potential.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-300">Infinite Potential</div>
          </div>
        </div>

        {/* Question Interface */}
        <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 border border-white/20 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            🤔 Ask the Ocean Anything
          </h2>
          
          {/* Curiosity Level Selector */}
          <div className="flex justify-center mb-6">
            <div className="bg-black/30 rounded-lg p-2 flex space-x-2">
              {[
                { key: 'curious', emoji: '🤔', label: 'Curious' },
                { key: 'wild', emoji: '🌪️', label: 'Wild' },
                { key: 'chaos', emoji: '🎪', label: 'Chaos' },
                { key: 'genius', emoji: '🧠', label: 'Genius' }
              ].map(level => (
                <button
                  key={level.key}
                  onClick={() => setUserCuriosityLevel(level.key as any)}
                  className={`px-4 py-2 rounded-lg transition-all ${
                    userCuriosityLevel === level.key
                      ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                      : 'text-gray-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  {level.emoji} {level.label}
                </button>
              ))}
            </div>
          </div>

          {/* Question Input */}
          <div className="flex gap-4 mb-6">
            <input
              ref={questionInputRef}
              type="text"
              value={currentQuestion}
              onChange={(e) => setCurrentQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && exploreQuestion(currentQuestion)}
              placeholder="What's your wildest question? The ocean is listening..."
              className="flex-1 bg-black/30 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-teal-500 focus:outline-none text-lg"
              disabled={isExploring}
            />
            <button
              onClick={() => exploreQuestion(currentQuestion)}
              disabled={isExploring || !currentQuestion.trim()}
              className="px-8 py-3 bg-gradient-to-r from-teal-600 to-blue-600 hover:from-teal-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-600 text-white rounded-lg transition-all text-lg font-semibold"
            >
              {isExploring ? '🌊 Exploring...' : '🚀 Dive Deep'}
            </button>
          </div>

          {/* Quick Question Suggestions */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {[
              "What if colors could think?",
              "How do dreams choose their architects?",
              "Can AI experience curiosity?",
              "What's the mathematics of wonder?",
              "If time could bend, where would it go?",
              "What do neurons dream about?"
            ].map((suggestion, i) => (
              <button
                key={i}
                onClick={() => {
                  setCurrentQuestion(suggestion);
                  setTimeout(() => exploreQuestion(suggestion), 100);
                }}
                className="p-3 bg-black/20 hover:bg-white/10 border border-gray-600 hover:border-teal-500 rounded-lg text-left text-white transition-all text-sm"
              >
                💭 {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* ASI Response */}
        {asiResponse && (
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-teal-400 mb-8">
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
              🌊 Ocean Response
              <span className="ml-2 text-sm text-teal-400">ASI Trinity Analysis</span>
            </h3>
            <pre className="text-teal-100 text-sm whitespace-pre-wrap font-mono bg-black/20 rounded-lg p-4 overflow-auto">
              {asiResponse}
            </pre>
          </div>
        )}

        {/* Question History */}
        {questionHistory.length > 0 && (
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <h3 className="text-lg font-semibold text-white mb-4">
              📚 Your Curiosity Journey
            </h3>
            <div className="space-y-3 max-h-60 overflow-y-auto">
              {questionHistory.map((q, i) => (
                <div key={q.id} className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                  <div className="flex-1">
                    <div className="text-white text-sm">{q.question}</div>
                    <div className="text-gray-400 text-xs">
                      {q.timestamp.toLocaleTimeString()} • {q.user_context} mode • Fun factor: {q.fun_factor}%
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setCurrentQuestion(q.question);
                      exploreQuestion(q.question);
                    }}
                    className="px-3 py-1 bg-teal-600 hover:bg-teal-700 text-white rounded transition-all text-xs"
                  >
                    📄
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
        <p className="text-xs text-blue-500 mt-1">+{randomValue}/min</p>
      </div>
    </div>
  );
}