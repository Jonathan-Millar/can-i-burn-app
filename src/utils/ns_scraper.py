import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import Dict, List, Optional, Any

class NSFireWatchScraper:
    """
    Scrapes Nova Scotia fire restriction data from the official BurnSafe website.
    """
    def __init__(self):
        self.url = "https://novascotia.ca/burnsafe/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.ns_counties = [
            'Annapolis County', 'Antigonish County', 'Cape Breton County', 'Colchester County',
            'Cumberland County', 'Digby County', 'Guysborough County', 'Halifax County',
            'Hants County', 'Inverness County', 'Kings County', 'Lunenburg County',
            'Pictou County', 'Queens County', 'Richmond County', 'Shelburne County',
            'Victoria County', 'Yarmouth County'
        ]

    def scrape_burnsafe_page(self) -> Optional[Dict]:
        """
        Scrape the Nova Scotia BurnSafe page for province-wide and county-specific restrictions.
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract last updated information
            last_updated_text = "Unknown"
            last_updated_elem = soup.find(string=re.compile(r'Last updated:'))
            if last_updated_elem:
                last_updated_text = last_updated_elem.strip()

            # Extract province-wide ban status
            province_wide_status = 'Unknown'
            burn_ban_text = soup.find(string=lambda text: text and 'Provincewide burn ban' in text)
            if burn_ban_text:
                # Look for surrounding text that mentions "No open fires allowed"
                parent_section = burn_ban_text.find_parent()
                if parent_section:
                    section_text = parent_section.get_text()
                    if 'No open fires allowed' in section_text:
                        province_wide_status = 'No Burning'
                    
                # Also check the next few elements for the description
                current = burn_ban_text.parent
                for _ in range(3):  # Check next 3 elements
                    if current and current.next_sibling:
                        current = current.next_sibling
                        if hasattr(current, 'get_text'):
                            text = current.get_text()
                            if 'No open fires allowed' in text:
                                province_wide_status = 'No Burning'
                                break

            # Extract county-specific restrictions from the table
            county_restrictions = {}
            
            # Find all tables and use the second one (county restrictions table)
            tables = soup.find_all('table')
            county_table = None
            
            if len(tables) >= 2:
                county_table = tables[1]  # Second table contains county data
            elif len(tables) == 1:
                county_table = tables[0]  # Fallback to first table
            
            if county_table:
                rows = county_table.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    # Look for both th and td elements (county name is in th, restriction in td)
                    county_cell = row.find('th')
                    restriction_cell = row.find('td')
                    
                    if county_cell and restriction_cell:
                        county_name = county_cell.get_text(strip=True).replace(' County', '')
                        restriction_text = restriction_cell.get_text(strip=True)
                        
                        status = 'Unknown'
                        if 'not allowed' in restriction_text.lower():
                            status = 'No Burning'
                        elif '7:00 pm and 8:00 am' in restriction_text.lower():
                            status = 'Restricted Hours (7PM-8AM)'
                        elif '2:00 pm and 8:00 am' in restriction_text.lower():
                            status = 'Burning Allowed (2PM-8AM)'
                        
                        county_restrictions[county_name] = {
                            'status': status,
                            'details': restriction_text,
                            'source': 'NS BurnSafe Table'
                        }
            
            # If no table found or incomplete data, use province-wide status as fallback
            if not county_restrictions or len(county_restrictions) < 15:  # NS has 18 counties
                print(f"Warning: Only found {len(county_restrictions)} counties in table, using province-wide fallback")
                for county in self.ns_counties:
                    county_key = county.replace(' County', '')
                    if county_key not in county_restrictions:
                        county_restrictions[county_key] = {
                            'status': province_wide_status,
                            'details': f'Province-wide burn ban in effect: {province_wide_status}',
                            'source': 'NS BurnSafe Province-wide'
                        }

            return {
                'province_wide_status': province_wide_status,
                'county_restrictions': county_restrictions,
                'last_updated_text': last_updated_text,
                'source_url': self.url,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error scraping NS BurnSafe page: {e}")
            return None

def get_ns_fire_report(county: str = None) -> Dict[str, Any]:
    """
    Convenience function to get Nova Scotia fire watch report.
    """
    scraper = NSFireWatchScraper()
    report_data = scraper.scrape_burnsafe_page()
    
    if not report_data:
        return {
            'location': county or 'Nova Scotia',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'overall_status': 'Unknown',
                'status_message': 'Unable to retrieve fire restrictions for Nova Scotia.'
            },
            'sources_consulted': [],
            'recommendations': ['Check official sources directly.']
        }

    report = {
        'location': county or 'Nova Scotia',
        'timestamp': report_data['timestamp'],
        'sources_consulted': ['NS BurnSafe Website'],
        'province_wide_status': report_data['province_wide_status'],
        'county_conditions': report_data['county_restrictions'],
        'last_updated_text': report_data['last_updated_text'],
        'source_url': report_data['source_url'],
        'summary': {},
        'recommendations': []
    }

    # Determine overall status and message
    overall_status = report_data['province_wide_status']
    status_message = f'Province-wide status: {overall_status}.'

    if county and county in report_data['county_restrictions']:
        county_info = report_data['county_restrictions'][county]
        overall_status = county_info['status']
        status_message = f'County: {county}, Status: {county_info["status"]}. Details: {county_info["details"]}.'
    
    report['summary']['overall_status'] = overall_status
    report['summary']['status_message'] = status_message

    # Generate recommendations
    recommendations = [
        "Always check current conditions before planning any burning activities.",
        "Follow all local fire department guidelines and obtain necessary permits."
    ]
    if overall_status == 'No Burning':
        recommendations.append("All outdoor burning is prohibited.")
    elif overall_status == 'Restricted':
        recommendations.append("Burning is restricted to specific hours (7 PM to 8 AM).")
    elif overall_status == 'Burning Allowed':
        recommendations.append("Burning is permitted during specific hours (2 PM to 8 AM). Monitor conditions.")
    
    report['recommendations'] = recommendations

    return report


