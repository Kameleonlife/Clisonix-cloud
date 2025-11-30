/**
 * ASI Terminal Component
 * =====================
 * 
 * Interactive terminal interface for Clisonix ASI system
 */

'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState, useRef, useEffect } from 'react';
import { useASIStore } from '@/lib/stores/asi-store';

// Client-only time display component to prevent hydration mismatch
function ClientTimeDisplay({ timestamp }: { timestamp: Date }) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  if (!mounted) {
    return <span>--:--:--</span>;
  }
  
  return <span>{timestamp.toLocaleTimeString()}</span>;
}

import { asiButton, commandInputVariants, statusBadge } from '@/lib/components/variants';
import { clsx } from 'clsx';

interface ASITerminalProps {
  className?: string;
  maxCommands?: number;
}

export function ASITerminal({ className, maxCommands = 10 }: ASITerminalProps) {
  const [input, setInput] = useState('');
  const [isInputFocused, setIsInputFocused] = useState(false);
  const terminalEndRef = useRef<HTMLDivElement>(null);
  
  const { 
    commands, 
    executeCommand, 
    clearCommands,
    alba,
    sandbox
  } = useASIStore();

  // Auto scroll to bottom when new commands are added
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [commands]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    executeCommand(input.trim());
    setInput('');
  };

  const handleQuickCommand = (command: string) => {
    executeCommand(command);
  };

  const getCommandStyle = (status: string) => {
    switch (status) {
      case 'completed': return 'commandCompleted';
      case 'rejected': return 'commandRejected';
      case 'executing': return 'commandExecuting';
      default: return 'commandExecuting';
    }
  };

  const getInputState = () => {
    if (alba.status === 'active') return 'processing';
    if (sandbox.violations > 0) return 'error';
    return 'normal';
  };

  return (
    <div className={clsx('asiTerminal', className)}>
      {/* Terminal Header */}
      <div className="terminalHeader">
        <div className="flex items-center space-x-2">
          <div className="terminalDotRed" />
          <div className="terminalDotYellow" />
          <div className="terminalDotGreen" />
        </div>
        <div className="flex-1 flex items-center justify-center">
          <span className="text-gray-400 text-sm font-mono">
            ASI Terminal v2.1.0
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <div className={statusBadge({ 
            status: alba.status === 'active' ? 'processing' : 'active',
            size: 'sm'
          })}>
            Alba {alba.status}
          </div>
          <button
            onClick={clearCommands}
            className={asiButton({ 
              intent: 'ghost', 
              size: 'xs' 
            })}
          >
            Clear
          </button>
        </div>
      </div>

      {/* Command History */}
      <div className="p-6 space-y-3 max-h-96 overflow-y-auto">
        {/* Welcome Message */}
        {commands.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-gray-400 text-sm space-y-2"
          >
            <div>🤖 <span className="text-cyan-400">Clisonix ASI</span> Online</div>
            <div>🔐 <span className="text-purple-400">Jona Sandbox</span> Active</div>
            <div>🌐 <span className="text-sky-400">Alba Network</span> Monitoring</div>
            <div>💡 <span className="text-emerald-400">Albi Intelligence</span> Ready</div>
            <div className="pt-2 text-xs">
              Shkruani një komandë për të filluar...
            </div>
          </motion.div>
        )}

        {/* Commands */}
        <AnimatePresence>
          {commands.slice(-maxCommands).map((command, index) => (
            <motion.div
              key={command.id}
              initial={{ opacity: 0, x: -20, height: 0 }}
              animate={{ opacity: 1, x: 0, height: 'auto' }}
              exit={{ opacity: 0, x: 20, height: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className={getCommandStyle(command.status)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-xs text-gray-500 font-mono">
                      <ClientTimeDisplay timestamp={command.timestamp} />
                    </span>
                    <span className="flex-1 font-mono text-sm">
                      <span className="text-cyan-400">ASI&gt;</span> {command.text}
                    </span>
                  </div>
                  
                  {command.output && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      transition={{ delay: 0.2 }}
                      className="text-sm text-gray-300 font-mono ml-4 pl-4 border-l border-gray-600"
                    >
                      {command.output.split('\n').map((line, lineIndex) => (
                        <div key={lineIndex} className="mb-1">
                          {line}
                        </div>
                      ))}
                    </motion.div>
                  )}
                </div>

                <div className={statusBadge({ 
                  status: command.status === 'completed' ? 'active' : 
                         command.status === 'rejected' ? 'error' :
                         command.status === 'executing' ? 'processing' : 'warning',
                  size: 'sm'
                })}>
                  {command.status}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        <div ref={terminalEndRef} />
      </div>

      {/* Quick Commands */}
      <div className="px-6 pb-4">
        <div className="text-xs text-gray-500 mb-2">Komanda të shpejta:</div>
        <div className="flex flex-wrap gap-2">
          {[
            { cmd: 'status', label: 'Status' },
            { cmd: 'analyze system', label: 'Analizë' },
            { cmd: 'health check', label: 'Shëndeti' },
            { cmd: 'optimize performance', label: 'Optimizim' },
            { cmd: 'backup data', label: 'Backup' }
          ].map(({ cmd, label }) => (
            <motion.button
              key={cmd}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleQuickCommand(cmd)}
              className={asiButton({ 
                intent: 'ghost', 
                size: 'xs'
              })}
            >
              {label}
            </motion.button>
          ))}
        </div>
      </div>

      {/* Command Input */}
      <form onSubmit={handleSubmit} className="p-6 border-t border-gray-700">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onFocus={() => setIsInputFocused(true)}
            onBlur={() => setIsInputFocused(false)}
            placeholder="Shkruani komandën tuaj këtu... (p.sh: 'analyze data', 'system status')"
            className={commandInputVariants({ 
              state: getInputState()
            })}
            disabled={alba.status === 'active'}
          />
          
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!input.trim() || alba.status === 'active'}
            className={asiButton({ 
              intent: alba.status === 'active' ? 'secondary' : 'primary',
              state: alba.status === 'active' ? 'processing' : 'idle'
            })}
          >
            {alba.status === 'active' ? 'Duke procesuar...' : 'Ekzekuto'}
          </motion.button>
        </div>

        {/* Input Hint */}
        {isInputFocused && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-2 text-xs text-gray-500"
          >
            💡 Provoni: &quot;monitor network&quot;, &quot;scan security&quot;, &quot;backup files&quot;, &quot;optimize system&quot;
          </motion.div>
        )}
      </form>
    </div>
  );
}

