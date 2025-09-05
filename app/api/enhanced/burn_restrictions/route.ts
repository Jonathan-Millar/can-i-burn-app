import { NextRequest, NextResponse } from 'next/server';
import { detectProvinceAndCounty } from '@/lib/province_detector';
import { geocodeLocation } from '@/lib/geocoding';
import { scrapeBurnRestrictions } from '@/lib/restrictions_scraper';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const latitude = searchParams.get("latitude");
    const longitude = searchParams.get("longitude");
    const location = searchParams.get("location");

    let lat: number;
    let lon: number;

    // If location name provided, geocode it
    if (location && (!latitude || !longitude)) {
      const coords = await geocodeLocation(location);
      if (!coords) {
        return NextResponse.json(
          {
            error: `Could not find coordinates for location: ${location}`,
          },
          { status: 400 }
        );
      }
      lat = coords.lat;
      lon = coords.lon;
    } else if (latitude && longitude) {
      lat = parseFloat(latitude);
      lon = parseFloat(longitude);
    } else {
      return NextResponse.json(
        { error: "Latitude and longitude are required" },
        { status: 400 }
      );
    }

    // Validate coordinates
    if (isNaN(lat) || isNaN(lon)) {
      return NextResponse.json(
        { error: "Invalid latitude or longitude" },
        { status: 400 }
      );
    }

    // Detect province and county
    const { province, county } = await detectProvinceAndCounty(lat, lon);
    if (!province) {
      return NextResponse.json(
        {
          error:
            "Location is outside supported provinces and territories (PEI, NB, NS, ON, BC, AB, SK, MB, QC, NL, YT, NT, NU)",
        },
        { status: 400 }
      );
    }

    // Get burn restrictions (pass coordinates for location-aware context)
    const restrictions = await scrapeBurnRestrictions(province, county, { latitude: lat, longitude: lon });
    if (!restrictions) {
      return NextResponse.json(
        { error: "Could not fetch burn restrictions" },
        { status: 500 }
      );
    }

    // Prepare response
    const response = {
      latitude: lat,
      longitude: lon,
      province,
      county,
      ...restrictions,
    };

    const nextResponse = NextResponse.json(response);
    // Add cache-busting headers
    nextResponse.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
    nextResponse.headers.set('Pragma', 'no-cache');
    nextResponse.headers.set('Expires', '0');
    return nextResponse;
  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json(
      { error: `Internal server error: ${error instanceof Error ? error.message : 'Unknown error'}` },
      { status: 500 }
    );
  }
}
