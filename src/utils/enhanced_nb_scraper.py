import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import json
from typing import Dict, List, Optional, Any

class EnhancedNBFireWatchScraper:
    """
    Enhanced New Brunswick Fire Watch scraper that combines multiple data sources
    to provide comprehensive fire restriction information.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        self.nb_counties = [
            'Albert', 'Carleton', 'Charlotte', 'Gloucester', 'Kent', 'Kings',
            'Madawaska', 'Northumberland', 'Queens', 'Restigouche', 
            'Saint John', 'Sunbury', 'Victoria', 'Westmorland', 'York'
        ]
    
    def scrape_county_conditions_api(self) -> Optional[Dict]:
        """
        Scrape the county-specific conditions API.
        """
        try:
            url = f"https://www3.gnb.ca/public/fire-feu/maps/conditions-e.htm?dummy={int(time.time() * 1000)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text()
            
            # Extract validity period
            validity_match = re.search(r'Burning conditions are valid from (.+?)\.', text_content)
            validity_period = validity_match.group(1) if validity_match else "Current conditions"
            
            # Parse county-specific restrictions
            restrictions = {}
            
            # Split by <br/> tags for better parsing
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
                    
                if ':' in line and any(county in line for county in self.nb_counties):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        county = parts[0].strip()
                        condition = parts[1].strip()
                        
                        # Normalize the status
                        if 'closed for burning' in condition.lower():
                            status = 'No Burning'
                            risk_level = 'High'
                        elif 'open for burning' in condition.lower():
                            status = 'Burning Allowed'
                            risk_level = 'Low'
                        elif 'restricted' in condition.lower():
                            status = 'Restricted'
                            risk_level = 'Moderate'
                        else:
                            status = 'Unknown'
                            risk_level = 'Unknown'
                        
                        restrictions[county] = {
                            'status': status,
                            'condition': condition,
                            'risk_level': risk_level,
                            'source': 'County Conditions API'
                        }
            
            return {
                'restrictions': restrictions,
                'validity_period': validity_period,
                'source': 'NB DNR County Conditions API',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error scraping county conditions API: {e}")
            return None
    
    def scrape_fire_watch_page(self) -> Optional[Dict]:
        """
        Scrape the main Fire Watch page for additional information.
        """
        try:
            url = "https://www.gnb.ca/en/topic/laws-safety/emergency-preparedness-alerts/fire-watch.html"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract general fire watch information
            fire_watch_info = {
                'general_status': 'Unknown',
                'alerts': [],
                'weather_conditions': None,
                'fire_danger_rating': None
            }
            
            # Look for burn ban notices
            page_text = soup.get_text().lower()
            if 'burn ban' in page_text or 'closed for burning' in page_text:
                fire_watch_info['general_status'] = 'Burn Ban Active'
            elif 'restricted burning' in page_text:
                fire_watch_info['general_status'] = 'Restricted Burning'
            elif 'open for burning' in page_text:
                fire_watch_info['general_status'] = 'Open for Burning'
            
            # Look for alerts and notices
            alert_sections = soup.find_all(['div', 'section'], class_=re.compile(r'alert|notice|warning', re.I))
            for section in alert_sections:
                alert_text = section.get_text(strip=True)
                if alert_text and len(alert_text) > 20:  # Filter out short/empty alerts
                    fire_watch_info['alerts'].append(alert_text)
            
            # Look for weather-related information
            weather_keywords = ['weather', 'wind', 'humidity', 'temperature', 'precipitation']
            for keyword in weather_keywords:
                weather_match = re.search(rf'{keyword}[^.]*\.', page_text, re.IGNORECASE)
                if weather_match:
                    fire_watch_info['weather_conditions'] = weather_match.group(0)
                    break
            
            return {
                'fire_watch_info': fire_watch_info,
                'source': 'NB Fire Watch Page',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error scraping fire watch page: {e}")
            return None
    
    def scrape_fire_danger_rating(self) -> Optional[Dict]:
        """
        Attempt to scrape fire danger rating information.
        """
        try:
            # Try the fire danger rating page
            url = "https://www.gnb.ca/en/topic/laws-safety/emergency-preparedness-alerts/fire-danger-rating.html"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                danger_info = {
                    'current_rating': None,
                    'forecast': None,
                    'regional_ratings': {}
                }
                
                # Look for danger rating indicators
                rating_keywords = ['low', 'moderate', 'high', 'very high', 'extreme']
                page_text = soup.get_text().lower()
                
                for rating in rating_keywords:
                    if f'fire danger rating: {rating}' in page_text or f'current rating: {rating}' in page_text:
                        danger_info['current_rating'] = rating.title()
                        break
                
                return {
                    'danger_info': danger_info,
                    'source': 'NB Fire Danger Rating Page',
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"Error scraping fire danger rating: {e}")
        
        return None
    
    def get_enhanced_report(self, county: str = None) -> Dict[str, Any]:
        """
        Generate an enhanced fire watch report combining all available sources.
        """
        report = {
            'location': county or 'New Brunswick',
            'timestamp': datetime.now().isoformat(),
            'sources_consulted': [],
            'county_conditions': {},
            'general_fire_watch': {},
            'fire_danger_rating': {},
            'summary': {},
            'recommendations': []
        }
        
        # Scrape county conditions
        county_data = self.scrape_county_conditions_api()
        if county_data:
            report['sources_consulted'].append('County Conditions API')
            report['county_conditions'] = county_data
            
            # If specific county requested, extract that data
            if county and county in county_data.get('restrictions', {}):
                county_info = county_data['restrictions'][county]
                report['summary']['county_status'] = county_info['status']
                report['summary']['county_condition'] = county_info['condition']
                report['summary']['risk_level'] = county_info['risk_level']
        
        # Scrape fire watch page
        fire_watch_data = self.scrape_fire_watch_page()
        if fire_watch_data:
            report['sources_consulted'].append('Fire Watch Page')
            report['general_fire_watch'] = fire_watch_data
            report['summary']['general_status'] = fire_watch_data['fire_watch_info']['general_status']
        
        # Scrape fire danger rating
        danger_data = self.scrape_fire_danger_rating()
        if danger_data:
            report['sources_consulted'].append('Fire Danger Rating Page')
            report['fire_danger_rating'] = danger_data
            if danger_data['danger_info']['current_rating']:
                report['summary']['fire_danger_rating'] = danger_data['danger_info']['current_rating']
        
        # Generate recommendations based on collected data
        self._generate_recommendations(report)
        
        # Create overall summary
        self._create_summary(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]):
        """
        Generate safety recommendations based on the collected data.
        """
        recommendations = []
        
        # Base recommendations
        recommendations.append("Always check current conditions before planning any burning activities")
        recommendations.append("Follow all local fire department guidelines and obtain necessary permits")
        
        # County-specific recommendations
        if 'county_status' in report['summary']:
            status = report['summary']['county_status']
            if status == 'No Burning':
                recommendations.extend([
                    "All outdoor burning is prohibited in this county",
                    "Extinguish any existing fires immediately",
                    "Report any unauthorized fires to local authorities"
                ])
            elif status == 'Restricted':
                recommendations.extend([
                    "Burning may be permitted during specific hours only",
                    "Check with local fire department for current restrictions",
                    "Have adequate water supply and supervision available"
                ])
            elif status == 'Burning Allowed':
                recommendations.extend([
                    "Burning is currently permitted but conditions can change rapidly",
                    "Monitor weather conditions and wind speed",
                    "Follow safe burning practices and have extinguishing materials ready"
                ])
        
        # Risk level recommendations
        if 'risk_level' in report['summary']:
            risk = report['summary']['risk_level']
            if risk == 'High':
                recommendations.append("Fire risk is currently high - exercise extreme caution")
            elif risk == 'Moderate':
                recommendations.append("Fire risk is moderate - follow all safety protocols")
        
        # Fire danger rating recommendations
        if 'fire_danger_rating' in report['summary']:
            rating = report['summary']['fire_danger_rating'].lower()
            if rating in ['high', 'very high', 'extreme']:
                recommendations.append(f"Fire danger rating is {rating} - avoid all non-essential burning")
        
        report['recommendations'] = recommendations
    
    def _create_summary(self, report: Dict[str, Any]):
        """
        Create an overall summary of the fire watch situation.
        """
        summary = report['summary']
        
        # Determine overall status
        if 'county_status' in summary:
            summary['overall_status'] = summary['county_status']
        elif 'general_status' in summary:
            summary['overall_status'] = summary['general_status']
        else:
            summary['overall_status'] = 'Unknown'
        
        # Create status message
        if summary['overall_status'] == 'No Burning':
            summary['status_message'] = "Burning is currently prohibited. All outdoor fires must be extinguished."
        elif summary['overall_status'] == 'Restricted':
            summary['status_message'] = "Burning is restricted. Check local conditions and follow all guidelines."
        elif summary['overall_status'] == 'Burning Allowed':
            summary['status_message'] = "Burning is currently permitted. Monitor conditions and follow safety protocols."
        else:
            summary['status_message'] = "Fire restriction status is unclear. Contact local authorities for guidance."
        
        # Add validity period if available
        if report['county_conditions'].get('validity_period'):
            summary['valid_until'] = report['county_conditions']['validity_period']

def get_enhanced_nb_fire_report(county: str = None) -> Dict[str, Any]:
    """
    Convenience function to get an enhanced New Brunswick fire watch report.
    """
    scraper = EnhancedNBFireWatchScraper()
    return scraper.get_enhanced_report(county)

