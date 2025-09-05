"use client";
import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface TextRevealEffectProps {
  text: string;
  className?: string;
  delay?: number;
  duration?: number;
  direction?: 'up' | 'down' | 'left' | 'right';
  stagger?: number;
}

export const TextRevealEffect: React.FC<TextRevealEffectProps> = ({
  text,
  className = "",
  delay = 0,
  duration = 0.5,
  direction = 'up',
  stagger = 0.05,
}) => {
  const words = text.split(' ');

  const directionVariants = {
    up: { y: 20, opacity: 0 },
    down: { y: -20, opacity: 0 },
    left: { x: 20, opacity: 0 },
    right: { x: -20, opacity: 0 },
  };

  const directionAnimate = {
    up: { y: 0, opacity: 1 },
    down: { y: 0, opacity: 1 },
    left: { x: 0, opacity: 1 },
    right: { x: 0, opacity: 1 },
  };

  return (
    <div className={cn("overflow-hidden", className)}>
      {words.map((word, index) => (
        <motion.span
          key={index}
          className="inline-block mr-2"
          initial={directionVariants[direction]}
          animate={directionAnimate[direction]}
          transition={{
            duration,
            delay: delay + index * stagger,
            ease: "easeOut"
          }}
        >
          {word}
        </motion.span>
      ))}
    </div>
  );
};

interface CharacterRevealEffectProps {
  text: string;
  className?: string;
  delay?: number;
  duration?: number;
  direction?: 'up' | 'down' | 'left' | 'right';
  stagger?: number;
}

export const CharacterRevealEffect: React.FC<CharacterRevealEffectProps> = ({
  text,
  className = "",
  delay = 0,
  duration = 0.05,
  direction = 'up',
  stagger = 0.02,
}) => {
  const characters = text.split('');

  const directionVariants = {
    up: { y: 20, opacity: 0 },
    down: { y: -20, opacity: 0 },
    left: { x: 20, opacity: 0 },
    right: { x: -20, opacity: 0 },
  };

  const directionAnimate = {
    up: { y: 0, opacity: 1 },
    down: { y: 0, opacity: 1 },
    left: { x: 0, opacity: 1 },
    right: { x: 0, opacity: 1 },
  };

  return (
    <div className={cn("overflow-hidden", className)}>
      {characters.map((char, index) => (
        <motion.span
          key={index}
          className="inline-block"
          initial={directionVariants[direction]}
          animate={directionAnimate[direction]}
          transition={{
            duration,
            delay: delay + index * stagger,
            ease: "easeOut"
          }}
        >
          {char === ' ' ? '\u00A0' : char}
        </motion.span>
      ))}
    </div>
  );
};

interface TypewriterEffectProps {
  text: string;
  className?: string;
  delay?: number;
  speed?: number;
  onComplete?: () => void;
}

export const TypewriterEffect: React.FC<TypewriterEffectProps> = ({
  text,
  className = "",
  delay = 0,
  speed = 50,
  onComplete,
}) => {
  const [displayedText, setDisplayedText] = React.useState('');
  const [currentIndex, setCurrentIndex] = React.useState(0);

  React.useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);

      return () => clearTimeout(timeout);
    } else if (onComplete) {
      onComplete();
    }
  }, [currentIndex, text, speed, onComplete]);

  React.useEffect(() => {
    if (delay > 0) {
      const timeout = setTimeout(() => {
        setCurrentIndex(0);
      }, delay);
      return () => clearTimeout(timeout);
    } else {
      setCurrentIndex(0);
    }
  }, [delay]);

  return (
    <motion.div
      className={cn("relative", className)}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, delay }}
    >
      <span>{displayedText}</span>
      <motion.span
        className="inline-block w-0.5 h-5 bg-current ml-1"
        animate={{ opacity: [0, 1, 0] }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
    </motion.div>
  );
};
