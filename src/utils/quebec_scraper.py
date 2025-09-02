"""
Quebec Fire Restriction Scraper

Scrapes fire restriction data from SOPFEU (Société de protection des forêts contre le feu).
Quebec has a sophisticated zone-based system with fire danger index ratings.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def determine_quebec_region_from_location(latitude, longitude, location_name=None):
    """
    Determine Quebec region/zone based on coordinates or location name.
    This is a simplified mapping - in production, would use official SOPFEU zone boundaries.
    """
    try:
        # Simplified geographic mapping for Quebec regions
        # Montreal area
        if 45.3 <= latitude <= 45.7 and -74.0 <= longitude <= -73.3:
            return 'Montreal'
        
        # Quebec City area
        if 46.6 <= latitude <= 47.0 and -71.5 <= longitude <= -71.0:
            return 'Quebec City'
        
        # Gatineau area (Ottawa region)
        if 45.3 <= latitude <= 45.6 and -76.0 <= longitude <= -75.5:
            return 'Gatineau'
        
        # Sherbrooke area (Eastern Townships)
        if 45.2 <= latitude <= 45.6 and -72.2 <= longitude <= -71.7:
            return 'Sherbrooke'
        
        # Trois-Rivières area
        if 46.2 <= latitude <= 46.5 and -72.8 <= longitude <= -72.3:
            return 'Trois-Rivières'
        
        # Saguenay area
        if 48.2 <= latitude <= 48.6 and -71.3 <= longitude <= -70.8:
            return 'Saguenay'
        
        # Rimouski area (Bas-Saint-Laurent)
        if 48.3 <= latitude <= 48.6 and -68.7 <= longitude <= -68.3:
            return 'Rimouski'
        
        # Val-d'Or area (Abitibi)
        if 48.0 <= latitude <= 48.3 and -77.9 <= longitude <= -77.6:
            return 'Val-d\'Or'
        
        # Determine zone type based on latitude
        if latitude >= 55.0:
            zone_type = 'Nordic Area'
        elif latitude >= 48.0:
            zone_type = 'Northern Intensive Protection Zone'
        else:
            zone_type = 'Southern Intensive Protection Zone'
        
        # Default based on location name if available
        if location_name:
            location_lower = location_name.lower()
            if any(city in location_lower for city in ['montreal', 'montréal']):
                return 'Montreal'
            elif any(city in location_lower for city in ['quebec', 'québec']):
                return 'Quebec City'
            elif any(city in location_lower for city in ['gatineau']):
                return 'Gatineau'
            elif any(city in location_lower for city in ['sherbrooke']):
                return 'Sherbrooke'
            elif any(city in location_lower for city in ['trois-rivières', 'trois-rivieres']):
                return 'Trois-Rivières'
            elif any(city in location_lower for city in ['saguenay']):
                return 'Saguenay'
            elif any(city in location_lower for city in ['rimouski']):
                return 'Rimouski'
            elif any(city in location_lower for city in ['val-d\'or', 'val-dor']):
                return 'Val-d\'Or'
        
        # Default to zone type if specific city not identified
        return zone_type
        
    except Exception as e:
        logger.error(f"Error determining Quebec region: {e}")
        return 'Central Quebec'

def scrape_quebec_fire_restrictions():
    """
    Scrape current fire restrictions from SOPFEU website.
    """
    try:
        url = "https://www.sopfeu.qc.ca/en/current-situation/"
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
        
        # Look for fire restriction information
        restrictions = {
            'provincial_status': 'Unknown',
            'active_fires': 0,
            'total_fires': 0,
            'current_restrictions': False,
            'fire_season_status': 'Unknown',
            'description': 'Unable to determine current restrictions',
            'last_updated': None
        }
        
        # Look for provincial status information
        page_text = soup.get_text().lower()
        
        # Check for fire season status
        if 'transition to fall' in page_text:
            restrictions['fire_season_status'] = 'Transition to Fall'
            restrictions['provincial_status'] = 'Low Fire Activity'
            restrictions['description'] = 'Fire season winding down. Autumn conditions reducing fire risk.'
        elif 'fire season' in page_text and 'active' in page_text:
            restrictions['fire_season_status'] = 'Active Fire Season'
            restrictions['provincial_status'] = 'Active Fire Season'
            restrictions['description'] = 'Active fire season. Check local fire danger index and restrictions.'
        elif 'demobilization' in page_text:
            restrictions['fire_season_status'] = 'Season Ending'
            restrictions['provincial_status'] = 'Season Ending'
            restrictions['description'] = 'Fire season ending. Crews being demobilized.'
        else:
            restrictions['provincial_status'] = 'Normal Conditions'
            restrictions['description'] = 'Normal fire management conditions. Check local fire danger index.'
        
        # Look for restriction information
        if 'no restrictions' in page_text and 'currently' in page_text:
            restrictions['current_restrictions'] = False
        elif 'restriction' in page_text and ('effect' in page_text or 'active' in page_text):
            restrictions['current_restrictions'] = True
            restrictions['description'] = 'Fire restrictions may be in effect in some areas. Check local fire danger index.'
        
        # Try to extract fire statistics
        try:
            # Look for active fires count
            if 'active fires' in page_text:
                import re
                active_match = re.search(r'(\d+)\s+active\s+fires?', page_text)
                if active_match:
                    restrictions['active_fires'] = int(active_match.group(1))
        except:
            pass
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping Quebec fire restrictions: {e}")
        return {
            'provincial_status': 'Unknown',
            'active_fires': 0,
            'total_fires': 0,
            'current_restrictions': False,
            'fire_season_status': 'Unknown',
            'description': f'Unable to retrieve fire restriction data. Error: {str(e)}',
            'last_updated': None,
            'error': str(e)
        }

def get_quebec_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for Quebec coordinates.
    """
    try:
        # Determine Quebec region
        region = determine_quebec_region_from_location(latitude, longitude, location_name)
        
        # Get current restrictions
        restrictions = scrape_quebec_fire_restrictions()
        
        # Determine overall status
        provincial_status = restrictions.get('provincial_status', 'Unknown')
        current_restrictions = restrictions.get('current_restrictions', False)
        fire_season_status = restrictions.get('fire_season_status', 'Unknown')
        active_fires = restrictions.get('active_fires', 0)
        
        if fire_season_status == 'Transition to Fall':
            overall_status = 'Low Fire Risk'
            details = f"Located in {region}, Quebec. Fire season transitioning to fall with reduced fire risk. Check SOPFEU fire danger index for current conditions in your area."
        elif current_restrictions:
            overall_status = 'Fire Restrictions Possible'
            details = f"Located in {region}, Quebec. Fire restrictions may be in effect. Check SOPFEU fire danger index and local restrictions for your specific area."
        elif fire_season_status == 'Active Fire Season':
            overall_status = 'Active Fire Season'
            details = f"Located in {region}, Quebec. Active fire season conditions. Check SOPFEU fire danger index daily for current restrictions in your area."
        elif provincial_status == 'Low Fire Activity':
            overall_status = 'Low Fire Activity'
            details = f"Located in {region}, Quebec. Low fire activity period. Check SOPFEU fire danger index for current conditions."
        else:
            overall_status = 'Check SOPFEU'
            details = f"Located in {region}, Quebec. Check SOPFEU website for current fire danger index and any restrictions in your area."
        
        # Add active fire information if available
        if active_fires > 0:
            details += f" Currently {active_fires} active fires in Quebec."
        
        return {
            'status': overall_status,
            'details': details,
            'source': 'SOPFEU',
            'last_updated': datetime.now().isoformat(),
            'region': region,
            'provincial_status': provincial_status,
            'fire_season_status': fire_season_status,
            'current_restrictions_possible': current_restrictions,
            'active_fires': active_fires,
            'fire_danger_system': '5-level index (Low, Moderate, High, Very High, Extreme)',
            'jurisdiction_info': {
                'intensive_protection_zone': 'Full fire suppression coverage (southern Quebec)',
                'nordic_area': 'Limited protection (northern Quebec)',
                'sopfeu_authority': 'Wildfire prevention and suppression',
                'municipal_coordination': 'Local fire departments coordinate with SOPFEU'
            },
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{region}, Quebec",
            'website': 'https://www.sopfeu.qc.ca/en/',
            'interactive_map': 'https://www.sopfeu.qc.ca/en/map/',
            'current_situation': 'https://www.sopfeu.qc.ca/en/current-situation/',
            'fire_danger_index': 'Check SOPFEU map for daily fire danger index in your area'
        }
        
    except Exception as e:
        logger.error(f"Error getting Quebec fire restrictions: {e}")
        return {
            'status': 'Check SOPFEU',
            'details': f'Located in Quebec. Visit SOPFEU website for current fire danger index and restrictions. Error: {str(e)}',
            'source': 'SOPFEU',
            'last_updated': datetime.now().isoformat(),
            'region': 'Unknown',
            'latitude': latitude,
            'longitude': longitude,
            'website': 'https://www.sopfeu.qc.ca/en/',
            'interactive_map': 'https://www.sopfeu.qc.ca/en/map/',
            'error': str(e)
        }

if __name__ == "__main__":
    # Test with Montreal coordinates
    print("Testing Quebec scraper with Montreal coordinates:")
    result = get_quebec_fire_restrictions(45.5017, -73.5673, "Montreal")
    import json
    print(json.dumps(result, indent=2))

