declare module 'geolocator' {
  interface GeolocatorLocation {
    coords: {
      latitude: number;
      longitude: number;
      accuracy: number;
      altitude?: number;
      altitudeAccuracy?: number;
      heading?: number;
      speed?: number;
    };
    timestamp: number;
    address?: {
      street?: string;
      town?: string;
      region?: string;
      country?: string;
      postalCode?: string;
    };
  }

  interface GeolocatorOptions {
    enableHighAccuracy?: boolean;
    timeout?: number;
    maximumAge?: number;
    fallbackToIP?: boolean;
    addressLookup?: boolean;
  }

  interface GeolocatorError {
    code: number;
    message: string;
  }

  interface Geolocator {
    locate(
      options: GeolocatorOptions,
      callback: (err: GeolocatorError | null, location: GeolocatorLocation) => void
    ): void;
  }

  const geolocator: Geolocator;
  export default geolocator;
}
