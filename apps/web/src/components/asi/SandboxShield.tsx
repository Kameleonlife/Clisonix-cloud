/**
 * Sandbox Shield Component
 * =======================
 * 
 * Jona's safety sandbox monitoring and control interface
 */

'use client';

import { motion } from 'framer-motion';
import { useASIStore } from '@/lib/stores/asi-store';
import { 
  sandboxShield,
  gradientText,
  safeGlow
} from '@/styles/asi.css';
import { 
  asiButton, 
  statusBadge, 
  progressBar,
  progressBarFill
} from '@/lib/components/variants';
import { clsx } from 'clsx';

interface SandboxShieldProps {
  className?: string;
}

export function SandboxShield({ className }: SandboxShieldProps) {
  const { 
    jona, 
    sandbox, 
    reportViolation,
    resetSystem 
  } = useASIStore();

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'low': return 'active';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'active';
    }
  };

  const getEthicsDescription = (ethics: string) => {
    switch (ethics) {
      case 'strict': return '🔒 Mbrojtje maksimale - Zero tolerance për rreziqe';
      case 'moderate': return '⚖️ Balancë mes sigurisë dhe funksionalitetit';
      case 'flexible': return '🔓 Fleksibilitet i shtuar me monitorim të kujdesshëm';
      default: return '🔐 Konfigurimi i paracaktuar i sigurisë';
    }
  };

  const handleEmergencyStop = () => {
    reportViolation('Emergency stop activated by user');
    // In a real system, this would halt all operations
  };

  return (
    <div className={clsx(sandboxShield, safeGlow, className)}>
      {/* Header */}
      <div className="text-center mb-6">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="text-3xl mb-2">🛡️</div>
          <h2 className={clsx(gradientText, 'text-xl font-bold mb-2')}>
            Jona Sandbox
          </h2>
          <p className="text-sm text-gray-400">
            Sistemi i Mbrojtjes dhe Etikës
          </p>
        </motion.div>
      </div>

      {/* Status Overview */}
      <div className="space-y-4 mb-6">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Status:</span>
          <div className={statusBadge({ 
            status: sandbox.active ? 'active' : 'inactive',
            size: 'md'
          })}>
            {sandbox.active ? 'AKTIV' : 'JOAKTIV'}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Niveli i Kërcënimit:</span>
          <div className={statusBadge({ 
            status: getThreatLevelColor(sandbox.threatLevel),
            size: 'md'
          })}>
            {sandbox.threatLevel.toUpperCase()}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Shkeljet:</span>
          <span className={`text-sm font-mono ${
            sandbox.violations === 0 ? 'text-green-400' : 
            sandbox.violations < 5 ? 'text-yellow-400' : 'text-red-400'
          }`}>
            {sandbox.violations}
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Etika:</span>
          <div className={statusBadge({ 
            status: jona.ethics === 'strict' ? 'active' : 'warning',
            size: 'sm'
          })}>
            {jona.ethics.toUpperCase()}
          </div>
        </div>
      </div>

      {/* Ethics Level Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-300">Niveli i Etikës:</span>
          <span className="text-xs text-gray-500">
            {jona.ethics === 'strict' ? '100%' : 
             jona.ethics === 'moderate' ? '70%' : '40%'}
          </span>
        </div>
        
        <div className={progressBar({ size: 'md' })}>
          <motion.div
            initial={{ width: 0 }}
            animate={{ 
              width: jona.ethics === 'strict' ? '100%' : 
                     jona.ethics === 'moderate' ? '70%' : '40%'
            }}
            transition={{ duration: 1, delay: 0.5 }}
            className={progressBarFill({ 
              color: jona.ethics === 'strict' ? 'green' : 
                     jona.ethics === 'moderate' ? 'yellow' : 'red'
            })}
          />
        </div>
        
        <div className="mt-1 text-xs text-gray-500">
          {getEthicsDescription(jona.ethics)}
        </div>
      </div>

      {/* Recent Violations */}
      {jona.violations.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-300 mb-2">
            🚨 Shkelje të Fundit:
          </h3>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {jona.violations.slice(-3).map((violation, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="text-xs text-red-400 bg-red-500/10 p-2 rounded border border-red-500/20"
              >
                {violation}
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Control Buttons */}
      <div className="space-y-3">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleEmergencyStop}
          className={asiButton({ 
            intent: 'danger', 
            size: 'md',
            fullWidth: true
          })}
        >
          🛑 STOP EMERGJENCIAL
        </motion.button>

        <div className="grid grid-cols-2 gap-2">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={asiButton({ 
              intent: sandbox.active ? 'warning' : 'success', 
              size: 'sm'
            })}
          >
            {sandbox.active ? 'Çaktivizo' : 'Aktivizo'}
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={resetSystem}
            className={asiButton({ 
              intent: 'secondary', 
              size: 'sm'
            })}
          >
            Reset
          </motion.button>
        </div>
      </div>

      {/* Real-time Monitor */}
      <div className="mt-6 pt-4 border-t border-purple-500/20">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-gray-400">Monitorim Real-time:</span>
          <motion.div
            animate={{ 
              scale: [1, 1.1, 1],
              opacity: [0.5, 1, 0.5]
            }}
            transition={{ 
              duration: 2, 
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="w-2 h-2 bg-green-400 rounded-full"
          />
        </div>
        
        <div className="text-xs text-gray-500 space-y-1">
          {sandbox.active && (
            <>
              <div>✅ Komanda po monitorohen</div>
              <div>🔍 Patterns po analizohen</div>
              <div>🛡️ Mbrojtja është aktive</div>
            </>
          )}
          {!sandbox.active && (
            <div className="text-red-400">
              ⚠️ Sandbox është i çaktivizuar
            </div>
          )}
        </div>
      </div>

      {/* Jona Signature */}
      <div className="mt-4 text-center">
        <div className="text-xs text-purple-400/70">
          💜 Me dashuri nga Jona
        </div>
      </div>
    </div>
  );
}

