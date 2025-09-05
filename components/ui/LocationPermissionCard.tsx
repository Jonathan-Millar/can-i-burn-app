import React from 'react';
import { motion } from 'framer-motion';
import { MapPin, X } from 'lucide-react';
import { Button } from './button';
import { Card } from './card';

interface LocationPermissionCardProps {
  onRequestLocation: () => void;
  onDismiss: () => void;
  isLoading: boolean;
  error: string | null;
  permission?: 'granted' | 'denied' | 'prompt' | 'unknown';
}

export const LocationPermissionCard: React.FC<LocationPermissionCardProps> = ({
  onRequestLocation,
  onDismiss,
  isLoading,
  error,
  permission = 'unknown',
}) => {
  const isDenied = permission === 'denied';
  const isFirstTime = permission === 'unknown' || permission === 'prompt';
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="max-w-md mx-auto mb-8"
    >
      <Card className="bg-white/10 backdrop-blur-md border border-white/20 p-6 text-center relative overflow-hidden">
        {/* Close button */}
        <motion.button
          onClick={onDismiss}
          className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center text-white/70 hover:text-white hover:bg-white/20 transition-all duration-200"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          <X className="w-4 h-4" />
        </motion.button>

        <div className="mb-4">
          <motion.div 
            className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center"
            animate={{ 
              scale: [1, 1.05, 1],
              rotate: [0, 5, -5, 0]
            }}
            transition={{ 
              duration: 2, 
              repeat: Infinity,
              repeatDelay: 3
            }}
          >
            <MapPin className="w-8 h-8 text-white" />
          </motion.div>
          
          <h3 className="text-xl font-semibold text-white mb-2">
            {isDenied ? 'Location Access Needed' : 'Get Your Location'}
          </h3>
          
          <p className="text-gray-300 text-sm leading-relaxed">
            {isDenied ? (
              <>
                Location access was previously denied. To automatically check fire restrictions for your area, 
                please enable location access in your browser settings and try again.
              </>
            ) : (
              <>
                Allow location access to automatically check fire restrictions for your current area.
                Your location data stays private and is not stored.
              </>
            )}
          </p>
          
          <div className="mt-3 text-xs text-gray-400">
            <p>• Works on all modern browsers and devices</p>
            <p>• Requires HTTPS for security</p>
            <p>• You can always search manually if needed</p>
            {isDenied && <p>• Check your browser's location settings</p>}
          </div>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg"
          >
            <p className="text-red-300 text-sm mb-2">{error}</p>
            <div className="text-xs text-gray-400">
              <p>• Make sure you're using HTTPS</p>
              <p>• Check your browser's location settings</p>
              <p>• Try refreshing the page</p>
            </div>
          </motion.div>
        )}

        <div className="flex gap-3 justify-center">
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              onClick={onRequestLocation}
              disabled={isLoading}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white border-0 px-6 py-2 rounded-lg font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Getting Location...
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  {isDenied ? 'Try Again' : 'Use My Location'}
                </div>
              )}
            </Button>
          </motion.div>
          
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              onClick={onDismiss}
              variant="outline"
              className="border-white/30 text-slate-700 hover:bg-white/10 px-6 py-2 rounded-lg font-medium transition-all duration-200"
            >
              Skip
            </Button>
          </motion.div>
        </div>

        <p className="text-xs text-gray-400 mt-4">
          You can always search for a location manually using the search bar above.
        </p>
      </Card>
    </motion.div>
  );
};
