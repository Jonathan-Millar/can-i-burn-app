"""
Saskatchewan Fire Restriction Scraper

Scrapes fire restriction data from Saskatchewan Public Safety Agency (SPSA).
Saskatchewan has a multi-jurisdictional system with municipal, provincial, and federal authorities.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def determine_saskatchewan_municipality_from_location(latitude, longitude, location_name=None):
    """
    Determine Saskatchewan municipality based on coordinates or location name.
    This is a simplified mapping - in production, would use official Saskatchewan boundaries.
    """
    try:
        # Simplified geographic mapping for Saskatchewan municipalities
        # Saskatoon area
        if 52.0 <= latitude <= 52.3 and -107.0 <= longitude <= -106.4:
            return 'Saskatoon'
        
        # Regina area
        if 50.3 <= latitude <= 50.6 and -104.8 <= longitude <= -104.4:
            return 'Regina'
        
        # Prince Albert area
        if 53.0 <= latitude <= 53.4 and -106.0 <= longitude <= -105.5:
            return 'Prince Albert'
        
        # Moose Jaw area
        if 50.2 <= latitude <= 50.5 and -105.8 <= longitude <= -105.4:
            return 'Moose Jaw'
        
        # Swift Current area
        if 50.1 <= latitude <= 50.4 and -108.0 <= longitude <= -107.5:
            return 'Swift Current'
        
        # Yorkton area
        if 51.1 <= latitude <= 51.4 and -102.7 <= longitude <= -102.3:
            return 'Yorkton'
        
        # North Battleford area
        if 52.6 <= latitude <= 52.9 and -108.5 <= longitude <= -108.1:
            return 'North Battleford'
        
        # Default based on location name if available
        if location_name:
            location_lower = location_name.lower()
            if any(city in location_lower for city in ['saskatoon', 'stoon']):
                return 'Saskatoon'
            elif any(city in location_lower for city in ['regina', 'queen city']):
                return 'Regina'
            elif any(city in location_lower for city in ['prince albert', 'pa']):
                return 'Prince Albert'
            elif any(city in location_lower for city in ['moose jaw']):
                return 'Moose Jaw'
            elif any(city in location_lower for city in ['swift current']):
                return 'Swift Current'
            elif any(city in location_lower for city in ['yorkton']):
                return 'Yorkton'
            elif any(city in location_lower for city in ['north battleford', 'battleford']):
                return 'North Battleford'
        
        # Default to Central Saskatchewan
        return 'Central Saskatchewan'
        
    except Exception as e:
        logger.error(f"Error determining Saskatchewan municipality: {e}")
        return 'Central Saskatchewan'

def scrape_saskatchewan_fire_restrictions():
    """
    Scrape current fire restrictions from Saskatchewan Public Safety Agency website.
    """
    try:
        url = "https://www.saskpublicsafety.ca/at-home/fire-bans-at-home"
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
        
        # Look for fire ban information
        restrictions = {
            'provincial_status': 'Unknown',
            'municipal_bans_active': False,
            'description': 'Unable to determine current restrictions',
            'last_updated': None
        }
        
        # Look for provincial fire ban status
        page_text = soup.get_text().lower()
        
        if 'fire ban' in page_text and 'lifted' in page_text:
            restrictions['provincial_status'] = 'No Provincial Fire Ban'
            restrictions['description'] = 'No provincial fire ban currently in effect. Check local municipal restrictions.'
        elif 'fire ban' in page_text and ('effect' in page_text or 'active' in page_text):
            restrictions['provincial_status'] = 'Provincial Fire Ban'
            restrictions['description'] = 'Provincial fire ban in effect on Crown land, provincial forests and parks.'
        elif 'fire restriction' in page_text:
            restrictions['provincial_status'] = 'Fire Restrictions'
            restrictions['description'] = 'Fire restrictions in effect. Check specific area restrictions.'
        else:
            restrictions['provincial_status'] = 'Normal Conditions'
            restrictions['description'] = 'No province-wide fire restrictions. Check local municipal restrictions.'
        
        # Look for municipal fire ban information
        if 'municipal' in page_text and ('ban' in page_text or 'restriction' in page_text):
            restrictions['municipal_bans_active'] = True
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping Saskatchewan fire restrictions: {e}")
        return {
            'provincial_status': 'Unknown',
            'municipal_bans_active': False,
            'description': f'Unable to retrieve fire restriction data. Error: {str(e)}',
            'last_updated': None,
            'error': str(e)
        }

def get_saskatchewan_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for Saskatchewan coordinates.
    """
    try:
        # Determine Saskatchewan municipality
        municipality = determine_saskatchewan_municipality_from_location(latitude, longitude, location_name)
        
        # Get current restrictions
        restrictions = scrape_saskatchewan_fire_restrictions()
        
        # Determine overall status
        provincial_status = restrictions.get('provincial_status', 'Unknown')
        municipal_bans = restrictions.get('municipal_bans_active', False)
        
        if provincial_status == 'Provincial Fire Ban':
            overall_status = 'Provincial Fire Ban'
            details = f"Provincial fire ban in effect in {municipality}. Open burning prohibited on Crown land, provincial forests and parks. Check local municipal restrictions for additional bans."
        elif municipal_bans:
            overall_status = 'Municipal Fire Restrictions'
            details = f"Municipal fire restrictions may be in effect in {municipality}. Check with local authorities for current burning restrictions."
        elif provincial_status == 'Fire Restrictions':
            overall_status = 'Fire Restrictions'
            details = f"Fire restrictions in effect in {municipality}. Check specific area restrictions before lighting fires."
        elif provincial_status == 'No Provincial Fire Ban':
            overall_status = 'No Provincial Fire Ban'
            details = f"No provincial fire ban in {municipality}. Check local municipal restrictions before lighting fires."
        else:
            overall_status = 'Check Local Authorities'
            details = f"Located in {municipality}. Check with local authorities and SPSA for current fire restrictions."
        
        return {
            'status': overall_status,
            'details': details,
            'source': 'Saskatchewan Public Safety Agency',
            'last_updated': datetime.now().isoformat(),
            'municipality': municipality,
            'provincial_status': provincial_status,
            'municipal_bans_possible': municipal_bans,
            'jurisdiction_info': {
                'municipal_authority': 'Local government',
                'provincial_authority': 'SPSA (Crown land, provincial forests/parks)',
                'federal_authority': 'National parks'
            },
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{municipality}, Saskatchewan",
            'website': 'https://www.saskpublicsafety.ca/at-home/fire-bans-at-home',
            'interactive_map': 'https://gis.saskatchewan.ca/portal/apps/webappviewer/index.html?id=f0a6d16a99944a788be8a633870a4590',
            'pdf_map': 'https://wfm.gov.sk.ca/static/public/MunicipalFireBans.pdf'
        }
        
    except Exception as e:
        logger.error(f"Error getting Saskatchewan fire restrictions: {e}")
        return {
            'status': 'Check SPSA',
            'details': f'Located in Saskatchewan. Visit Saskatchewan Public Safety Agency website for current fire restrictions. Error: {str(e)}',
            'source': 'Saskatchewan Public Safety Agency',
            'last_updated': datetime.now().isoformat(),
            'municipality': 'Unknown',
            'latitude': latitude,
            'longitude': longitude,
            'website': 'https://www.saskpublicsafety.ca/at-home/fire-bans-at-home',
            'interactive_map': 'https://gis.saskatchewan.ca/portal/apps/webappviewer/index.html?id=f0a6d16a99944a788be8a633870a4590',
            'error': str(e)
        }

if __name__ == "__main__":
    # Test with Saskatoon coordinates
    print("Testing Saskatchewan scraper with Saskatoon coordinates:")
    result = get_saskatchewan_fire_restrictions(52.1579, -106.6702, "Saskatoon")
    import json
    print(json.dumps(result, indent=2))

