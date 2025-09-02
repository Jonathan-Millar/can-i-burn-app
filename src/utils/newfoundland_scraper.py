"""
Newfoundland and Labrador Fire Restriction Scraper

Scrapes fire restriction data from NL Department of Fisheries, Forestry and Agriculture.
NL has a province-wide fire hazard rating system with frequent fire bans.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def determine_nl_region_from_location(latitude, longitude, location_name=None):
    """
    Determine Newfoundland and Labrador region based on coordinates or location name.
    """
    try:
        # Determine if location is in Labrador or Island of Newfoundland
        # Labrador is generally north of 52°N and west of 58°W
        if latitude >= 52.0 and longitude <= -58.0:
            region_type = 'Labrador'
            
            # Specific Labrador communities
            if 53.2 <= latitude <= 53.4 and -60.5 <= longitude <= -60.1:
                return 'Happy Valley-Goose Bay'
            elif 52.8 <= latitude <= 53.1 and -67.1 <= longitude <= -66.8:
                return 'Labrador City'
            elif 51.3 <= latitude <= 51.5 and -57.2 <= longitude <= -56.9:
                return 'Nain'
            else:
                return 'Central Labrador'
        else:
            region_type = 'Island of Newfoundland'
            
            # Specific Newfoundland communities
            # St. John's area
            if 47.4 <= latitude <= 47.7 and -52.9 <= longitude <= -52.5:
                return 'St. John\'s'
            
            # Corner Brook area
            if 48.8 <= latitude <= 49.1 and -58.1 <= longitude <= -57.8:
                return 'Corner Brook'
            
            # Gander area
            if 48.8 <= latitude <= 49.1 and -54.8 <= longitude <= -54.5:
                return 'Gander'
            
            # Grand Falls-Windsor area
            if 48.9 <= latitude <= 49.0 and -55.8 <= longitude <= -55.5:
                return 'Grand Falls-Windsor'
            
            # Clarenville area
            if 48.1 <= latitude <= 48.3 and -53.9 <= longitude <= -53.7:
                return 'Clarenville'
            
            # Determine general region on island
            if latitude >= 49.0:
                return 'Northern Peninsula'
            elif longitude <= -56.0:
                return 'Western Newfoundland'
            elif longitude >= -54.0:
                return 'Eastern Newfoundland'
            else:
                return 'Central Newfoundland'
        
        # Default based on location name if available
        if location_name:
            location_lower = location_name.lower()
            if any(city in location_lower for city in ['st. john\'s', 'st johns', 'saint johns']):
                return 'St. John\'s'
            elif any(city in location_lower for city in ['corner brook']):
                return 'Corner Brook'
            elif any(city in location_lower for city in ['gander']):
                return 'Gander'
            elif any(city in location_lower for city in ['happy valley', 'goose bay']):
                return 'Happy Valley-Goose Bay'
            elif any(city in location_lower for city in ['labrador city']):
                return 'Labrador City'
            elif any(city in location_lower for city in ['grand falls', 'windsor']):
                return 'Grand Falls-Windsor'
            elif any(city in location_lower for city in ['clarenville']):
                return 'Clarenville'
            elif 'labrador' in location_lower:
                return 'Labrador'
        
        return region_type
        
    except Exception as e:
        logger.error(f"Error determining NL region: {e}")
        return 'Newfoundland and Labrador'

def scrape_nl_fire_restrictions():
    """
    Scrape current fire restrictions from NL government website.
    """
    try:
        url = "https://www.gov.nl.ca/ffa/public-education/forestry/forest-fires/fire-hazard-map/"
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
        
        # Initialize restrictions data
        restrictions = {
            'province_wide_ban': False,
            'fire_hazard_level': 'Unknown',
            'ban_until_date': None,
            'description': 'Unable to determine current restrictions',
            'last_updated': None,
            'fire_season_active': False,
            'enhanced_penalties': False
        }
        
        # Look for fire ban information
        page_text = soup.get_text().lower()
        
        # Check for province-wide fire ban
        if 'province-wide fire ban' in page_text and 'in effect' in page_text:
            restrictions['province_wide_ban'] = True
            restrictions['fire_hazard_level'] = 'Extreme'
            restrictions['description'] = 'Province-wide fire ban in effect. All open fires and outdoor burning are banned.'
            
            # Try to extract ban end date
            import re
            date_match = re.search(r'until at least (\w+ \d+)', page_text)
            if date_match:
                restrictions['ban_until_date'] = date_match.group(1)
                restrictions['description'] += f' Ban in place until at least {date_match.group(1)}.'
        
        # Check for fire ban status
        elif 'fire ban in effect' in page_text:
            restrictions['province_wide_ban'] = True
            restrictions['fire_hazard_level'] = 'Very High'
            restrictions['description'] = 'Fire ban in effect. Open fires and outdoor burning are banned.'
        
        # Check for extreme conditions
        elif 'extreme' in page_text and ('fire' in page_text or 'hazard' in page_text):
            restrictions['fire_hazard_level'] = 'Extreme'
            restrictions['description'] = 'Extreme fire hazard conditions. Check current restrictions.'
        
        # Check for very high conditions
        elif 'very high' in page_text and ('fire' in page_text or 'hazard' in page_text):
            restrictions['fire_hazard_level'] = 'Very High'
            restrictions['description'] = 'Very high fire hazard conditions. Extreme caution required.'
        
        # Check for high conditions
        elif 'high' in page_text and ('fire' in page_text or 'hazard' in page_text):
            restrictions['fire_hazard_level'] = 'High'
            restrictions['description'] = 'High fire hazard conditions. Caution required for forested areas.'
        
        # Check for fire season status
        current_month = datetime.now().month
        if 4 <= current_month <= 9:  # April to September
            restrictions['fire_season_active'] = True
        elif current_month == 10:  # October (Labrador only)
            restrictions['fire_season_active'] = True
        
        # Check for enhanced penalties
        if any(penalty in page_text for penalty in ['$50,000', '$150,000', 'prison', 'fine']):
            restrictions['enhanced_penalties'] = True
        
        # Try to extract last updated time
        if 'last updated' in page_text:
            import re
            time_match = re.search(r'last updated:?\s*([^.]+)', page_text)
            if time_match:
                restrictions['last_updated'] = time_match.group(1).strip()
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping NL fire restrictions: {e}")
        return {
            'province_wide_ban': False,
            'fire_hazard_level': 'Unknown',
            'ban_until_date': None,
            'description': f'Unable to retrieve fire restriction data. Error: {str(e)}',
            'last_updated': None,
            'fire_season_active': False,
            'enhanced_penalties': False,
            'error': str(e)
        }

def get_nl_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for Newfoundland and Labrador coordinates.
    """
    try:
        # Determine NL region
        region = determine_nl_region_from_location(latitude, longitude, location_name)
        
        # Get current restrictions
        restrictions = scrape_nl_fire_restrictions()
        
        # Determine overall status
        province_wide_ban = restrictions.get('province_wide_ban', False)
        fire_hazard_level = restrictions.get('fire_hazard_level', 'Unknown')
        ban_until_date = restrictions.get('ban_until_date')
        fire_season_active = restrictions.get('fire_season_active', False)
        enhanced_penalties = restrictions.get('enhanced_penalties', False)
        
        if province_wide_ban:
            overall_status = 'Province-wide Fire Ban'
            details = f"Located in {region}, Newfoundland and Labrador. Province-wide fire ban currently in effect. All open fires and outdoor burning are banned."
            if ban_until_date:
                details += f" Ban in place until at least {ban_until_date}."
        elif fire_hazard_level == 'Extreme':
            overall_status = 'Extreme Fire Hazard'
            details = f"Located in {region}, Newfoundland and Labrador. Extreme fire hazard conditions. Open fires and outdoor burning may be banned."
        elif fire_hazard_level == 'Very High':
            overall_status = 'Very High Fire Hazard'
            details = f"Located in {region}, Newfoundland and Labrador. Very high fire hazard conditions. Extreme caution required for any forested land activities."
        elif fire_hazard_level == 'High':
            overall_status = 'High Fire Hazard'
            details = f"Located in {region}, Newfoundland and Labrador. High fire hazard conditions. Caution required for forested areas."
        elif fire_season_active:
            overall_status = 'Fire Season Active'
            details = f"Located in {region}, Newfoundland and Labrador. Fire season is active. Check daily fire hazard ratings."
        else:
            overall_status = 'Check Daily Hazard'
            details = f"Located in {region}, Newfoundland and Labrador. Check daily fire hazard map for current conditions."
        
        # Add enhanced penalty information
        if enhanced_penalties:
            details += " Enhanced penalties in effect: fines from $50,000 to $150,000 for fire ban violations."
        
        # Determine fire season dates based on region
        if 'labrador' in region.lower():
            fire_season_dates = "May 15 - October 15"
        else:
            fire_season_dates = "April 24 - September 30"
        
        return {
            'status': overall_status,
            'details': details,
            'source': 'NL Fisheries, Forestry and Agriculture',
            'last_updated': datetime.now().isoformat(),
            'region': region,
            'province_wide_ban': province_wide_ban,
            'fire_hazard_level': fire_hazard_level,
            'ban_until_date': ban_until_date,
            'fire_season_active': fire_season_active,
            'fire_season_dates': fire_season_dates,
            'enhanced_penalties': enhanced_penalties,
            'fire_hazard_system': '5-level rating (Low, Moderate, High, Very High, Extreme)',
            'jurisdiction_info': {
                'island_fire_season': 'April 24 - September 30',
                'labrador_fire_season': 'May 15 - October 15',
                'daily_updates': 'Fire hazard map updated daily at 2 PM NDT',
                'province_wide_system': 'Unified fire hazard rating across NL',
                'enhanced_enforcement': 'Fines $50K-$150K, possible imprisonment'
            },
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{region}, Newfoundland and Labrador",
            'website': 'https://www.gov.nl.ca/ffa/public-education/forestry/forest-fires/',
            'fire_hazard_map': 'https://www.gov.nl.ca/ffa/public-education/forestry/forest-fires/fire-hazard-map/',
            'daily_update_time': '2:00 PM NDT',
            'current_restrictions': restrictions.get('description', 'Check fire hazard map for current conditions')
        }
        
    except Exception as e:
        logger.error(f"Error getting NL fire restrictions: {e}")
        return {
            'status': 'Check NL Fire Hazard Map',
            'details': f'Located in Newfoundland and Labrador. Visit NL government fire hazard map for current restrictions. Error: {str(e)}',
            'source': 'NL Fisheries, Forestry and Agriculture',
            'last_updated': datetime.now().isoformat(),
            'region': 'Unknown',
            'latitude': latitude,
            'longitude': longitude,
            'website': 'https://www.gov.nl.ca/ffa/public-education/forestry/forest-fires/',
            'fire_hazard_map': 'https://www.gov.nl.ca/ffa/public-education/forestry/forest-fires/fire-hazard-map/',
            'error': str(e)
        }

if __name__ == "__main__":
    # Test with St. John's coordinates
    print("Testing NL scraper with St. John's coordinates:")
    result = get_nl_fire_restrictions(47.5615, -52.7126, "St. John's")
    import json
    print(json.dumps(result, indent=2))

