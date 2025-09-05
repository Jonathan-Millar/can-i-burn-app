import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Heart, MapPin, Search, Flame, AlertTriangle, CheckCircle, Ban, HelpCircle } from 'lucide-react';
import { PlaceholdersAndVanishInput } from './ui/placeholders-and-vanish-input';
import { LoaderFour } from './ui/loader';
import { GlassMorphismCard } from './ui/GlassMorphismCard';
import { EnhancedReportCard } from './ui/EnhancedReportCard';
import { LocationPermissionCard } from './ui/LocationPermissionCard';
import { HeroHighlight, Highlight } from './ui/hero-highlight';
import { BackgroundBeams } from './ui/background-beams';
import { Button } from './ui/button';
import { TextGenerateEffect } from './ui/text-generate-effect';
import { SparklesCore } from './ui/sparkles';
import { AnimatedCard } from './ui/AnimatedCard';
import { EnhancedLoader } from './ui/EnhancedLoader';
import { FloatingActionButton } from './ui/FloatingActionButton';
import { TextRevealEffect, CharacterRevealEffect } from './ui/TextRevealEffect';
import SplitText from './ui/SplitText';
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
  const [locationTimeout, setLocationTimeout] = useState<NodeJS.Timeout | null>(null);

  const {
    coordinates,
    error: locationError,
    isLoading: isLocationLoading,
    permission,
    requestLocation,
    requestLocationIfGranted,
    address: locationAddress,
    hasRequestedBefore,
  } = useGeolocation({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 300000, // 5 minutes
    fallbackToIP: true,
    addressLookup: true,
  });

  const handleSearch = useCallback(async (location: string, coords?: {latitude: number, longitude: number}) => {
    try {
      setIsLoading(true);
      setError(null);
      setSearchResults(null);

      // Use coordinates directly if available, otherwise use location string
      const url = coords 
        ? `/api/enhanced/burn_restrictions?latitude=${coords.latitude}&longitude=${coords.longitude}`
        : `/api/enhanced/burn_restrictions?location=${encodeURIComponent(location)}`;
      
      const resp = await fetch(url);
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
  }, []);

  const clearResults = () => {
    setSearchResults(null);
    setSearchValue('');
  };

  const handleLocationRequest = async () => {
    setHasRequestedLocation(true);
    
    // Set a timeout to prevent infinite loading
    const timeout = setTimeout(() => {
      setError('Location request timed out. Please try again or search manually.');
    }, 15000); // 15 second timeout
    
    setLocationTimeout(timeout);
    
    try {
      await requestLocation();
    } finally {
      // Clear timeout if location request completes
      if (locationTimeout) {
        clearTimeout(locationTimeout);
        setLocationTimeout(null);
      }
    }
  };

  const handleDismissLocation = () => {
    setShowLocationPermission(false);
    setHasRequestedLocation(true);
  };

  // Auto-search when coordinates are obtained
  useEffect(() => {
    if (coordinates && !searchResults && !isLoading) {
      console.log('FireRestrictionApp: Got coordinates, starting auto-search...', coordinates);
      // Clear any previous errors when we get coordinates
      setError(null);
      // Use address if available, otherwise use coordinates
      const locationString = locationAddress || `${coordinates.latitude}, ${coordinates.longitude}`;
      setSearchValue(locationString);
      handleSearch(locationString, coordinates);
    }
  }, [coordinates, locationAddress, searchResults, isLoading, handleSearch]);

  // Auto-request location if permission was previously granted (seamless flow)
  useEffect(() => {
    if (permission === 'granted' && !coordinates && !isLocationLoading && !hasRequestedLocation) {
      // Automatically request location for users who previously granted permission
      console.log('Auto-requesting location for granted permission');
      requestLocationIfGranted();
    }
  }, [permission, coordinates, isLocationLoading, hasRequestedLocation, requestLocationIfGranted]);

  // Show location permission card only for first-time users or when permission is denied
  useEffect(() => {
    // Only show permission card if:
    // 1. User hasn't requested location before AND
    // 2. Permission is unknown/prompt (first time) OR permission is denied (user previously denied)
    // 3. User hasn't manually dismissed it
    if (!hasRequestedLocation && !hasRequestedBefore && (permission === 'unknown' || permission === 'prompt' || permission === 'denied')) {
      const timer = setTimeout(() => {
        setShowLocationPermission(true);
      }, 1000); // Show after 1 second delay for better UX
      
      return () => clearTimeout(timer);
    }
  }, [hasRequestedLocation, hasRequestedBefore, permission]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (locationTimeout) {
        clearTimeout(locationTimeout);
      }
    };
  }, [locationTimeout]);

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Image */}
      <div 
        className="fixed inset-0 bg-cover bg-center bg-no-repeat bg-fixed"
        style={{
          backgroundImage: 'url(/images/background.png)',
          height: '100vh',
          width: '100vw',
          objectFit: 'cover'
        }}
      />
      
      {/* Overlay for better text readability */}
      <div className="fixed inset-0 bg-black/40" />
      
      <div className="relative z-20 max-w-4xl mx-auto p-4 min-h-screen flex flex-col">
        {/* Header */}
        <motion.div
          className="text-center mb-8 pt-8"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <motion.div
            className="flex items-center justify-center mb-6"
          >
            <motion.div
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
            >
              <Flame className="w-12 h-12 text-orange-500 mr-4" />
            </motion.div>
            <SplitText
              text="Can I Burn?"
              className="text-5xl md:text-6xl font-bold text-white font-holtwood"
              delay={100}
              duration={0.6}
              ease="power3.out"
              splitType="chars"
              from={{ opacity: 0, y: 40 }}
              to={{ opacity: 1, y: 0 }}
              threshold={0.1}
              rootMargin="-100px"
              textAlign="center"
              tag="h1"
            />
          </motion.div>
        </motion.div>

        {/* Location Permission Card */}
        <AnimatePresence>
          {showLocationPermission && !hasRequestedLocation && (
            <LocationPermissionCard
              onRequestLocation={handleLocationRequest}
              onDismiss={handleDismissLocation}
              isLoading={isLocationLoading}
              error={locationError}
              permission={permission}
            />
          )}
        </AnimatePresence>

        {/* Main Content Area - grows to fill space */}
        <div className="flex-1 flex flex-col justify-center">
          {/* Loading State */}
          <AnimatePresence>
            {isLoading && (
              <motion.div
                className="flex flex-col items-center justify-center mb-8 space-y-4"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.3 }}
              >
                <EnhancedLoader 
                  text="Checking Fire Restrictions..." 
                  variant="fire"
                  size="lg"
                />
                <motion.p 
                  className="text-gray-400 text-sm"
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  Searching official sources
                </motion.p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error */}
          <AnimatePresence>
            {(error || locationError) && !isLoading && (
              <motion.div
                className="mb-8 max-w-xl mx-auto text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
              >
                <div className="bg-red-500/10 backdrop-blur-sm border border-red-500/20 rounded-xl p-6">
                  <div className="flex items-center justify-center mb-2">
                    <svg className="w-6 h-6 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 className="text-red-400 font-semibold">
                      {locationError ? 'Location Error' : 'Search Error'}
                    </h3>
                  </div>
                  <TextGenerateEffect 
                    words={locationError || error || 'An unexpected error occurred'} 
                    className="text-red-300 text-sm"
                    duration={0.3}
                  />
                  {locationError && (
                    <div className="mt-3 text-xs text-gray-400">
                      <p>You can still search for a location manually using the search bar below.</p>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence mode="wait">
            {searchResults && !isLoading && (
              <motion.div
                className="mb-8 space-y-6"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.6, ease: "easeOut" }}
              >
                <AnimatedCard intensity={0.3} scale={1.02}>
                  <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                  >
                    <GlassMorphismCard
                      data={searchResults}
                      onClose={clearResults}
                    />
                  </motion.div>
                </AnimatedCard>
                
                {/* Enhanced Report - only show if there's meaningful data */}
                {searchResults.burn_restriction.enhanced_report && 
                 (searchResults.burn_restriction.enhanced_report.county_conditions || 
                  searchResults.burn_restriction.enhanced_report.zone || 
                  (searchResults.burn_restriction.enhanced_report.sources && searchResults.burn_restriction.enhanced_report.sources.length > 0)) && (
                  <AnimatedCard intensity={0.2} scale={1.01}>
                    <motion.div
                      initial={{ opacity: 0, y: 30 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3 }}
                    >
                      <EnhancedReportCard 
                        data={searchResults.burn_restriction.enhanced_report}
                      />
                    </motion.div>
                  </AnimatedCard>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
{/* Location Button */}
{!coordinates && !isLocationLoading && (
              <div className="mb-6 text-center">
                <div className="flex justify-center">
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    animate={{ opacity: [1, 0.3, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="relative group"
                  >
                    <Button
                      onClick={handleLocationRequest}
                      variant="outline"
                      size="sm"
                      className="inline-flex items-center gap-2 bg-black/60 backdrop-blur-sm border-white/30 text-white hover:bg-white/20 hover:border-white/50 transition-all duration-300 shadow-lg"
                    >
                      <MapPin className="w-4 h-4" />
                      Use My Location
                    </Button>
                    
                    {/* Custom tooltip */}
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.8 }}
                      whileHover={{ opacity: 1, y: 0, scale: 1 }}
                      className="absolute -top-12 left-1/2 transform -translate-x-1/2 bg-black/80 text-white text-xs px-3 py-2 rounded-lg whitespace-nowrap pointer-events-none z-50"
                    >
                      Get your current location for instant fire restriction info
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-black/80" />
                    </motion.div>
                  </motion.div>
                </div>
              </div>
            )}
        {/* Search Interface - Fixed at bottom */}
        <div className="mb-4">
          <div className="max-w-xl mx-auto">
            <PlaceholdersAndVanishInput
              placeholders={[
                "Check Calgary fire restrictions",
                "Search Banff National Park rules",
                "Enter Vancouver, BC coordinates",
                "Find Algonquin Park burn status",
                "Jasper campfire regulations",
                "Check Tofino fire conditions",
                "Search Whistler area restrictions",
                "Find Cottage Country burn bans"
              ]}
              onChange={(e) => setSearchValue(e.target.value)}
              onSubmit={(e) => {
                e.preventDefault();
                if (searchValue.trim()) {
                  handleSearch(searchValue.trim());
                }
              }}
            />
            
            
          </div>
        </div>

        {/* Footer */}
        <motion.footer
          className="text-center pb-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.8 }}
        >
          <motion.div
            className="flex items-center justify-center gap-2"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <p className="text-gray-500 text-sm flex items-center gap-2">
              Built with 
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: 3 }}
              >
                <Heart className="w-4 h-4 text-red-500" fill="currentColor" />
              </motion.div>
              by SZSN Labs
            </p>
          </motion.div>
        </motion.footer>
      </div>
    </div>
  );
};
