import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AnimatedSearchInput } from './ui/AnimatedSearchInput';
import { SophisticatedLoader } from './ui/SophisticatedLoader';
import { GlassMorphismCard } from './ui/GlassMorphismCard';
import { EnhancedReportCard } from './ui/EnhancedReportCard';
import { LocationPermissionCard } from './ui/LocationPermissionCard';
import { useGeolocation } from '../lib/useGeolocation';

// Data types matching the card's expected shape
interface UICardRestrictionData {
  status: 'ALLOWED' | 'RESTRICTED' | 'BANNED' | 'UNKNOWN';
  details: string | string[]; // Allow both string and array
  source: string;
  last_updated: string;
  enhanced_report?: any;
}

interface UICardLocationData {
  latitude: number;
  longitude: number;
  province: string; // Full name, e.g., "New Brunswick"
  county?: string;
  burn_restriction: UICardRestrictionData;
}

const provinceFullName: Record<string, string> = {
  PEI: 'Prince Edward Island',
  NB: 'New Brunswick',
  NS: 'Nova Scotia',
  ON: 'Ontario',
  BC: 'British Columbia',
  AB: 'Alberta',
  SK: 'Saskatchewan',
  MB: 'Manitoba',
  QC: 'Quebec',
  NL: 'Newfoundland and Labrador',
  YT: 'Yukon',
  NT: 'Northwest Territories',
  NU: 'Nunavut',
};

function mapStatusToUI(burnStatus?: string): UICardRestrictionData['status'] {
  const s = (burnStatus || '').toLowerCase();
  if (s.includes('no fires') || s.includes('no fire') || s.includes('banned')) return 'BANNED';
  if (s.includes('restricted')) return 'RESTRICTED';
  if (s.includes('open') || s.includes('allowed') || s.includes('permitted')) return 'ALLOWED';
  return 'UNKNOWN';
}

function mapApiToUICard(data: any): UICardLocationData {
  const uiStatus = mapStatusToUI(data.burn_status);
  const provinceName = provinceFullName[data.province] || data.province || 'Unknown';

  // Keep details as array for list display
  const details = Array.isArray(data.details) ? data.details : (data.details ? [data.details] : ['No additional details provided.']);

  return {
    latitude: data.latitude,
    longitude: data.longitude,
    province: provinceName,
    county: data.county || undefined,
    burn_restriction: {
      status: uiStatus,
      details: details,
      source: data.source || 'Unknown source',
      last_updated: data.last_updated || new Date().toISOString(),
      enhanced_report: data.enhanced_report,
    },
  };
}

export const FireRestrictionApp: React.FC = () => {
  const [searchValue, setSearchValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<UICardLocationData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showLocationPermission, setShowLocationPermission] = useState(false);
  const [hasRequestedLocation, setHasRequestedLocation] = useState(false);

  const {
    coordinates,
    error: locationError,
    isLoading: isLocationLoading,
    permission,
    requestLocation,
    address: locationAddress,
  } = useGeolocation({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 300000, // 5 minutes
    fallbackToIP: true,
    addressLookup: true,
  });

  const handleSearch = async (location: string) => {
    try {
      setIsLoading(true);
      setError(null);
      setSearchResults(null);

      const resp = await fetch(`/api/enhanced/burn_restrictions?location=${encodeURIComponent(location)}`);
      const json = await resp.json();

      if (!resp.ok || json.error) {
        throw new Error(json.error || `Request failed with status ${resp.status}`);
      }

      const uiData = mapApiToUICard(json);
      setSearchResults(uiData);
    } catch (e) {
      console.error('Search failed', e);
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setSearchResults(null);
    setSearchValue('');
  };

  const handleLocationRequest = async () => {
    setHasRequestedLocation(true);
    await requestLocation();
  };

  const handleDismissLocation = () => {
    setShowLocationPermission(false);
    setHasRequestedLocation(true);
  };

  // Auto-search when coordinates are obtained
  useEffect(() => {
    if (coordinates && !searchResults && !isLoading) {
      // Use address if available, otherwise use coordinates
      const locationString = locationAddress || `${coordinates.latitude}, ${coordinates.longitude}`;
      setSearchValue(locationString);
      handleSearch(locationString);
    }
  }, [coordinates, locationAddress, searchResults, isLoading]);

  // Show location permission card on app load (only once)
  useEffect(() => {
    if (!hasRequestedLocation && permission === 'unknown') {
      const timer = setTimeout(() => {
        setShowLocationPermission(true);
      }, 1000); // Show after 1 second delay for better UX
      
      return () => clearTimeout(timer);
    }
  }, [hasRequestedLocation, permission]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 p-4">
      {/* Background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-orange-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-red-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-yellow-500/5 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          className="text-center mb-12 pt-8"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <motion.h1
            className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-orange-400 via-red-500 to-yellow-500 bg-clip-text text-transparent mb-4"
            animate={{
              backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: "linear"
            }}
            style={{
              backgroundSize: "200% 200%",
            }}
          >
            Can I Burn?
          </motion.h1>
          
        </motion.div>

        {/* Location Permission Card */}
        <AnimatePresence>
          {showLocationPermission && !hasRequestedLocation && (
            <LocationPermissionCard
              onRequestLocation={handleLocationRequest}
              onDismiss={handleDismissLocation}
              isLoading={isLocationLoading}
              error={locationError}
            />
          )}
        </AnimatePresence>

        {/* Search Interface */}
        <div className="mb-12">
          <div className="max-w-md mx-auto">
            <AnimatedSearchInput
              placeholder="Enter city, address, or coordinates"
              value={searchValue}
              onChange={setSearchValue}
              onSubmit={handleSearch}
              isLoading={isLoading}
              icon={
                <svg 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2"
                  className="w-6 h-6"
                >
                  <circle cx="11" cy="11" r="8"/>
                  <path d="m21 21-4.35-4.35"/>
                </svg>
              }
            />
            
            {/* Location Button */}
            {!coordinates && !isLocationLoading && (
              <div className="mt-4 text-center">
                <button
                  onClick={handleLocationRequest}
                  className="inline-flex items-center gap-2 px-4 py-2 text-sm text-gray-300 hover:text-white transition-colors duration-200 border border-gray-600 hover:border-gray-400 rounded-lg"
                >
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
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Loading State */}
        <AnimatePresence>
          {isLoading && (
            <motion.div
              className="flex justify-center mb-8"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.3 }}
            >
              <SophisticatedLoader
                variant="fire"
                size="lg"
                message="Checking fire restrictions..."
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error */}
        <AnimatePresence>
          {error && !isLoading && (
            <motion.div
              className="mb-8 max-w-xl mx-auto text-center text-red-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {searchResults && !isLoading && (
            <motion.div
              className="mb-8 space-y-6"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.5 }}
            >
              <GlassMorphismCard
                data={searchResults}
                onClose={clearResults}
              />
              
              {/* Enhanced Report - only show if there's meaningful data */}
              {searchResults.burn_restriction.enhanced_report && 
               (searchResults.burn_restriction.enhanced_report.county_conditions || 
                searchResults.burn_restriction.enhanced_report.zone || 
                (searchResults.burn_restriction.enhanced_report.sources && searchResults.burn_restriction.enhanced_report.sources.length > 0)) && (
                <EnhancedReportCard 
                  data={searchResults.burn_restriction.enhanced_report}
                />
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <motion.footer
          className="text-center mt-16 pb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.8 }}
        >
          <p className="text-gray-500 text-sm">
            Built with ❤️ by SZSN Labs
          </p>
        </motion.footer>
      </div>
    </div>
  );
};
