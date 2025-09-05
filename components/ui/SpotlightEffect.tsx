import React, { useState, useRef, useEffect } from 'react';
import { motion, useMotionValue, useTransform } from 'framer-motion';
import { cn } from '@/lib/utils';

interface SpotlightEffectProps {
  children: React.ReactNode;
  className?: string;
  spotlightColor?: string;
  spotlightSize?: number;
  intensity?: number;
  enableFollowMouse?: boolean;
  enableClick?: boolean;
  animateOnHover?: boolean;
}

export const SpotlightEffect: React.FC<SpotlightEffectProps> = ({
  children,
  className = "",
  spotlightColor = "rgba(249, 115, 22, 0.3)", // Orange spotlight
  spotlightSize = 200,
  intensity = 0.8,
  enableFollowMouse = true,
  enableClick = false,
  animateOnHover = true
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isClicked, setIsClicked] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // Transform mouse position to spotlight position
  const spotlightX = useTransform(mouseX, (value) => value);
  const spotlightY = useTransform(mouseY, (value) => value);

  // Handle mouse movement
  useEffect(() => {
    if (!enableFollowMouse) return;

    const handleMouseMove = (event: MouseEvent) => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        mouseX.set(x);
        mouseY.set(y);
      }
    };

    const container = containerRef.current;
    if (container) {
      container.addEventListener('mousemove', handleMouseMove);
      return () => container.removeEventListener('mousemove', handleMouseMove);
    }
  }, [mouseX, mouseY, enableFollowMouse]);

  const handleClick = (event: React.MouseEvent) => {
    if (!enableClick) return;
    
    setIsClicked(true);
    
    // Reset click state after animation
    setTimeout(() => {
      setIsClicked(false);
    }, 600);
  };

  return (
    <motion.div
      ref={containerRef}
      className={cn("relative overflow-hidden", className)}
      onMouseEnter={() => animateOnHover && setIsHovered(true)}
      onMouseLeave={() => animateOnHover && setIsHovered(false)}
      onClick={handleClick}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Main content */}
      <div className="relative z-10">
        {children}
      </div>

      {/* Spotlight overlay */}
      <motion.div
        className="absolute inset-0 pointer-events-none z-20"
        initial={{ opacity: 0 }}
        animate={{
          opacity: enableFollowMouse && isHovered ? intensity : 0,
        }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="absolute rounded-full pointer-events-none"
          style={{
            left: spotlightX,
            top: spotlightY,
            width: spotlightSize,
            height: spotlightSize,
            background: `radial-gradient(circle, ${spotlightColor} 0%, transparent 70%)`,
            transform: 'translate(-50%, -50%)',
            filter: 'blur(1px)',
          }}
          animate={{
            scale: isClicked ? [1, 1.5, 1] : isHovered ? 1.1 : 1,
            opacity: isClicked ? [intensity, intensity * 1.5, intensity] : intensity,
          }}
          transition={{
            scale: { duration: isClicked ? 0.6 : 0.3 },
            opacity: { duration: isClicked ? 0.6 : 0.3 }
          }}
        />
      </motion.div>

      {/* Secondary glow effect */}
      <motion.div
        className="absolute inset-0 pointer-events-none z-15"
        initial={{ opacity: 0 }}
        animate={{
          opacity: enableFollowMouse && isHovered ? intensity * 0.5 : 0,
        }}
        transition={{ duration: 0.4, delay: 0.1 }}
      >
        <motion.div
          className="absolute rounded-full pointer-events-none"
          style={{
            left: spotlightX,
            top: spotlightY,
            width: spotlightSize * 1.5,
            height: spotlightSize * 1.5,
            background: `radial-gradient(circle, ${spotlightColor.replace('0.3', '0.1')} 0%, transparent 60%)`,
            transform: 'translate(-50%, -50%)',
            filter: 'blur(3px)',
          }}
          animate={{
            scale: isClicked ? [1, 1.8, 1] : isHovered ? 1.2 : 1,
          }}
          transition={{ duration: isClicked ? 0.8 : 0.4 }}
        />
      </motion.div>

      {/* Click ripple effect */}
      {enableClick && (
        <motion.div
          className="absolute inset-0 pointer-events-none z-25"
          initial={{ opacity: 0 }}
          animate={{
            opacity: isClicked ? [0, 1, 0] : 0,
          }}
          transition={{ duration: 0.6 }}
        >
          <motion.div
            className="absolute rounded-full pointer-events-none border-2"
            style={{
              left: spotlightX,
              top: spotlightY,
              width: 20,
              height: 20,
              borderColor: spotlightColor.replace('0.3', '0.8'),
              transform: 'translate(-50%, -50%)',
            }}
            animate={{
              width: isClicked ? [20, spotlightSize * 2] : 20,
              height: isClicked ? [20, spotlightSize * 2] : 20,
              opacity: isClicked ? [1, 0] : 0,
            }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          />
        </motion.div>
      )}

      {/* Ambient glow on hover */}
      {animateOnHover && (
        <motion.div
          className="absolute inset-0 pointer-events-none z-5"
          animate={{
            opacity: isHovered ? 0.1 : 0,
          }}
          transition={{ duration: 0.5 }}
          style={{
            background: `radial-gradient(ellipse at center, ${spotlightColor} 0%, transparent 70%)`,
          }}
        />
      )}

      {/* Floating particles effect */}
      {isHovered && enableFollowMouse && (
        <div className="absolute inset-0 pointer-events-none z-30">
          {[...Array(8)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 rounded-full pointer-events-none"
              style={{
                backgroundColor: spotlightColor.replace('0.3', '0.6'),
                left: spotlightX,
                top: spotlightY,
              }}
              initial={{
                opacity: 0,
                scale: 0,
              }}
              animate={{
                opacity: [0, 1, 0],
                scale: [0, 1, 0],
                x: Math.cos(i * 45 * Math.PI / 180) * 50,
                y: Math.sin(i * 45 * Math.PI / 180) * 50,
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.1,
                ease: "easeOut"
              }}
            />
          ))}
        </div>
      )}
    </motion.div>
  );
};

// Preset variations for common use cases
export const FireSpotlight: React.FC<Omit<SpotlightEffectProps, 'spotlightColor'>> = (props) => (
  <SpotlightEffect 
    {...props} 
    spotlightColor="rgba(249, 115, 22, 0.4)" // Fire orange
  />
);

export const SearchSpotlight: React.FC<Omit<SpotlightEffectProps, 'spotlightColor'>> = (props) => (
  <SpotlightEffect 
    {...props} 
    spotlightColor="rgba(59, 130, 246, 0.3)" // Blue
  />
);

export const DangerSpotlight: React.FC<Omit<SpotlightEffectProps, 'spotlightColor'>> = (props) => (
  <SpotlightEffect 
    {...props} 
    spotlightColor="rgba(239, 68, 68, 0.4)" // Red
  />
);

export const SafeSpotlight: React.FC<Omit<SpotlightEffectProps, 'spotlightColor'>> = (props) => (
  <SpotlightEffect 
    {...props} 
    spotlightColor="rgba(34, 197, 94, 0.3)" // Green
  />
);

// Advanced spotlight with multiple layers
export const MultiLayerSpotlight: React.FC<SpotlightEffectProps> = ({
  children,
  className = "",
  spotlightColor = "rgba(249, 115, 22, 0.3)",
  ...props
}) => {
  return (
    <SpotlightEffect
      className={className}
      spotlightColor={spotlightColor}
      {...props}
    >
      <div className="relative">
        {/* Inner spotlight layer */}
        <SpotlightEffect
          spotlightColor={spotlightColor.replace('0.3', '0.1')}
          spotlightSize={150}
          intensity={0.6}
          enableClick={false}
          animateOnHover={false}
          className="absolute inset-0"
        >
          <div className="opacity-0 pointer-events-none">{children}</div>
        </SpotlightEffect>
        
        {/* Content */}
        {children}
      </div>
    </SpotlightEffect>
  );
};
