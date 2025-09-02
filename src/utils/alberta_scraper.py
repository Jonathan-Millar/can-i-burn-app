"""
Alberta Fire Restriction Scraper

Scrapes fire restriction data from Alberta Wildfire.
Alberta uses a tiered fire ban system with 5 levels of restrictions.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alberta Fire Restriction Levels
ALBERTA_RESTRICTION_LEVELS = {
    'fire_advisory': {
        'level': 1,
        'description': 'Fire danger increased, permits may be restricted',
        'public_campfires': True,
        'campground_fires': True,
        'private_fires': True,
        'backyard_pits': True,
        'charcoal_bbq': True
    },
    'fire_restriction': {
        'level': 2,
        'description': 'Wood campfires prohibited on public land only',
        'public_campfires': False,
        'campground_fires': True,
        'private_fires': True,
        'backyard_pits': True,
        'charcoal_bbq': True
    },
    'fire_ban': {
        'level': 3,
        'description': 'All wood fires prohibited (public + private land)',
        'public_campfires': False,
        'campground_fires': False,
        'private_fires': False,
        'backyard_pits': False,
        'charcoal_bbq': False
    },
    'ohv_restriction': {
        'level': 4,
        'description': 'Off-highway vehicle use prohibited',
        'additional_restrictions': True
    },
    'forest_closure': {
        'level': 5,
        'description': 'Extreme danger, forest access closed',
        'forest_access': False
    }
}

def determine_alberta_region_from_location(latitude, longitude, location_name=None):
    """
    Determine Alberta region based on coordinates or location name.
    This is a simplified mapping - in production, would use official Alberta boundaries.
    """
    try:
        # Simplified geographic mapping for Alberta regions
        # Calgary area
        if 50.8 <= latitude <= 51.2 and -114.5 <= longitude <= -113.8:
            return 'Calgary Region'
        
        # Edmonton area
        if 53.3 <= latitude <= 53.8 and -113.8 <= longitude <= -113.2:
            return 'Edmonton Region'
        
        # Fort McMurray area (oil sands)
        if 56.5 <= latitude <= 57.0 and -111.5 <= longitude <= -110.5:
            return 'Fort McMurray Region'
        
        # Lethbridge area
        if 49.5 <= latitude <= 50.0 and -113.0 <= longitude <= -112.5:
            return 'Lethbridge Region'
        
        # Red Deer area
        if 52.0 <= latitude <= 52.5 and -114.0 <= longitude <= -113.5:
            return 'Red Deer Region'
        
        # Grande Prairie area
        if 55.0 <= latitude <= 55.5 and -119.0 <= longitude <= -118.5:
            return 'Grande Prairie Region'
        
        # Default based on location name if available
        if location_name:
            location_lower = location_name.lower()
            if any(city in location_lower for city in ['calgary', 'airdrie', 'cochrane']):
                return 'Calgary Region'
            elif any(city in location_lower for city in ['edmonton', 'sherwood park', 'st. albert']):
                return 'Edmonton Region'
            elif any(city in location_lower for city in ['fort mcmurray', 'fort mac']):
                return 'Fort McMurray Region'
            elif any(city in location_lower for city in ['lethbridge', 'medicine hat']):
                return 'Lethbridge Region'
            elif any(city in location_lower for city in ['red deer', 'lacombe']):
                return 'Red Deer Region'
            elif any(city in location_lower for city in ['grande prairie', 'peace river']):
                return 'Grande Prairie Region'
        
        # Default to Central Alberta
        return 'Central Alberta'
        
    except Exception as e:
        logger.error(f"Error determining Alberta region: {e}")
        return 'Central Alberta'

def scrape_alberta_fire_restrictions():
    """
    Scrape current fire restrictions from Alberta government website.
    """
    try:
        url = "https://www.alberta.ca/fire-bans"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for active fire ban information
        restrictions = {
            'current_level': 'Unknown',
            'description': 'Unable to determine current restrictions',
            'public_campfires': None,
            'campground_fires': None,
            'private_fires': None,
            'backyard_pits': None,
            'charcoal_bbq': None,
            'last_updated': None
        }
        
        # Look for active fire ban section
        active_section = soup.find(string=lambda x: x and 'active fire' in x.lower() if x else False)
        if active_section:
            # Try to determine current restriction level from page content
            page_text = soup.get_text().lower()
            
            if 'fire ban' in page_text and 'prohibited' in page_text:
                restrictions['current_level'] = 'Fire Ban'
                restrictions['description'] = 'Fire ban in effect - all wood fires prohibited'
                restrictions.update(ALBERTA_RESTRICTION_LEVELS['fire_ban'])
            elif 'fire restriction' in page_text:
                restrictions['current_level'] = 'Fire Restriction'
                restrictions['description'] = 'Fire restriction in effect - public land campfires prohibited'
                restrictions.update(ALBERTA_RESTRICTION_LEVELS['fire_restriction'])
            elif 'fire advisory' in page_text:
                restrictions['current_level'] = 'Fire Advisory'
                restrictions['description'] = 'Fire advisory in effect - increased fire danger'
                restrictions.update(ALBERTA_RESTRICTION_LEVELS['fire_advisory'])
            else:
                restrictions['current_level'] = 'Normal Conditions'
                restrictions['description'] = 'No province-wide fire restrictions currently in effect'
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping Alberta fire restrictions: {e}")
        return {
            'current_level': 'Unknown',
            'description': f'Unable to retrieve fire restriction data. Error: {str(e)}',
            'public_campfires': None,
            'campground_fires': None,
            'private_fires': None,
            'backyard_pits': None,
            'charcoal_bbq': None,
            'last_updated': None,
            'error': str(e)
        }

def get_alberta_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for Alberta coordinates.
    """
    try:
        # Determine Alberta region
        region = determine_alberta_region_from_location(latitude, longitude, location_name)
        
        # Get current restrictions
        restrictions = scrape_alberta_fire_restrictions()
        
        # Determine overall status
        current_level = restrictions.get('current_level', 'Unknown')
        
        if current_level == 'Fire Ban':
            overall_status = 'All Fires Prohibited'
            details = f"Fire ban in effect in {region}. All wood fires prohibited including campfires, backyard fire pits, and charcoal BBQs. Only propane appliances allowed."
        elif current_level == 'Fire Restriction':
            overall_status = 'Public Land Fire Restriction'
            details = f"Fire restriction in effect in {region}. Wood campfires prohibited on public land. Campground and private property fires still allowed."
        elif current_level == 'Fire Advisory':
            overall_status = 'Fire Advisory'
            details = f"Fire advisory in effect in {region}. Increased fire danger - fire permits may be restricted. Safe campfires allowed."
        elif current_level == 'Normal Conditions':
            overall_status = 'Normal Fire Conditions'
            details = f"No province-wide fire restrictions in {region}. Check local municipal restrictions before lighting fires."
        else:
            overall_status = 'Check Alberta Wildfire'
            details = f"Located in {region}. Visit Alberta Wildfire website for current fire restrictions and local conditions."
        
        return {
            'status': overall_status,
            'details': details,
            'source': 'Alberta Wildfire',
            'last_updated': datetime.now().isoformat(),
            'region': region,
            'restriction_level': current_level,
            'fire_permissions': {
                'public_campfires': restrictions.get('public_campfires'),
                'campground_fires': restrictions.get('campground_fires'),
                'private_fires': restrictions.get('private_fires'),
                'backyard_pits': restrictions.get('backyard_pits'),
                'charcoal_bbq': restrictions.get('charcoal_bbq')
            },
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{region}, Alberta",
            'website': 'https://www.alberta.ca/fire-bans',
            'interactive_map': 'https://www.albertafirebans.ca/'
        }
        
    except Exception as e:
        logger.error(f"Error getting Alberta fire restrictions: {e}")
        return {
            'status': 'Check Alberta Wildfire',
            'details': f'Located in Alberta. Visit Alberta Wildfire website for current fire restrictions. Error: {str(e)}',
            'source': 'Alberta Wildfire',
            'last_updated': datetime.now().isoformat(),
            'region': 'Unknown',
            'latitude': latitude,
            'longitude': longitude,
            'website': 'https://www.alberta.ca/fire-bans',
            'interactive_map': 'https://www.albertafirebans.ca/',
            'error': str(e)
        }

if __name__ == "__main__":
    # Test with Calgary coordinates
    print("Testing Alberta scraper with Calgary coordinates:")
    result = get_alberta_fire_restrictions(51.0447, -114.0719, "Calgary")
    import json
    print(json.dumps(result, indent=2))

