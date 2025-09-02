"""
Manitoba Fire Restriction Scraper

Scrapes fire restriction data from Manitoba Wildfire Service.
Manitoba has a dual jurisdiction system with provincial and municipal authorities.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def determine_manitoba_municipality_from_location(latitude, longitude, location_name=None):
    """
    Determine Manitoba municipality based on coordinates or location name.
    This is a simplified mapping - in production, would use official Manitoba boundaries.
    """
    try:
        # Simplified geographic mapping for Manitoba municipalities
        # Winnipeg area (largest city)
        if 49.7 <= latitude <= 50.0 and -97.4 <= longitude <= -96.9:
            return 'Winnipeg'
        
        # Brandon area
        if 49.7 <= latitude <= 49.9 and -100.1 <= longitude <= -99.8:
            return 'Brandon'
        
        # Thompson area (northern)
        if 55.6 <= latitude <= 55.9 and -98.0 <= longitude <= -97.7:
            return 'Thompson'
        
        # Portage la Prairie area
        if 49.8 <= latitude <= 50.1 and -98.4 <= longitude <= -98.1:
            return 'Portage la Prairie'
        
        # Steinbach area
        if 49.4 <= latitude <= 49.6 and -96.8 <= longitude <= -96.6:
            return 'Steinbach'
        
        # Selkirk area
        if 50.1 <= latitude <= 50.2 and -96.9 <= longitude <= -96.8:
            return 'Selkirk'
        
        # Dauphin area
        if 51.1 <= latitude <= 51.2 and -100.1 <= longitude <= -100.0:
            return 'Dauphin'
        
        # Default based on location name if available
        if location_name:
            location_lower = location_name.lower()
            if any(city in location_lower for city in ['winnipeg', 'wpg']):
                return 'Winnipeg'
            elif any(city in location_lower for city in ['brandon']):
                return 'Brandon'
            elif any(city in location_lower for city in ['thompson']):
                return 'Thompson'
            elif any(city in location_lower for city in ['portage la prairie', 'portage']):
                return 'Portage la Prairie'
            elif any(city in location_lower for city in ['steinbach']):
                return 'Steinbach'
            elif any(city in location_lower for city in ['selkirk']):
                return 'Selkirk'
            elif any(city in location_lower for city in ['dauphin']):
                return 'Dauphin'
        
        # Default to Central Manitoba
        return 'Central Manitoba'
        
    except Exception as e:
        logger.error(f"Error determining Manitoba municipality: {e}")
        return 'Central Manitoba'

def is_fire_season():
    """
    Check if current date is within Manitoba's fire season (April 1 - November 15).
    """
    today = date.today()
    current_year = today.year
    
    # Fire season: April 1 to November 15
    fire_season_start = date(current_year, 4, 1)
    fire_season_end = date(current_year, 11, 15)
    
    return fire_season_start <= today <= fire_season_end

def scrape_manitoba_fire_restrictions():
    """
    Scrape current fire restrictions from Manitoba government website.
    """
    try:
        url = "https://www.gov.mb.ca/wildfire/burn_conditions.html"
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
            'seasonal_restriction': is_fire_season(),
            'enhanced_restrictions': False,
            'travel_restrictions': False,
            'description': 'Unable to determine current restrictions',
            'last_updated': None
        }
        
        # Look for provincial fire restriction status
        page_text = soup.get_text().lower()
        
        # Check for enhanced restrictions beyond seasonal
        if 'fire ban' in page_text and ('effect' in page_text or 'active' in page_text):
            restrictions['provincial_status'] = 'Enhanced Fire Ban'
            restrictions['enhanced_restrictions'] = True
            restrictions['description'] = 'Enhanced fire ban in effect beyond seasonal restrictions.'
        elif 'fire restriction' in page_text and ('effect' in page_text or 'active' in page_text):
            restrictions['provincial_status'] = 'Enhanced Fire Restrictions'
            restrictions['enhanced_restrictions'] = True
            restrictions['description'] = 'Enhanced fire restrictions in effect beyond seasonal restrictions.'
        elif 'travel restriction' in page_text:
            restrictions['travel_restrictions'] = True
            restrictions['description'] = 'Travel restrictions may be in effect in some areas.'
        else:
            restrictions['provincial_status'] = 'Seasonal Restrictions Only'
            restrictions['description'] = 'Standard seasonal fire restrictions in effect (April 1 - November 15).'
        
        # Check for travel restrictions
        if 'travel' in page_text and ('restriction' in page_text or 'ban' in page_text):
            restrictions['travel_restrictions'] = True
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping Manitoba fire restrictions: {e}")
        return {
            'provincial_status': 'Unknown',
            'seasonal_restriction': is_fire_season(),
            'enhanced_restrictions': False,
            'travel_restrictions': False,
            'description': f'Unable to retrieve fire restriction data. Error: {str(e)}',
            'last_updated': None,
            'error': str(e)
        }

def get_manitoba_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for Manitoba coordinates.
    """
    try:
        # Determine Manitoba municipality
        municipality = determine_manitoba_municipality_from_location(latitude, longitude, location_name)
        
        # Get current restrictions
        restrictions = scrape_manitoba_fire_restrictions()
        
        # Determine overall status
        seasonal_restriction = restrictions.get('seasonal_restriction', False)
        enhanced_restrictions = restrictions.get('enhanced_restrictions', False)
        travel_restrictions = restrictions.get('travel_restrictions', False)
        provincial_status = restrictions.get('provincial_status', 'Unknown')
        
        if enhanced_restrictions and provincial_status == 'Enhanced Fire Ban':
            overall_status = 'Enhanced Fire Ban'
            details = f"Enhanced fire ban in effect in {municipality}. All open fires prohibited beyond normal seasonal restrictions. Check municipal restrictions for additional local bans."
        elif enhanced_restrictions and provincial_status == 'Enhanced Fire Restrictions':
            overall_status = 'Enhanced Fire Restrictions'
            details = f"Enhanced fire restrictions in effect in {municipality}. Additional restrictions beyond seasonal prohibitions. Check municipal restrictions."
        elif seasonal_restriction:
            overall_status = 'Seasonal Fire Restrictions'
            details = f"Seasonal fire restrictions in effect in {municipality} (April 1 - November 15). Open fires prohibited except under permit or in approved campfire pits. Check municipal restrictions for additional local bans."
        else:
            overall_status = 'Outside Fire Season'
            details = f"Outside main fire season in {municipality}. Check municipal restrictions as local fire bans may still be in effect."
        
        # Add travel restriction info
        if travel_restrictions:
            details += " Travel restrictions may also be in effect in some areas."
        
        return {
            'status': overall_status,
            'details': details,
            'source': 'Manitoba Wildfire Service',
            'last_updated': datetime.now().isoformat(),
            'municipality': municipality,
            'provincial_status': provincial_status,
            'seasonal_restriction_active': seasonal_restriction,
            'enhanced_restrictions': enhanced_restrictions,
            'travel_restrictions': travel_restrictions,
            'fire_season_dates': 'April 1 - November 15',
            'jurisdiction_info': {
                'provincial_authority': 'Manitoba Wildfire Service (Crown land, provincial parks)',
                'municipal_authority': 'Local governments (municipal burning restrictions)',
                'coordination': 'Office of the Fire Commissioner'
            },
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{municipality}, Manitoba",
            'website': 'https://www.gov.mb.ca/wildfire/burn_conditions.html',
            'municipal_map': 'https://www.arcgis.com/apps/mapviewer/index.html?webmap=9acc1c9b1ed14cc5b18e8e03966c5e89',
            'provincial_restrictions': 'https://www.gov.mb.ca/conservation_fire/Restrictions/index.html'
        }
        
    except Exception as e:
        logger.error(f"Error getting Manitoba fire restrictions: {e}")
        return {
            'status': 'Check Manitoba Wildfire Service',
            'details': f'Located in Manitoba. Visit Manitoba Wildfire Service website for current fire restrictions. Error: {str(e)}',
            'source': 'Manitoba Wildfire Service',
            'last_updated': datetime.now().isoformat(),
            'municipality': 'Unknown',
            'seasonal_restriction_active': is_fire_season(),
            'latitude': latitude,
            'longitude': longitude,
            'website': 'https://www.gov.mb.ca/wildfire/burn_conditions.html',
            'municipal_map': 'https://www.arcgis.com/apps/mapviewer/index.html?webmap=9acc1c9b1ed14cc5b18e8e03966c5e89',
            'error': str(e)
        }

if __name__ == "__main__":
    # Test with Winnipeg coordinates
    print("Testing Manitoba scraper with Winnipeg coordinates:")
    result = get_manitoba_fire_restrictions(49.8951, -97.1384, "Winnipeg")
    import json
    print(json.dumps(result, indent=2))

