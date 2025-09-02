"""
Canadian Territories Fire Restriction Scraper

Scrapes fire restriction data from Yukon, Northwest Territories, and Nunavut.
Territories have less comprehensive online systems than provinces.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def determine_territory_from_location(latitude, longitude, location_name=None):
    """
    Determine Canadian territory based on coordinates or location name.
    """
    try:
        # Rough territorial boundaries
        # Yukon: West of -124°W, north of 60°N
        # NWT: Between -124°W and -102°W, north of 60°N  
        # Nunavut: East of -102°W, north of 60°N (approximately)
        
        if latitude < 60.0:
            return None  # Not in territories
        
        # Yukon Territory (YT)
        if longitude <= -124.0:
            territory = 'YT'
            
            # Specific Yukon communities
            if 60.6 <= latitude <= 60.8 and -135.2 <= longitude <= -135.0:
                return 'YT', 'Whitehorse'
            elif 64.0 <= latitude <= 64.1 and -139.5 <= longitude <= -139.3:
                return 'YT', 'Dawson City'
            elif 60.0 <= latitude <= 60.1 and -128.9 <= longitude <= -128.7:
                return 'YT', 'Watson Lake'
            elif 60.7 <= latitude <= 60.8 and -137.6 <= longitude <= -137.4:
                return 'YT', 'Haines Junction'
            else:
                return 'YT', 'Yukon Territory'
        
        # Northwest Territories (NT)
        elif -124.0 < longitude <= -102.0:
            territory = 'NT'
            
            # Specific NWT communities
            if 62.4 <= latitude <= 62.5 and -114.5 <= longitude <= -114.2:
                return 'NT', 'Yellowknife'
            elif 60.7 <= latitude <= 60.9 and -116.0 <= longitude <= -115.6:
                return 'NT', 'Hay River'
            elif 59.9 <= latitude <= 60.1 and -112.0 <= longitude <= -111.7:
                return 'NT', 'Fort Smith'
            elif 68.3 <= latitude <= 68.4 and -133.8 <= longitude <= -133.6:
                return 'NT', 'Inuvik'
            elif 65.2 <= latitude <= 65.3 and -126.9 <= longitude <= -126.7:
                return 'NT', 'Norman Wells'
            else:
                return 'NT', 'Northwest Territories'
        
        # Nunavut (NU)
        elif longitude > -102.0:
            territory = 'NU'
            
            # Specific Nunavut communities
            if 63.7 <= latitude <= 63.8 and -68.6 <= longitude <= -68.4:
                return 'NU', 'Iqaluit'
            elif 62.7 <= latitude <= 62.9 and -92.2 <= longitude <= -92.0:
                return 'NU', 'Rankin Inlet'
            elif 69.0 <= latitude <= 69.2 and -105.2 <= longitude <= -105.0:
                return 'NU', 'Cambridge Bay'
            elif 64.2 <= latitude <= 64.4 and -96.2 <= longitude <= -96.0:
                return 'NU', 'Baker Lake'
            else:
                return 'NU', 'Nunavut'
        
        # Check location name if coordinates don't match
        if location_name:
            location_lower = location_name.lower()
            
            # Yukon communities
            if any(city in location_lower for city in ['whitehorse', 'dawson', 'watson lake', 'haines junction']):
                if 'whitehorse' in location_lower:
                    return 'YT', 'Whitehorse'
                elif 'dawson' in location_lower:
                    return 'YT', 'Dawson City'
                elif 'watson' in location_lower:
                    return 'YT', 'Watson Lake'
                elif 'haines' in location_lower:
                    return 'YT', 'Haines Junction'
                else:
                    return 'YT', 'Yukon Territory'
            
            # NWT communities
            elif any(city in location_lower for city in ['yellowknife', 'hay river', 'fort smith', 'inuvik', 'norman wells']):
                if 'yellowknife' in location_lower:
                    return 'NT', 'Yellowknife'
                elif 'hay river' in location_lower:
                    return 'NT', 'Hay River'
                elif 'fort smith' in location_lower:
                    return 'NT', 'Fort Smith'
                elif 'inuvik' in location_lower:
                    return 'NT', 'Inuvik'
                elif 'norman wells' in location_lower:
                    return 'NT', 'Norman Wells'
                else:
                    return 'NT', 'Northwest Territories'
            
            # Nunavut communities
            elif any(city in location_lower for city in ['iqaluit', 'rankin inlet', 'cambridge bay', 'baker lake']):
                if 'iqaluit' in location_lower:
                    return 'NU', 'Iqaluit'
                elif 'rankin' in location_lower:
                    return 'NU', 'Rankin Inlet'
                elif 'cambridge' in location_lower:
                    return 'NU', 'Cambridge Bay'
                elif 'baker' in location_lower:
                    return 'NU', 'Baker Lake'
                else:
                    return 'NU', 'Nunavut'
            
            # Territory names
            elif 'yukon' in location_lower:
                return 'YT', 'Yukon Territory'
            elif any(name in location_lower for name in ['northwest territories', 'nwt', 'nt']):
                return 'NT', 'Northwest Territories'
            elif 'nunavut' in location_lower:
                return 'NU', 'Nunavut'
        
        return None, None
        
    except Exception as e:
        logger.error(f"Error determining territory: {e}")
        return None, None

def scrape_nwt_fire_restrictions():
    """
    Scrape current fire restrictions from NWT government website.
    """
    try:
        # Try to get fire danger information from NWT
        url = "https://www.gov.nt.ca/ecc/en/services/wildfire-prevention-and-safety/fire-danger-and-you"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text().lower()
        
        # Initialize restrictions data
        restrictions = {
            'fire_danger_level': 'Unknown',
            'fire_season_active': False,
            'restrictions_in_place': False,
            'description': 'Check GNWT wildfire updates for current restrictions'
        }
        
        # Check for fire season (May 1 - September 30)
        current_month = datetime.now().month
        if 5 <= current_month <= 9:  # May to September
            restrictions['fire_season_active'] = True
        
        # Look for fire danger levels
        if 'extreme' in page_text and 'fire' in page_text:
            restrictions['fire_danger_level'] = 'Extreme'
            restrictions['restrictions_in_place'] = True
            restrictions['description'] = 'Extreme fire danger. Do not have campfires unless no other choice for food/warmth.'
        elif 'high' in page_text and 'fire' in page_text:
            restrictions['fire_danger_level'] = 'High'
            restrictions['restrictions_in_place'] = True
            restrictions['description'] = 'High fire danger. Do not have fires unless necessary for food/warmth.'
        elif 'moderate' in page_text and 'fire' in page_text:
            restrictions['fire_danger_level'] = 'Moderate'
            restrictions['description'] = 'Moderate fire danger. Take extra caution, keep fires small.'
        elif 'low' in page_text and 'fire' in page_text:
            restrictions['fire_danger_level'] = 'Low'
            restrictions['description'] = 'Low fire danger. Have campfires with regular caution.'
        
        # Check for fire bans
        if any(term in page_text for term in ['fire ban', 'fire restriction', 'burning restriction']):
            restrictions['restrictions_in_place'] = True
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping NWT fire restrictions: {e}")
        return {
            'fire_danger_level': 'Unknown',
            'fire_season_active': False,
            'restrictions_in_place': False,
            'description': f'Unable to retrieve NWT fire restriction data. Check GNWT wildfire updates.',
            'error': str(e)
        }

def scrape_yukon_fire_restrictions():
    """
    Scrape current fire restrictions from Yukon government (limited due to access restrictions).
    """
    try:
        # Yukon website has Cloudflare protection, so provide fallback information
        current_month = datetime.now().month
        fire_season_active = 5 <= current_month <= 9  # Approximate fire season
        
        return {
            'fire_danger_level': 'Check Daily Updates',
            'fire_season_active': fire_season_active,
            'restrictions_in_place': False,
            'description': 'Check Yukon government wildfire updates for current fire danger ratings and restrictions.',
            'note': 'Yukon uses multi-level fire restrictions (Level 1-3). Visit yukon.ca for current status.'
        }
        
    except Exception as e:
        logger.error(f"Error scraping Yukon fire restrictions: {e}")
        return {
            'fire_danger_level': 'Unknown',
            'fire_season_active': False,
            'restrictions_in_place': False,
            'description': 'Unable to retrieve Yukon fire restriction data. Visit yukon.ca for current restrictions.',
            'error': str(e)
        }

def scrape_nunavut_fire_restrictions():
    """
    Scrape current fire restrictions from Nunavut (limited online data available).
    """
    try:
        current_month = datetime.now().month
        fire_season_active = 6 <= current_month <= 9  # Approximate fire season for Arctic
        
        return {
            'fire_danger_level': 'Check Local Authorities',
            'fire_season_active': fire_season_active,
            'restrictions_in_place': False,
            'description': 'Check with local community government for current fire restrictions and burn permit requirements.',
            'note': 'Nunavut fire restrictions are managed at community level. Contact local authorities for current status.'
        }
        
    except Exception as e:
        logger.error(f"Error scraping Nunavut fire restrictions: {e}")
        return {
            'fire_danger_level': 'Unknown',
            'fire_season_active': False,
            'restrictions_in_place': False,
            'description': 'Unable to retrieve Nunavut fire restriction data. Contact local community government.',
            'error': str(e)
        }

def get_territory_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for Canadian territories coordinates.
    """
    try:
        # Determine territory and region
        territory_result = determine_territory_from_location(latitude, longitude, location_name)
        
        if not territory_result or territory_result[0] is None:
            return {
                'status': 'Not in Canadian Territories',
                'details': 'Location is not within Canadian territories (Yukon, Northwest Territories, or Nunavut).',
                'latitude': latitude,
                'longitude': longitude,
                'error': 'Location outside territories'
            }
        
        territory_code, region = territory_result
        
        # Get territory-specific restrictions
        if territory_code == 'NT':
            restrictions = scrape_nwt_fire_restrictions()
            territory_name = 'Northwest Territories'
            website = 'https://www.gov.nt.ca/ecc/'
            fire_season = 'May 1 - September 30'
            agency = 'GNWT Environment and Climate Change'
        elif territory_code == 'YT':
            restrictions = scrape_yukon_fire_restrictions()
            territory_name = 'Yukon Territory'
            website = 'https://yukon.ca/en/emergencies-and-safety/wildfires'
            fire_season = 'May - September (approximate)'
            agency = 'Yukon Wildland Fire Management'
        elif territory_code == 'NU':
            restrictions = scrape_nunavut_fire_restrictions()
            territory_name = 'Nunavut'
            website = 'https://www.gov.nu.ca/'
            fire_season = 'June - September (approximate)'
            agency = 'Nunavut Fire Marshal / Community Governments'
        else:
            return {
                'status': 'Unknown Territory',
                'details': 'Unable to determine territory from coordinates.',
                'latitude': latitude,
                'longitude': longitude,
                'error': 'Territory detection failed'
            }
        
        # Determine overall status
        fire_danger_level = restrictions.get('fire_danger_level', 'Unknown')
        restrictions_in_place = restrictions.get('restrictions_in_place', False)
        fire_season_active = restrictions.get('fire_season_active', False)
        description = restrictions.get('description', 'Check local authorities for current restrictions')
        
        if fire_danger_level == 'Extreme':
            overall_status = 'Extreme Fire Danger'
        elif fire_danger_level == 'High':
            overall_status = 'High Fire Danger'
        elif restrictions_in_place:
            overall_status = 'Fire Restrictions in Place'
        elif fire_season_active:
            overall_status = 'Fire Season Active'
        else:
            overall_status = 'Check Local Restrictions'
        
        details = f"Located in {region}, {territory_name}. {description}"
        
        return {
            'status': overall_status,
            'details': details,
            'source': agency,
            'last_updated': datetime.now().isoformat(),
            'region': region,
            'territory': territory_name,
            'territory_code': territory_code,
            'fire_danger_level': fire_danger_level,
            'restrictions_in_place': restrictions_in_place,
            'fire_season_active': fire_season_active,
            'fire_season_dates': fire_season,
            'website': website,
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{region}, {territory_name}",
            'territory_info': {
                'fire_season': fire_season,
                'management_agency': agency,
                'website': website,
                'data_limitations': 'Territories have limited online fire restriction systems',
                'recommendation': 'Contact local authorities for most current information'
            },
            'current_restrictions': description,
            'additional_info': restrictions.get('note', ''),
            'data_source_note': 'Territory fire restriction data may be limited. Always check with local authorities for most current information.'
        }
        
    except Exception as e:
        logger.error(f"Error getting territory fire restrictions: {e}")
        return {
            'status': 'Check Local Authorities',
            'details': f'Located in Canadian territories. Unable to retrieve detailed fire restriction data. Contact local authorities for current restrictions. Error: {str(e)}',
            'source': 'Canadian Territories',
            'last_updated': datetime.now().isoformat(),
            'latitude': latitude,
            'longitude': longitude,
            'error': str(e),
            'recommendation': 'Contact local territorial or community government for current fire restrictions'
        }

if __name__ == "__main__":
    # Test with territorial capitals
    print("Testing territories scraper:")
    
    # Test Yellowknife, NWT
    print("\n1. Yellowknife, NWT:")
    result = get_territory_fire_restrictions(62.4540, -114.3718, "Yellowknife")
    print(f"Status: {result['status']}")
    print(f"Region: {result.get('region', 'Unknown')}")
    print(f"Fire Danger: {result.get('fire_danger_level', 'Unknown')}")
    
    # Test Whitehorse, YT
    print("\n2. Whitehorse, YT:")
    result = get_territory_fire_restrictions(60.7212, -135.0568, "Whitehorse")
    print(f"Status: {result['status']}")
    print(f"Region: {result.get('region', 'Unknown')}")
    print(f"Territory: {result.get('territory', 'Unknown')}")
    
    # Test Iqaluit, NU
    print("\n3. Iqaluit, NU:")
    result = get_territory_fire_restrictions(63.7467, -68.5170, "Iqaluit")
    print(f"Status: {result['status']}")
    print(f"Region: {result.get('region', 'Unknown')}")
    print(f"Territory: {result.get('territory', 'Unknown')}")

