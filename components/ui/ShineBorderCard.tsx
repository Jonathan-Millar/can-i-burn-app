import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, Ban, HelpCircle, X, MapPin, Clock } from 'lucide-react';
import { Badge } from './badge';
import { cn } from '@/lib/utils';
import { ShineBorder } from './shine-border';

interface FireRestrictionData {
  status: 'Open Burning' | 'Restricted Burning' | 'Burning Banned' | 'Unknown';
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

interface ShineBorderCardProps {
  data: LocationData;
  className?: string;
  onClose?: () => void;
}

export const ShineBorderCard: React.FC<ShineBorderCardProps> = ({
  data,
  className = "",
  onClose
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Open Burning':
        return {
          shineColor: ["#10B981", "#34D399", "#6EE7B7"], // Green gradient
          text: 'text-green-400',
          icon: CheckCircle
        };
      case 'Restricted Burning':
        return {
          shineColor: ["#F59E0B", "#FBBF24", "#FCD34D"], // Yellow/Orange gradient
          text: 'text-yellow-400',
          icon: AlertTriangle
        };
      case 'Burning Banned':
        return {
          shineColor: ["#EF4444", "#F87171", "#FCA5A5"], // Red gradient
          text: 'text-red-400',
          icon: Ban
        };
      default:
        return {
          shineColor: ["#6B7280", "#9CA3AF", "#D1D5DB"], // Gray gradient
          text: 'text-gray-400',
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
      {/* Main card with shine border */}
      <div className="relative bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden">
        <ShineBorder 
          shineColor={statusStyle.shineColor}
          borderWidth={2}
          duration={20}
        />
        
        {/* Glassmorphism overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/10 via-white/5 to-transparent pointer-events-none" />
        
        {/* Close button */}
        {onClose && (
          <motion.button
            onClick={onClose}
            className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center text-white/70 hover:text-white hover:bg-white/20 transition-all duration-200 z-10"
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
                  {data.burn_restriction.status}
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
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20">
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
              statusStyle.text.replace('text-', 'bg-')
            )} />
          </motion.div>
        </div>

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
      </div>
    </motion.div>
  );
};
