"use client";
import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface EnhancedLoaderProps {
  text?: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'dots' | 'pulse' | 'spinner' | 'fire';
}

export const EnhancedLoader: React.FC<EnhancedLoaderProps> = ({
  text = "Loading...",
  className = "",
  size = 'md',
  variant = 'fire',
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  if (variant === 'fire') {
    return (
      <motion.div
        className={cn("flex flex-col items-center justify-center space-y-4", className)}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="relative">
          {/* Fire animation */}
          <motion.div
            className={cn("relative", sizeClasses[size])}
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 5, -5, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            {/* Fire base */}
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-orange-400 rounded-full" />
            
            {/* Fire flames */}
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute bottom-1 left-1/2 transform -translate-x-1/2"
                style={{
                  width: `${4 + i * 2}px`,
                  height: `${6 + i * 3}px`,
                  background: `linear-gradient(to top, ${
                    i === 0 ? '#ff6b35' : i === 1 ? '#f7931e' : '#ffd23f'
                  }, transparent)`,
                  borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
                }}
                animate={{
                  scaleY: [1, 1.2, 0.8, 1],
                  scaleX: [1, 0.8, 1.2, 1],
                  rotate: [0, 10, -10, 0],
                }}
                transition={{
                  duration: 1.5 + i * 0.3,
                  repeat: Infinity,
                  delay: i * 0.2,
                  ease: "easeInOut"
                }}
              />
            ))}
            
            {/* Sparks */}
            {[...Array(4)].map((_, i) => (
              <motion.div
                key={`spark-${i}`}
                className="absolute w-1 h-1 bg-yellow-300 rounded-full"
                style={{
                  left: `${30 + i * 10}%`,
                  top: `${20 + i * 5}%`,
                }}
                animate={{
                  y: [-5, -15, -5],
                  opacity: [0, 1, 0],
                  scale: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.3,
                  ease: "easeInOut"
                }}
              />
            ))}
          </motion.div>
        </div>
        
        {text && (
          <motion.p
            className={cn("text-gray-400 font-medium", textSizeClasses[size])}
            animate={{
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            {text}
          </motion.p>
        )}
      </motion.div>
    );
  }

  if (variant === 'dots') {
    return (
      <motion.div
        className={cn("flex flex-col items-center justify-center space-y-4", className)}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex space-x-2">
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              className={cn("bg-blue-500 rounded-full", sizeClasses[size])}
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                delay: i * 0.2,
                ease: "easeInOut"
              }}
            />
          ))}
        </div>
        {text && (
          <motion.p
            className={cn("text-gray-400 font-medium", textSizeClasses[size])}
            animate={{
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            {text}
          </motion.p>
        )}
      </motion.div>
    );
  }

  if (variant === 'pulse') {
    return (
      <motion.div
        className={cn("flex flex-col items-center justify-center space-y-4", className)}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className={cn("bg-gradient-to-r from-blue-500 to-purple-500 rounded-full", sizeClasses[size])}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.7, 1, 0.7],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        {text && (
          <motion.p
            className={cn("text-gray-400 font-medium", textSizeClasses[size])}
            animate={{
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            {text}
          </motion.p>
        )}
      </motion.div>
    );
  }

  // Default spinner
  return (
    <motion.div
      className={cn("flex flex-col items-center justify-center space-y-4", className)}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        className={cn("border-2 border-gray-300 border-t-blue-500 rounded-full", sizeClasses[size])}
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      {text && (
        <motion.p
          className={cn("text-gray-400 font-medium", textSizeClasses[size])}
          animate={{
            opacity: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          {text}
        </motion.p>
      )}
    </motion.div>
  );
};
