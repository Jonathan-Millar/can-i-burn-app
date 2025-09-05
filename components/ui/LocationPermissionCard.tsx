import React from 'react';
import { motion } from 'framer-motion';
import { Button } from './button';
import { Card } from './card';

interface LocationPermissionCardProps {
  onRequestLocation: () => void;
  onDismiss: () => void;
  isLoading: boolean;
  error: string | null;
}

export const LocationPermissionCard: React.FC<LocationPermissionCardProps> = ({
  onRequestLocation,
  onDismiss,
  isLoading,
  error,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="max-w-md mx-auto mb-8"
    >
      <Card className="bg-white/10 backdrop-blur-md border border-white/20 p-6 text-center">
        <div className="mb-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="w-8 h-8 text-white"
            >
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
          </div>
          
          <h3 className="text-xl font-semibold text-white mb-2">
            Get Your Location
          </h3>
          
          <p className="text-gray-300 text-sm leading-relaxed">
            Allow location access to automatically check fire restrictions for your current area.
            Your location data stays private and is not stored.
          </p>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg"
          >
            <p className="text-red-300 text-sm">{error}</p>
          </motion.div>
        )}

        <div className="flex gap-3 justify-center">
          <Button
            onClick={onRequestLocation}
            disabled={isLoading}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white border-0 px-6 py-2 rounded-lg font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Getting Location...
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="w-4 h-4"
                >
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                  <circle cx="12" cy="10" r="3" />
                </svg>
                Use My Location
              </div>
            )}
          </Button>
          
          <Button
            onClick={onDismiss}
            variant="outline"
            className="border-white/30 text-white hover:bg-white/10 px-6 py-2 rounded-lg font-medium transition-all duration-200"
          >
            Skip
          </Button>
        </div>

        <p className="text-xs text-gray-400 mt-4">
          You can always search for a location manually using the search bar above.
        </p>
      </Card>
    </motion.div>
  );
};
