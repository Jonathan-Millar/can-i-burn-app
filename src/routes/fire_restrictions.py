import json
import os
import requests
from datetime import datetime
from flask import Blueprint, request, jsonify
from shapely.geometry import Point, shape
from geopy.geocoders import Nominatim

fire_restrictions_bp = Blueprint('fire_restrictions', __name__)

# Load county GeoJSON data
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'pei_county_zones.geojson')
with open(GEOJSON_PATH, 'r') as f:
    county_data = json.load(f)

def get_county_from_coordinates(latitude, longitude):
    """
    Determine which PEI county contains the given coordinates.
    """
    point = Point(longitude, latitude)
    
    for feature in county_data['features']:
        county_shape = shape(feature['geometry'])
        if county_shape.contains(point):
            # Extract county name from properties
            properties = feature['properties']
            county_name = properties.get('KEYWORD', 'Unknown')
            return county_name
    
    return None

def scrape_burn_restrictions():
    """
    Scrape current burn restrictions from the PEI government website.
    """
    try:
        # The burn restrictions page URL
        url = "https://www.princeedwardisland.ca/en/feature/burning-restrictions"
        
        # For now, we'll return mock data based on what we observed
        # In a real implementation, we would parse the HTML or use an API
        restrictions = {
            'PRINCE': {
                'status': 'No Burning',
                'details': 'Fire closure order in place - all fires banned',
                'last_updated': datetime.now().isoformat()
            },
            'QUEENS': {
                'status': 'No Burning', 
                'details': 'Fire closure order in place - all fires banned',
                'last_updated': datetime.now().isoformat()
            },
            'KINGS': {
                'status': 'No Burning',
                'details': 'Fire closure order in place - all fires banned', 
                'last_updated': datetime.now().isoformat()
            }
        }
        
        return restrictions
    except Exception as e:
        print(f"Error scraping burn restrictions: {e}")
        return {}

def geocode_location(location_name):
    """
    Convert a location name to GPS coordinates.
    """
    try:
        geolocator = Nominatim(user_agent="pei_fire_watch")
        # Append ", PEI, Canada" to improve accuracy
        location = geolocator.geocode(f"{location_name}, PEI, Canada")
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Error geocoding location: {e}")
        return None, None

@fire_restrictions_bp.route('/burn_restrictions', methods=['GET'])
def get_burn_restrictions():
    """
    API endpoint to get burn restrictions for a location.
    Accepts either latitude/longitude or location name.
    """
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        location_name = request.args.get('location')
        
        # If location name is provided, geocode it first
        if location_name and (latitude is None or longitude is None):
            latitude, longitude = geocode_location(location_name)
            if latitude is None or longitude is None:
                return jsonify({
                    'error': f'Could not geocode location: {location_name}'
                }), 400
        
        # Validate coordinates
        if latitude is None or longitude is None:
            return jsonify({
                'error': 'Please provide either latitude/longitude or location name'
            }), 400
        
        # Check if coordinates are within PEI bounds (approximate)
        if not (45.9 <= latitude <= 47.1 and -64.5 <= longitude <= -61.9):
            return jsonify({
                'error': 'Coordinates appear to be outside of PEI'
            }), 400
        
        # Get county for the coordinates
        county = get_county_from_coordinates(latitude, longitude)
        if not county:
            return jsonify({
                'error': 'Could not determine county for the given coordinates'
            }), 404
        
        # Get current burn restrictions
        restrictions = scrape_burn_restrictions()
        county_restriction = restrictions.get(county, {
            'status': 'Unknown',
            'details': 'Unable to retrieve restriction information',
            'last_updated': datetime.now().isoformat()
        })
        
        return jsonify({
            'latitude': latitude,
            'longitude': longitude,
            'county': county,
            'burn_restriction': county_restriction
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fire_restrictions_bp.route('/counties', methods=['GET'])
def get_counties():
    """
    API endpoint to get all PEI counties.
    """
    try:
        counties = []
        seen_counties = set()
        for feature in county_data['features']:
            properties = feature['properties']
            county_name = properties.get('KEYWORD', 'Unknown').strip()
            if county_name and county_name != 'Unknown' and county_name not in seen_counties:
                counties.append({
                    'name': county_name,
                    'id': county_name.lower()
                })
                seen_counties.add(county_name)
        
        return jsonify({'counties': counties})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

