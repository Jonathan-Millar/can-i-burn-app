"""
British Columbia Fire Restriction Scraper

Scrapes fire restriction data from BC Wildfire Service.
BC uses a fire centre-based system with 6 regional centres and 3 fire categories.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BC Fire Centres and their coverage areas
BC_FIRE_CENTRES = {
    'Cariboo': {
        'url': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions/cariboo-fire-centre-bans',
        'regions': ['Interior BC', 'Central BC']
    },
    'Coastal': {
        'url': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions/coastal-fire-centre-bans',
        'regions': ['Lower Mainland', 'Vancouver Island', 'Sea-to-Sky', 'Central Coast', 'Haida Gwaii']
    },
    'Kamloops': {
        'url': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions/kamloops-fire-centre-bans',
        'regions': ['South-central BC', 'Thompson-Nicola']
    },
    'Northwest': {
        'url': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions/northwest-fire-centre-bans',
        'regions': ['Northern BC', 'Northwest BC']
    },
    'Prince George': {
        'url': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions/prince-george-fire-centre-bans',
        'regions': ['North-central BC', 'Peace River']
    },
    'Southeast': {
        'url': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions/southeast-fire-centre-bans',
        'regions': ['Kootenays', 'Rockies', 'East Kootenay', 'West Kootenay']
    }
}

def determine_fire_centre_from_location(latitude, longitude, location_name=None):
    """
    Determine BC fire centre based on coordinates or location name.
    This is a simplified mapping - in production, would use official BC boundaries.
    """
    try:
        # Simplified geographic mapping for BC fire centres
        # Vancouver/Lower Mainland area
        if 49.0 <= latitude <= 49.5 and -123.5 <= longitude <= -122.5:
            return 'Coastal'
        
        # Vancouver Island
        if 48.0 <= latitude <= 51.0 and -128.5 <= longitude <= -123.0:
            return 'Coastal'
        
        # Interior BC - Kamloops area
        if 50.0 <= latitude <= 51.5 and -121.5 <= longitude <= -119.5:
            return 'Kamloops'
        
        # Southeast BC - Kootenays
        if 49.0 <= latitude <= 51.0 and -117.5 <= longitude <= -114.0:
            return 'Southeast'
        
        # Northern BC - Prince George area
        if 53.0 <= latitude <= 55.0 and -124.0 <= longitude <= -120.0:
            return 'Prince George'
        
        # Northwest BC
        if latitude >= 55.0 and longitude <= -125.0:
            return 'Northwest'
        
        # Central Interior - Cariboo
        if 51.5 <= latitude <= 53.5 and -123.0 <= longitude <= -120.0:
            return 'Cariboo'
        
        # Default to closest based on location name if available
        if location_name:
            location_lower = location_name.lower()
            if any(city in location_lower for city in ['vancouver', 'victoria', 'nanaimo', 'richmond']):
                return 'Coastal'
            elif any(city in location_lower for city in ['kamloops', 'kelowna', 'vernon']):
                return 'Kamloops'
            elif any(city in location_lower for city in ['cranbrook', 'nelson', 'castlegar']):
                return 'Southeast'
            elif any(city in location_lower for city in ['prince george', 'fort st john']):
                return 'Prince George'
            elif any(city in location_lower for city in ['prince rupert', 'terrace', 'smithers']):
                return 'Northwest'
            elif any(city in location_lower for city in ['williams lake', 'quesnel', '100 mile house']):
                return 'Cariboo'
        
        # Default to Coastal (most populated area)
        return 'Coastal'
        
    except Exception as e:
        logger.error(f"Error determining fire centre: {e}")
        return 'Coastal'

def scrape_main_restrictions_page(content, target_fire_centre):
    """
    Scrape the main BC fire restrictions page as a fallback.
    """
    try:
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the fire centre table
        table = soup.find('table')
        if not table:
            raise Exception("Could not find restrictions table")
        
        # Look for the target fire centre row
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                # Check if this row contains our fire centre
                first_cell = cells[0].get_text().strip()
                if target_fire_centre.lower() in first_cell.lower():
                    # Parse the restriction status from images
                    restrictions = {
                        'category_1': 'Unknown',
                        'category_2': 'Unknown',
                        'category_3': 'Unknown',
                        'area_restrictions': False,
                        'last_updated': None
                    }
                    
                    # Check each category column for ban/permit status
                    for i, cell in enumerate(cells[1:4], 1):  # Skip first cell (fire centre name)
                        img = cell.find('img')
                        if img and img.get('src'):
                            src = img.get('src')
                            if 'bans.png' in src:
                                status = 'Prohibited'
                            elif 'permitted.png' in src:
                                status = 'Permitted'
                            elif 'attention.png' in src:
                                status = 'Restricted'
                            else:
                                status = 'Unknown'
                            
                            # Assign to appropriate category
                            if i == 1:
                                restrictions['category_1'] = status
                            elif i == 2:
                                restrictions['category_2'] = status
                            elif i == 3:
                                restrictions['category_3'] = status
                    
                    return restrictions
        
        # If we didn't find the specific fire centre, return default
        return {
            'category_1': 'Unknown',
            'category_2': 'Unknown',
            'category_3': 'Unknown',
            'area_restrictions': False,
            'last_updated': None
        }
        
    except Exception as e:
        logger.error(f"Error parsing main restrictions page: {e}")
        return {
            'category_1': 'Unknown',
            'category_2': 'Unknown',
            'category_3': 'Unknown',
            'area_restrictions': False,
            'last_updated': None,
            'error': str(e)
        }

def scrape_fire_centre_restrictions(fire_centre):
    """
    Scrape fire restrictions for a specific BC fire centre.
    """
    try:
        if fire_centre not in BC_FIRE_CENTRES:
            raise ValueError(f"Unknown fire centre: {fire_centre}")
        
        url = BC_FIRE_CENTRES[fire_centre]['url']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Try multiple times with different approaches
        response = None
        for attempt in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=15, verify=True)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {fire_centre}: {e}")
                if attempt == 2:
                    # Try the main fire restrictions page as fallback
                    fallback_url = "https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions"
                    response = requests.get(fallback_url, headers=headers, timeout=15)
                    response.raise_for_status()
                    return scrape_main_restrictions_page(response.content, fire_centre)
        
        if not response:
            raise Exception("Failed to get response after multiple attempts")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse fire restrictions
        restrictions = {
            'category_1': 'Unknown',  # Campfires
            'category_2': 'Unknown',  # Open fires 0.5-3m
            'category_3': 'Unknown',  # Open fires >3m
            'area_restrictions': False,
            'last_updated': None
        }
        
        # Look for restriction status indicators
        # BC uses specific images to indicate ban status
        ban_images = soup.find_all('img', alt=lambda x: x and 'ban' in x.lower() if x else False)
        permitted_images = soup.find_all('img', src=lambda x: x and 'permitted' in x if x else False)
        attention_images = soup.find_all('img', alt=lambda x: x and 'attention' in x.lower() if x else False)
        
        # Parse category restrictions from page structure
        category_sections = soup.find_all(['h2', 'h3'], string=lambda x: x and 'category' in x.lower() if x else False)
        
        for section in category_sections:
            section_text = section.get_text().lower()
            
            # Find the status indicator near this section
            next_elements = section.find_next_siblings(limit=5)
            status = 'Unknown'
            
            for element in next_elements:
                if element.find('img'):
                    img = element.find('img')
                    if img.get('src'):
                        src = img.get('src')
                        if 'bans.png' in src:
                            status = 'Prohibited'
                        elif 'permitted.png' in src:
                            status = 'Permitted'
                        elif 'attention.png' in src:
                            status = 'Restricted'
                        break
            
            # Assign to appropriate category
            if 'category 1' in section_text or 'campfire' in section_text:
                restrictions['category_1'] = status
            elif 'category 2' in section_text:
                restrictions['category_2'] = status
            elif 'category 3' in section_text:
                restrictions['category_3'] = status
        
        # Check for area restrictions
        area_section = soup.find(string=lambda x: x and 'area restriction' in x.lower() if x else False)
        if area_section:
            parent = area_section.find_parent()
            if parent and 'no' not in parent.get_text().lower():
                restrictions['area_restrictions'] = True
        
        # Look for last updated date
        updated_element = soup.find('img', alt=lambda x: x and 'last updated' in x.lower() if x else False)
        if updated_element:
            date_text = updated_element.find_next(string=True)
            if date_text:
                restrictions['last_updated'] = date_text.strip()
        
        return restrictions
        
    except Exception as e:
        logger.error(f"Error scraping {fire_centre} fire centre: {e}")
        return {
            'category_1': 'Unknown',
            'category_2': 'Unknown', 
            'category_3': 'Unknown',
            'area_restrictions': False,
            'last_updated': None,
            'error': str(e)
        }

def get_bc_fire_restrictions(latitude, longitude, location_name=None):
    """
    Get comprehensive fire restriction data for British Columbia coordinates.
    """
    try:
        # Determine fire centre
        fire_centre = determine_fire_centre_from_location(latitude, longitude, location_name)
        
        # For now, provide general BC fire restriction information
        # In production, this would scrape real-time data
        general_status = "Fire restrictions vary by fire centre and category in BC"
        details = f"Located in {fire_centre} Fire Centre. BC uses a 3-category fire system: Category 1 (campfires), Category 2 (open fires 0.5-3m), and Category 3 (large fires >3m). Check BC Wildfire Service website for current restrictions."
        
        # Try to get actual restrictions (but don't fail if it doesn't work)
        restrictions = None
        try:
            restrictions = scrape_fire_centre_restrictions(fire_centre)
        except Exception as e:
            logger.warning(f"Could not get real-time restrictions: {e}")
        
        # Determine status based on available data
        if restrictions and restrictions.get('category_1') == 'Prohibited':
            overall_status = 'All Fires Prohibited'
            details = f"Category 1 (campfires) prohibited in {fire_centre} Fire Centre. Check Category 2 and 3 restrictions for larger fires."
        elif restrictions and restrictions.get('category_1') == 'Restricted':
            overall_status = 'Campfire Restrictions'
            details = f"Category 1 (campfire) restrictions in effect in {fire_centre} Fire Centre. Some areas may be excluded."
        elif restrictions and restrictions.get('category_1') == 'Permitted':
            overall_status = 'Campfires Permitted'
            details = f"Category 1 (campfires) currently permitted in {fire_centre} Fire Centre. Check local municipal restrictions."
        else:
            overall_status = 'Check BC Wildfire Service'
            details = f"Located in {fire_centre} Fire Centre. Visit BC Wildfire Service website for current fire restrictions by category."
        
        return {
            'status': overall_status,
            'details': details,
            'source': 'BC Wildfire Service',
            'last_updated': datetime.now().isoformat(),
            'fire_centre': fire_centre,
            'category_restrictions': {
                'category_1_campfires': restrictions.get('category_1', 'Check BC Wildfire Service') if restrictions else 'Check BC Wildfire Service',
                'category_2_open_fires': restrictions.get('category_2', 'Check BC Wildfire Service') if restrictions else 'Check BC Wildfire Service',
                'category_3_large_fires': restrictions.get('category_3', 'Check BC Wildfire Service') if restrictions else 'Check BC Wildfire Service'
            },
            'area_restrictions': restrictions.get('area_restrictions', False) if restrictions else False,
            'latitude': latitude,
            'longitude': longitude,
            'location_method': 'coordinates' if not location_name else 'location_name',
            'administrative_area': f"{fire_centre} Fire Centre, British Columbia",
            'website': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions'
        }
        
    except Exception as e:
        logger.error(f"Error getting BC fire restrictions: {e}")
        return {
            'status': 'Check BC Wildfire Service',
            'details': f'Located in British Columbia. Visit BC Wildfire Service website for current fire restrictions. Error: {str(e)}',
            'source': 'BC Wildfire Service',
            'last_updated': datetime.now().isoformat(),
            'fire_centre': 'Unknown',
            'latitude': latitude,
            'longitude': longitude,
            'website': 'https://www2.gov.bc.ca/gov/content/safety/wildfire-status/prevention/fire-bans-and-restrictions',
            'error': str(e)
        }

if __name__ == "__main__":
    # Test with Vancouver coordinates
    print("Testing BC scraper with Vancouver coordinates:")
    result = get_bc_fire_restrictions(49.2827, -123.1207, "Vancouver")
    import json
    print(json.dumps(result, indent=2))

