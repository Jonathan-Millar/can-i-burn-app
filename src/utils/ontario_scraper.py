"""
Ontario Fire Restriction Scraper

This module scrapes fire restriction data for Ontario from the official government sources.
Ontario uses a Fire Zone system rather than counties for fire restrictions.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OntarioFireScraper:
    def __init__(self):
        self.base_url = "https://www.ontario.ca/page/outdoor-fire-restrictions"
        self.map_url = "https://www.lioapplications.lrc.gov.on.ca/ForestFireInformationMap/index.html"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_general_fire_status(self):
        """
        Get general fire restriction status for Ontario from the main page.
        Returns a simplified status since Ontario uses fire zones.
        """
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for general restriction information
            content = soup.get_text().lower()
            
            # Determine general status based on content
            if 'restricted fire zone' in content and 'in effect' in content:
                status = "Restricted Fire Zones Active"
                details = "Some areas of Ontario have active Restricted Fire Zones. Check specific fire zones for your location."
            elif 'no burning' in content or 'prohibited' in content:
                status = "No Burning"
                details = "Outdoor burning is currently prohibited in restricted areas."
            else:
                status = "Check Local Conditions"
                details = "Fire restrictions vary by zone. Check local conditions and fire danger ratings."
            
            return {
                'status': status,
                'details': details,
                'source': 'Ontario Ministry of Natural Resources and Forestry',
                'last_updated': datetime.now().isoformat(),
                'province_wide': True,
                'fire_zones': {}
            }
            
        except Exception as e:
            logger.error(f"Error scraping Ontario general fire status: {e}")
            return {
                'status': 'Data Unavailable',
                'details': f'Unable to retrieve fire restriction data: {str(e)}',
                'source': 'Ontario Ministry of Natural Resources and Forestry',
                'last_updated': datetime.now().isoformat(),
                'province_wide': True,
                'fire_zones': {}
            }

    def get_fire_zone_status(self, zone_number=None):
        """
        Get fire zone specific status. 
        For now, returns general status since zone-specific data requires complex API integration.
        """
        general_status = self.get_general_fire_status()
        
        if zone_number:
            # Add zone-specific information if available
            general_status['fire_zone'] = zone_number
            general_status['zone_specific'] = True
        
        return general_status

    def get_fire_restrictions_by_coordinates(self, latitude, longitude):
        """
        Get fire restrictions for specific coordinates in Ontario.
        Uses general status since mapping coordinates to fire zones requires complex GIS operations.
        """
        try:
            # Get general status
            fire_data = self.get_general_fire_status()
            
            # Add coordinate information
            fire_data.update({
                'latitude': latitude,
                'longitude': longitude,
                'location_method': 'coordinates',
                'administrative_area': 'Ontario',
                'fire_zone': 'Unknown - Check Local Conditions'
            })
            
            # Enhance details with coordinate-specific advice
            fire_data['details'] += f" Location: {latitude:.4f}, {longitude:.4f}. " \
                                   "Ontario uses fire zones for restrictions. Check the interactive fire map " \
                                   "at ontario.ca for zone-specific information."
            
            return fire_data
            
        except Exception as e:
            logger.error(f"Error getting Ontario fire restrictions for coordinates {latitude}, {longitude}: {e}")
            return {
                'status': 'Data Unavailable',
                'details': f'Unable to retrieve fire restriction data for coordinates: {str(e)}',
                'source': 'Ontario Ministry of Natural Resources and Forestry',
                'last_updated': datetime.now().isoformat(),
                'latitude': latitude,
                'longitude': longitude,
                'administrative_area': 'Ontario',
                'fire_zone': 'Unknown'
            }

def get_ontario_fire_restrictions(latitude=None, longitude=None, location_name=None):
    """
    Main function to get Ontario fire restrictions.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate  
        location_name (str): Name of location (not used for Ontario)
    
    Returns:
        dict: Fire restriction data for Ontario
    """
    scraper = OntarioFireScraper()
    
    if latitude is not None and longitude is not None:
        return scraper.get_fire_restrictions_by_coordinates(latitude, longitude)
    else:
        return scraper.get_general_fire_status()

# Test function
if __name__ == "__main__":
    # Test with Toronto coordinates
    toronto_lat, toronto_lon = 43.6532, -79.3832
    print("Testing Ontario fire restrictions for Toronto:")
    result = get_ontario_fire_restrictions(toronto_lat, toronto_lon)
    print(json.dumps(result, indent=2))
    
    # Test general status
    print("\nTesting Ontario general fire status:")
    general_result = get_ontario_fire_restrictions()
    print(json.dumps(general_result, indent=2))

