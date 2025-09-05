import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Ban, AlertTriangle, CheckCircle, HelpCircle, ChevronDown, Timer, MapPin, Link2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CountyCondition {
  original_text: string;
  normalized_status: string;
  risk_level: string;
}

interface Zone {
  type: string;
  name: string;
  province: string;
  status: string;
}

interface EnhancedReportData {
  original_status?: string;
  county_conditions?: {
    restrictions: Record<string, CountyCondition>;
    validity_period?: string;
  };
  zone?: Zone;
  sources?: string[];
}

interface EnhancedReportCardProps {
  data: EnhancedReportData;
  className?: string;
}

export const EnhancedReportCard: React.FC<EnhancedReportCardProps> = ({
  data,
  className = "",
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return 'text-red-400 bg-red-500/10 border-red-500/20';
      case 'moderate':
        return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
      case 'low':
        return 'text-green-400 bg-green-500/10 border-green-500/20';
      default:
        return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'no fires':
        return Ban;
      case 'restricted burning':
        return AlertTriangle;
      case 'open burning':
        return CheckCircle;
      default:
        return HelpCircle;
    }
  };

  const countyConditions = data.county_conditions?.restrictions || {};
  const countyEntries = Object.entries(countyConditions);

  return (
    <motion.div
      className={cn("relative max-w-md w-full mx-auto", className)}
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      {/* Main Enhanced Report Card */}
      <div className="relative bg-black/30 backdrop-blur-xl border border-blue-500/20 rounded-2xl overflow-hidden">
        {/* Header gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-purple-500/10 to-indigo-500/10 opacity-50" />
        
        <div className="relative p-6 space-y-6">
          {/* Header */}
          <motion.div 
            className="flex items-center justify-between cursor-pointer"
            onClick={() => setIsExpanded(!isExpanded)}
            whileHover={{ scale: 1.01 }}
          >
            <div className="flex items-center space-x-3">
              <motion.div 
                className="w-3 h-3 bg-blue-400 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              <h3 className="text-white font-semibold text-lg">Enhanced Fire Report</h3>
              {data.zone && (
                <span className="text-blue-300 text-sm px-2 py-1 bg-blue-500/10 rounded-full border border-blue-500/20">
                  {data.zone.name} {data.zone.type}
                </span>
              )}
            </div>
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.3 }}
              className="text-blue-400"
            >
              <ChevronDown className="w-5 h-5" />
            </motion.div>
          </motion.div>

          {/* Current Zone Status */}
          {data.zone && (
            <motion.div 
              className="bg-white/5 rounded-xl p-4 border border-white/10"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-white font-medium">Current Zone Status</h4>
                  <p className="text-gray-300 text-sm">{data.zone.name} {data.zone.type}, {data.zone.province}</p>
                </div>
                <div className="flex items-center space-x-2">
                  {React.createElement(getStatusIcon(data.zone.status), { className: "w-6 h-6" })}
                  <span className={cn(
                    "px-3 py-1 rounded-full text-xs font-medium border",
                    data.zone.status === 'no fires' 
                      ? 'text-red-400 bg-red-500/10 border-red-500/20' 
                      : 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20'
                  )}>
                    {data.zone.status.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
              </div>
            </motion.div>
          )}

          {/* Validity Period */}
          {data.county_conditions?.validity_period && (
            <motion.div 
              className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-xl p-4 border border-purple-500/20"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              <div className="flex items-center space-x-2">
                <Timer className="w-4 h-4 text-purple-400" />
                <span className="text-white font-medium">Validity Period</span>
              </div>
              <p className="text-purple-200 text-sm mt-1">{data.county_conditions.validity_period}</p>
            </motion.div>
          )}

          {/* Expandable County Conditions */}
          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-4"
              >
                <div className="border-t border-white/10 pt-4">
                  <h4 className="text-white font-medium mb-4 flex items-center space-x-2">
                    <MapPin className="w-4 h-4" />
                    <span>All County Conditions</span>
                    <span className="text-gray-400 text-sm">({countyEntries.length} counties)</span>
                  </h4>
                  
                  {/* County Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {countyEntries.map(([county, condition], index) => (
                      <motion.div
                        key={county}
                        className="bg-white/5 rounded-lg p-3 border border-white/10 hover:bg-white/10 transition-all duration-200"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        whileHover={{ scale: 1.02 }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="text-white font-medium text-sm">{county}</h5>
                          {React.createElement(getStatusIcon(condition.normalized_status), { className: "w-5 h-5" })}
                        </div>
                        <p className="text-gray-300 text-xs mb-2">{condition.original_text}</p>
                        <div className="flex items-center justify-between">
                          <span className={cn(
                            "px-2 py-1 rounded text-xs font-medium border",
                            getRiskLevelColor(condition.risk_level)
                          )}>
                            {condition.risk_level} Risk
                          </span>
                          <span className={cn(
                            "text-xs",
                            condition.normalized_status === 'no fires' ? 'text-red-300' : 'text-yellow-300'
                          )}>
                            {condition.normalized_status.replace('_', ' ')}
                          </span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Sources */}
                {data.sources && data.sources.length > 0 && (
                  <motion.div
                    className="bg-gradient-to-r from-gray-500/10 to-slate-500/10 rounded-xl p-4 border border-gray-500/20"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                  >
                    <h5 className="text-white font-medium mb-2 flex items-center space-x-2">
                      <Link2 className="w-4 h-4" />
                      <span>Data Sources</span>
                    </h5>
                    <div className="space-y-2">
                      {data.sources.map((source, index) => (
                        <motion.a
                          key={index}
                          href={source}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-blue-300 text-xs hover:text-blue-200 transition-colors duration-200 break-all"
                          whileHover={{ x: 4 }}
                        >
                          {source}
                        </motion.a>
                      ))}
                    </div>
                  </motion.div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Animated border effect */}
        <motion.div
          className="absolute inset-0 border-2 border-blue-500/0 rounded-2xl"
          animate={{
            borderColor: ['rgba(59, 130, 246, 0)', 'rgba(59, 130, 246, 0.3)', 'rgba(59, 130, 246, 0)'],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </div>
    </motion.div>
  );
};
