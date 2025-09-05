import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface SophisticatedLoaderProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'fire' | 'search' | 'data' | 'pulse';
  message?: string;
  className?: string;
}

export const SophisticatedLoader: React.FC<SophisticatedLoaderProps> = ({
  size = 'md',
  variant = 'fire',
  message,
  className = ""
}) => {
  const sizeMap = {
    sm: { container: 'w-16 h-16', text: 'text-sm', spacing: 'mt-2' },
    md: { container: 'w-24 h-24', text: 'text-base', spacing: 'mt-3' },
    lg: { container: 'w-32 h-32', text: 'text-lg', spacing: 'mt-4' },
    xl: { container: 'w-40 h-40', text: 'text-xl', spacing: 'mt-6' }
  };

  const currentSize = sizeMap[size];

  const renderFireLoader = () => (
    <div className={cn("relative", currentSize.container)}>
      {/* Outer ring with fire gradient */}
      <motion.div
        className="absolute inset-0 rounded-full bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 opacity-20"
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* Middle ring */}
      <motion.div
        className="absolute inset-2 rounded-full border-2 border-orange-500/30"
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      
      {/* Inner rotating elements */}
      <div className="absolute inset-0 flex items-center justify-center">
        {[...Array(8)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-gradient-to-t from-red-500 to-orange-400 rounded-full"
            style={{
              transformOrigin: `0 ${currentSize.container === 'w-16 h-16' ? '32px' : currentSize.container === 'w-24 h-24' ? '48px' : currentSize.container === 'w-32 h-32' ? '64px' : '80px'}`,
            }}
            animate={{
              rotate: 360,
              scale: [0.5, 1, 0.5],
            }}
            transition={{
              rotate: {
                duration: 2,
                repeat: Infinity,
                ease: "linear",
                delay: i * 0.125,
              },
              scale: {
                duration: 1,
                repeat: Infinity,
                ease: "easeInOut",
                delay: i * 0.125,
              }
            }}
          />
        ))}
      </div>
      
      {/* Central flame effect */}
      <motion.div
        className="absolute inset-6 bg-gradient-to-t from-orange-600 via-red-500 to-yellow-400 rounded-full blur-sm"
        animate={{
          scale: [0.8, 1.2, 0.8],
          opacity: [0.6, 1, 0.6],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
    </div>
  );

  const renderSearchLoader = () => (
    <div className={cn("relative", currentSize.container)}>
      {/* Search ring */}
      <motion.div
        className="absolute inset-0 rounded-full border-4 border-transparent bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-30"
        style={{ backgroundClip: 'padding-box' }}
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      
      {/* Scanning beam */}
      <motion.div
        className="absolute inset-0 rounded-full overflow-hidden"
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "linear"
        }}
      >
        <div className="absolute top-0 left-1/2 w-0.5 h-full bg-gradient-to-b from-cyan-400 via-blue-500 to-transparent transform -translate-x-1/2" />
      </motion.div>
      
      {/* Pulsing dots */}
      {[...Array(4)].map((_, i) => (
        <motion.div
          key={i}
          className={cn(
            "absolute w-3 h-3 bg-blue-400 rounded-full",
            i === 0 && "top-0 left-1/2 transform -translate-x-1/2",
            i === 1 && "top-1/2 right-0 transform -translate-y-1/2",
            i === 2 && "bottom-0 left-1/2 transform -translate-x-1/2",
            i === 3 && "top-1/2 left-0 transform -translate-y-1/2"
          )}
          animate={{
            scale: [0.5, 1.2, 0.5],
            opacity: [0.3, 1, 0.3],
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            delay: i * 0.25,
          }}
        />
      ))}
    </div>
  );

  const renderDataLoader = () => (
    <div className={cn("relative", currentSize.container)}>
      {/* Data streams */}
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute bg-gradient-to-t from-green-400 to-emerald-300 rounded-full opacity-70"
          style={{
            width: '2px',
            height: `${20 + i * 8}%`,
            left: `${15 + i * 12}%`,
            bottom: '20%',
          }}
          animate={{
            scaleY: [0.3, 1, 0.3],
            opacity: [0.3, 1, 0.3],
          }}
          transition={{
            duration: 1.2,
            repeat: Infinity,
            delay: i * 0.1,
            ease: "easeInOut"
          }}
        />
      ))}
      
      {/* Central processor */}
      <motion.div
        className="absolute top-1/2 left-1/2 w-8 h-8 transform -translate-x-1/2 -translate-y-1/2"
        animate={{
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <div className="w-full h-full bg-gradient-to-br from-green-400 to-blue-500 rounded-lg opacity-80" />
        <motion.div
          className="absolute inset-1 bg-black/20 rounded"
          animate={{
            opacity: [0.2, 0.8, 0.2],
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
          }}
        />
      </motion.div>
      
      {/* Orbiting data points */}
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-cyan-400 rounded-full"
          style={{
            top: '50%',
            left: '50%',
          }}
          animate={{
            rotate: 360,
          }}
          transition={{
            duration: 2 + i * 0.5,
            repeat: Infinity,
            ease: "linear",
          }}
          transformTemplate={({ rotate }) => 
            `translate(-50%, -50%) rotate(${rotate}) translateX(${30 + i * 10}px) rotate(-${rotate})`
          }
        />
      ))}
    </div>
  );

  const renderPulseLoader = () => (
    <div className={cn("relative", currentSize.container)}>
      {/* Concentric pulse rings */}
      {[...Array(4)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute inset-0 rounded-full border-2 border-purple-500/30"
          animate={{
            scale: [1, 1.5 + i * 0.3],
            opacity: [0.8, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            delay: i * 0.4,
            ease: "easeOut"
          }}
        />
      ))}
      
      {/* Central core */}
      <motion.div
        className="absolute top-1/2 left-1/2 w-6 h-6 transform -translate-x-1/2 -translate-y-1/2 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full"
        animate={{
          scale: [0.8, 1.2, 0.8],
          boxShadow: [
            '0 0 0 0 rgba(168, 85, 247, 0.4)',
            '0 0 20px 10px rgba(168, 85, 247, 0.1)',
            '0 0 0 0 rgba(168, 85, 247, 0.4)'
          ],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
    </div>
  );

  const renderLoader = () => {
    switch (variant) {
      case 'fire':
        return renderFireLoader();
      case 'search':
        return renderSearchLoader();
      case 'data':
        return renderDataLoader();
      case 'pulse':
        return renderPulseLoader();
      default:
        return renderFireLoader();
    }
  };

  return (
    <motion.div
      className={cn("flex flex-col items-center justify-center", className)}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ duration: 0.3 }}
    >
      {/* Loader animation */}
      <div className="relative">
        {renderLoader()}
        
        {/* Backdrop blur effect */}
        <div className="absolute inset-0 bg-black/20 backdrop-blur-sm rounded-full opacity-30 -z-10" />
      </div>

      {/* Loading message */}
      {message && (
        <motion.div
          className={cn(
            "text-gray-300 font-medium text-center max-w-xs",
            currentSize.text,
            currentSize.spacing
          )}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <motion.span
            animate={{
              opacity: [1, 0.5, 1],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            {message}
          </motion.span>
        </motion.div>
      )}
    </motion.div>
  );
};
