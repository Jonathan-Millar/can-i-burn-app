import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, Ban, HelpCircle, X, MapPin, Clock } from 'lucide-react';
import { Badge } from './badge';
import { cn } from '@/lib/utils';

interface FireRestrictionData {
  status: 'ALLOWED' | 'RESTRICTED' | 'BANNED' | 'UNKNOWN';
  details: string | string[];
  source: string;
  last_updated: string;
  enhanced_report?: any;
}

interface LocationData {
  latitude: number;
  longitude: number;
  province: string;
  county?: string;
  burn_restriction: FireRestrictionData;
}

interface GlassMorphismCardProps {
  data: LocationData;
  className?: string;
  onClose?: () => void;
}

export const GlassMorphismCard: React.FC<GlassMorphismCardProps> = ({
  data,
  className = "",
  onClose
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ALLOWED':
        return {
          bg: 'from-green-500/20 to-emerald-600/20',
          border: 'border-green-500/30',
          text: 'text-green-400',
          glow: 'shadow-green-500/20',
          icon: CheckCircle
        };
      case 'RESTRICTED':
        return {
          bg: 'from-yellow-500/20 to-orange-600/20',
          border: 'border-yellow-500/30',
          text: 'text-yellow-400',
          glow: 'shadow-yellow-500/20',
          icon: AlertTriangle
        };
      case 'BANNED':
        return {
          bg: 'from-red-500/20 to-rose-600/20',
          border: 'border-red-500/30',
          text: 'text-red-400',
          glow: 'shadow-red-500/20',
          icon: Ban
        };
      default:
        return {
          bg: 'from-gray-500/20 to-slate-600/20',
          border: 'border-gray-500/30',
          text: 'text-gray-400',
          glow: 'shadow-gray-500/20',
          icon: HelpCircle
        };
    }
  };

  const statusStyle = getStatusColor(data.burn_restriction.status);

  return (
    <motion.div
      className={cn("relative max-w-md w-full mx-auto", className)}
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -50, scale: 0.9 }}
      transition={{
        duration: 0.5,
        ease: [0.23, 1, 0.320, 1]
      }}
      layout
    >
      {/* Background glow */}
      <motion.div
        className={cn("absolute -inset-1 rounded-3xl blur-lg", statusStyle.glow)}
        animate={{
          opacity: [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        style={{
          background: `linear-gradient(45deg, ${statusStyle.bg.replace('/20', '/10')})`
        }}
      />

      {/* Main card */}
      <motion.div
        className={cn(
          "relative bg-black/40 backdrop-blur-xl border rounded-3xl overflow-hidden",
          statusStyle.border
        )}
      >
        {/* Glass morphism overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/10 via-white/5 to-transparent" />
        
        {/* Status gradient overlay */}
        <motion.div
          className={cn("absolute inset-0 bg-gradient-to-br opacity-10", statusStyle.bg)}
          animate={{
            opacity: [0.05, 0.15, 0.05],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />

        {/* Close button */}
        {onClose && (
          <motion.button
            onClick={onClose}
            className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center text-white/70 hover:text-white hover:bg-white/20 transition-all duration-200"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            <X className="w-4 h-4" />
          </motion.button>
        )}

        <div className="relative p-6 space-y-6">
          {/* Header */}
          <motion.div
            className="space-y-2"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <div className="flex items-center space-x-3">
              <motion.div
                className={cn("flex items-center justify-center w-8 h-8", statusStyle.text)}
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  repeatDelay: 3,
                }}
              >
                <statusStyle.icon className="w-6 h-6" />
              </motion.div>
              <div>
                <h3 className="text-white font-bold text-xl">
                  {data.burn_restriction.status.charAt(0) + data.burn_restriction.status.slice(1).toLowerCase()} Burns
                </h3>
                <p className="text-gray-400 text-sm">
                  {data.province}{data.county && `, ${data.county}`}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Status details */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            {/* Details list */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
              <ul className="text-gray-200 text-sm leading-relaxed space-y-2 list-disc list-inside">
                {(() => {
                  console.log('Details type:', typeof data.burn_restriction.details);
                  console.log('Details value:', data.burn_restriction.details);
                  console.log('Is array:', Array.isArray(data.burn_restriction.details));
                  
                  if (Array.isArray(data.burn_restriction.details)) {
                    return data.burn_restriction.details.map((detail, index) => (
                      <li key={index} className="text-gray-200 ml-0">
                        {detail}
                      </li>
                    ));
                  }
                  
                  if (typeof data.burn_restriction.details === 'string') {
                    // Try different split methods
                    const parts = data.burn_restriction.details.includes('\n') 
                      ? data.burn_restriction.details.split('\n')
                      : data.burn_restriction.details.split('. ');
                    
                    return parts.filter(Boolean).map((detail, index) => (
                      <li key={index} className="text-gray-200 ml-0">
                        {detail.trim()}{detail.endsWith('.') ? '' : '.'}
                      </li>
                    ));
                  }
                  
                  return (
                    <li className="text-gray-200 ml-0">
                      No details available
                    </li>
                  );
                })()}
              </ul>
            </div>

          </motion.div>

          {/* Location coordinates */}
          <motion.div
            className="flex items-center justify-between text-xs text-gray-500"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {data.latitude.toFixed(4)}, {data.longitude.toFixed(4)}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {new Date(data.burn_restriction.last_updated).toLocaleDateString()}
            </span>
          </motion.div>

          {/* Source */}
          <motion.div
            className="pt-4 border-t border-white/10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full" />
              <span className="text-gray-400 text-xs">
                Source: {data.burn_restriction.source}
              </span>
            </div>
          </motion.div>

          {/* Animated status indicator */}
          <motion.div
            className="absolute -bottom-2 left-1/2 transform -translate-x-1/2"
            animate={{
              y: [0, -5, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <div className={cn(
              "w-12 h-1 rounded-full opacity-60",
              statusStyle.bg.replace('/20', '/40')
            )} />
          </motion.div>
        </div>

        {/* Shimmer effect */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full"
          animate={{
            translateX: ['100%', '100%', '-100%'],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            repeatDelay: 5,
            ease: "easeInOut"
          }}
        />
      </motion.div>

      {/* Floating elements */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(3)].map((_, i) => (
          <motion.div
            key={i}
            className={cn("absolute w-1 h-1 rounded-full", statusStyle.text.replace('text-', 'bg-'))}
            style={{
              top: `${20 + i * 30}%`,
              right: `${-10 + i * 5}%`,
            }}
            animate={{
              y: [0, -20, 0],
              opacity: [0, 1, 0],
              scale: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 3 + i,
              repeat: Infinity,
              delay: i * 0.5,
            }}
          />
        ))}
      </div>
    </motion.div>
  );
};
