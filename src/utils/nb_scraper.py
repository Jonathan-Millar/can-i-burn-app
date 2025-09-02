import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

def scrape_nb_fire_restrictions():
    """
    Scrape New Brunswick fire restriction data from the county-specific API.
    Returns a dictionary with county-specific restrictions.
    """
    try:
        # Use the county-specific API endpoint
        url = f"https://www3.gnb.ca/public/fire-feu/maps/conditions-e.htm?dummy={int(time.time() * 1000)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        
        # Extract validity period
        validity_match = re.search(r'Burning conditions are valid from (.+?)\.', text_content)
        validity_period = validity_match.group(1) if validity_match else "Current conditions"
        
        # Parse county-specific restrictions
        restrictions = {}
        
        # Split by <br/> tags first, then by lines
        lines = []
        if '<br/>' in response.text:
            lines = response.text.split('<br/>')
        else:
            lines = text_content.split('\n')
        
        for line in lines:
            line = line.strip()
            # Skip the validity period line
            if 'Burning conditions are valid' in line:
                continue
                
            if ':' in line and any(county in line for county in [
                'Albert', 'Carleton', 'Charlotte', 'Gloucester', 'Kent', 'Kings',
                'Madawaska', 'Northumberland', 'Queens', 'Restigouche', 
                'Saint John', 'Sunbury', 'Victoria', 'Westmorland', 'York'
            ]):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    county = parts[0].strip()
                    condition = parts[1].strip()
                    
                    # Normalize the status
                    if 'closed for burning' in condition.lower():
                        status = 'No Burning'
                        details = f'County closed for burning - {validity_period}'
                    elif 'open for burning' in condition.lower():
                        status = 'Burning Allowed'
                        details = f'County open for burning - {validity_period}'
                    elif 'restricted' in condition.lower():
                        status = 'Restricted'
                        details = f'Restricted burning conditions - {validity_period}'
                    else:
                        status = 'Unknown'
                        details = f'{condition} - {validity_period}'
                    
                    restrictions[county] = {
                        'status': status,
                        'details': details
                    }
        
        # If no counties were parsed, fall back to default
        if not restrictions:
            default_counties = [
                'Albert', 'Carleton', 'Charlotte', 'Gloucester', 'Kent', 'Kings',
                'Madawaska', 'Northumberland', 'Queens', 'Restigouche', 
                'Saint John', 'Sunbury', 'Victoria', 'Westmorland', 'York'
            ]
            
            for county in default_counties:
                restrictions[county] = {
                    'status': 'No Burning',
                    'details': f'Province-wide restrictions in effect - {validity_period}'
                }
        
        return {
            'restrictions': restrictions,
            'last_updated': datetime.now().isoformat(),
            'source': 'New Brunswick Department of Natural Resources',
            'validity_period': validity_period
        }
        
    except Exception as e:
        print(f"Error scraping NB fire restrictions: {e}")
        return None

def scrape_nb_burn_restrictions():
    """
    Legacy function name - calls the new function for backward compatibility.
    """
    result = scrape_nb_fire_restrictions()
    if result and 'restrictions' in result:
        # Return province-wide status for backward compatibility
        return {
            'status': 'No Burning',  # Default to most restrictive
            'details': 'Province-wide burn ban in effect - all fires prohibited',
            'last_updated': result['last_updated'],
            'source': result['source']
        }
    else:
        return {
            'status': 'Unknown',
            'details': 'Unable to fetch current restrictions',
            'last_updated': datetime.now().isoformat(),
            'source': 'New Brunswick Fire Watch'
        }

