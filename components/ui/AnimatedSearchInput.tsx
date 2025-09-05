import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AnimatedSearchInputProps {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  onSubmit?: (value: string) => void;
  isLoading?: boolean;
  className?: string;
  icon?: React.ReactNode;
}

export const AnimatedSearchInput: React.FC<AnimatedSearchInputProps> = ({
  placeholder = "Enter location...",
  value,
  onChange,
  onSubmit,
  isLoading = false,
  className = "",
  icon
}) => {
  const [isFocused, setIsFocused] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSubmit && value.trim()) {
      onSubmit(value);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && onSubmit && value.trim()) {
      onSubmit(value);
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className={cn("relative w-full", className)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <motion.div
        className="relative group"
        onHoverStart={() => setIsHovered(true)}
        onHoverEnd={() => setIsHovered(false)}
      >
        {/* Background glow effect */}
        <motion.div
          className="absolute -inset-0.5 bg-gradient-to-r from-orange-600 via-red-600 to-yellow-600 rounded-2xl opacity-0 blur group-hover:opacity-20 transition-opacity duration-500"
          animate={{
            opacity: isFocused ? 0.3 : isHovered ? 0.2 : 0,
          }}
          transition={{ duration: 0.3 }}
        />

        {/* Main container */}
        <motion.div
          className="relative bg-black/40 backdrop-blur-xl border border-gray-700/50 rounded-xl overflow-visible"
          animate={{
            borderColor: isFocused 
              ? "rgba(249, 115, 22, 0.5)" 
              : isHovered 
              ? "rgba(156, 163, 175, 0.7)" 
              : "rgba(156, 163, 175, 0.3)"
          }}
          transition={{ duration: 0.2 }}
        >
          {/* Glass morphism overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-transparent pointer-events-none" />
          
          {/* Inner glow */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-orange-500/10 via-red-500/10 to-yellow-500/10 opacity-0"
            animate={{
              opacity: isFocused ? 1 : 0,
            }}
            transition={{ duration: 0.3 }}
          />

          <div className="relative flex items-center px-6 py-3 pt-6">
            {/* Icon */}
            {icon && (
              <motion.div
                className="flex-shrink-0 mr-3 text-gray-400"
                animate={{
                  color: isFocused ? "#f97316" : "#9ca3af",
                  scale: isFocused ? 1.1 : 1,
                }}
                transition={{ duration: 0.2 }}
              >
                {icon}
              </motion.div>
            )}

            {/* Input container */}
            <div className="relative flex-1">
              {/* Floating label */}
              <motion.label
                className="absolute left-0 text-gray-400 pointer-events-none select-none font-medium"
                animate={{
                  y: isFocused || value ? -24 : 0,
                  scale: isFocused || value ? 0.85 : 1,
                  color: isFocused ? "#f97316" : "#9ca3af",
                }}
                transition={{
                  duration: 0.2,
                  ease: "easeOut"
                }}
                style={{
                  transformOrigin: "0 0"
                }}
              >
                {placeholder}
              </motion.label>

              {/* Input field */}
              <input
                ref={inputRef}
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                className="w-full bg-transparent text-white text-lg placeholder-transparent outline-none disabled:opacity-50 disabled:cursor-not-allowed"
              />

              {/* Animated underline */}
              <motion.div
                className="absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-orange-500 via-red-500 to-yellow-500"
                initial={{ width: 0 }}
                animate={{
                  width: isFocused ? "100%" : "0%",
                }}
                transition={{ duration: 0.3, ease: "easeOut" }}
              />
            </div>

            {/* Loading spinner or submit button */}
            <motion.div
              className="flex-shrink-0 ml-3"
              animate={{
                scale: isLoading || (value && !isLoading) ? 1 : 0,
                opacity: isLoading || (value && !isLoading) ? 1 : 0,
              }}
              transition={{ duration: 0.2 }}
            >
              {isLoading ? (
                <motion.div
                  className="w-6 h-6 border-2 border-orange-500/30 border-t-orange-500 rounded-full"
                  animate={{ rotate: 360 }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                />
              ) : (
                <motion.button
                  type="submit"
                  className="w-6 h-6 text-orange-500 hover:text-orange-400 transition-colors duration-200"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={!value.trim() || isLoading}
                >
                  <svg 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2"
                    className="w-full h-full"
                  >
                    <path d="m9 18 6-6-6-6"/>
                  </svg>
                </motion.button>
              )}
            </motion.div>
          </div>
        </motion.div>

        {/* Floating particles effect */}
        <AnimatePresence>
          {isFocused && (
            <>
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-1 h-1 bg-orange-500/60 rounded-full pointer-events-none"
                  initial={{
                    opacity: 0,
                    x: Math.random() * 400 - 200,
                    y: Math.random() * 100 + 50,
                  }}
                  animate={{
                    opacity: [0, 1, 0],
                    y: [100, -20],
                    x: Math.random() * 400 - 200 + (Math.random() - 0.5) * 100,
                  }}
                  exit={{ opacity: 0 }}
                  transition={{
                    duration: 2 + Math.random() * 2,
                    repeat: Infinity,
                    delay: Math.random() * 2,
                  }}
                />
              ))}
            </>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.form>
  );
};
