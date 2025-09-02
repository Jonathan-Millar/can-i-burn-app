from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Initialize Nominatim geocoder with longer timeout
geolocator = Nominatim(user_agent="fire_watch_app", timeout=10)
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def normalize_county_name(county_name, province_code):
    """
    Normalize county names to match expected formats for each province.
    """
    if not county_name:
        return None
    
    # Remove common suffixes and clean up
    county_name = county_name.replace('County', '').replace('Regional Municipality', '').strip()
    
    # Province-specific normalization
    if province_code == 'PEI':
        # PEI has Prince, Queens, Kings counties
        if 'Prince' in county_name or 'Summerside' in county_name:
            return 'PRINCE'
        elif 'Queens' in county_name or 'Charlottetown' in county_name:
            return 'QUEENS'
        elif 'Kings' in county_name:
            return 'KINGS'
    elif province_code == 'NB':
        # New Brunswick counties - return as-is after cleaning
        return county_name.title()
    elif province_code == 'NS':
        # Nova Scotia counties - return as-is after cleaning
        return county_name.title()
    elif province_code == 'ON':
        # Ontario counties/regions - return as-is after cleaning
        return county_name.title()
    elif province_code == 'BC':
        # British Columbia regions - return as-is after cleaning
        return county_name.title()
    elif province_code == 'AB':
        # Alberta regions - return as-is after cleaning
        return county_name.title()
    elif province_code == 'SK':
        # Saskatchewan municipalities - return as-is after cleaning
        return county_name.title()
    elif province_code == 'MB':
        # Manitoba municipalities - return as-is after cleaning
        return county_name.title()
    elif province_code == 'QC':
        # Quebec regions - return as-is after cleaning
        return county_name.title()
    elif province_code == 'NL':
        # Newfoundland and Labrador regions - return as-is after cleaning
        return county_name.title()
    elif province_code in ['YT', 'NT', 'NU']:
        # Territories - return as-is after cleaning
        return county_name.title()
    
    return county_name

def detect_province_and_county(latitude, longitude, max_retries=3):
    """
    Determine which province and county/region contains the given coordinates using Nominatim.
    Returns a tuple of (province_code, county_name) or (None, None) if not found.
    """
    for attempt in range(max_retries):
        try:
            location = geocode((latitude, longitude), addressdetails=True, language='en')
            if location and location.raw and 'address' in location.raw:
                address = location.raw['address']
                
                province_full_name = address.get('state')
                county_name = address.get('county') or \
                              address.get('state_district') or \
                              address.get('suburb') or \
                              address.get('city_district') or \
                              address.get('city')
                
                province_code = None
                if province_full_name == 'Prince Edward Island':
                    province_code = 'PEI'
                elif province_full_name == 'New Brunswick':
                    province_code = 'NB'
                elif province_full_name == 'Nova Scotia':
                    province_code = 'NS'
                elif province_full_name == 'Ontario':
                    province_code = 'ON'
                elif province_full_name == 'British Columbia':
                    province_code = 'BC'
                elif province_full_name == 'Alberta':
                    province_code = 'AB'
                elif province_full_name == 'Saskatchewan':
                    province_code = 'SK'
                elif province_full_name == 'Manitoba':
                    province_code = 'MB'
                elif province_full_name == 'Quebec' or province_full_name == 'Québec':
                    province_code = 'QC'
                elif province_full_name == 'Newfoundland and Labrador':
                    province_code = 'NL'
                elif province_full_name == 'Yukon' or province_full_name == 'Yukon Territory':
                    province_code = 'YT'
                elif province_full_name == 'Northwest Territories':
                    province_code = 'NT'
                elif province_full_name == 'Nunavut':
                    province_code = 'NU'
                
                if province_code:
                    normalized_county = normalize_county_name(county_name, province_code)
                    return (province_code, normalized_county)

        except Exception as e:
            print(f"Error during Nominatim reverse geocoding (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Failed to geocode coordinates after {max_retries} attempts")
            
    return (None, None)


