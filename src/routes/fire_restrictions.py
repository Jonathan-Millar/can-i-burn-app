import json
import os
import requests
from datetime import datetime
from flask import Blueprint, request, jsonify
from geopy.geocoders import Nominatim
from src.utils.geo_utils import get_county_from_coordinates
from src.utils.province_detector import detect_province_and_county
from src.utils.nb_scraper import scrape_nb_burn_restrictions

fire_restrictions_bp = Blueprint('fire_restrictions', __name__)

# Load PEI county data
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'pei_county_zones.geojson')
with open(GEOJSON_PATH, 'r') as f:
    county_data = json.load(f)

def get_county_from_coordinates_wrapper(latitude, longitude):
    """
    Determine which PEI county contains the given coordinates.
    """
    return get_county_from_coordinates(latitude, longitude, county_data)

def scrape_burn_restrictions(province='PEI'):
    """
    Scrape current burn restrictions for the specified province.
    For PEI, returns simulated data (ready for real integration).
    For NB, scrapes from the official Fire Watch page.
    """
    if province == 'NB':
        return scrape_nb_burn_restrictions()
    else:  # PEI
        # Simulated PEI data - in production, this would scrape from PEI's official source
        return {
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

def geocode_location(location_name):
    """
    Convert a location name to GPS coordinates.
    Tries both PEI and NB contexts.
    """
    try:
        geolocator = Nominatim(user_agent="fire_watch_app")
        
        # Try with PEI context first
        location = geolocator.geocode(f"{location_name}, PEI, Canada", timeout=5)
        if location:
            return location.latitude, location.longitude
        
        # Try with New Brunswick context
        location = geolocator.geocode(f"{location_name}, New Brunswick, Canada", timeout=5)
        if location:
            return location.latitude, location.longitude
            
        # Try without province context
        location = geolocator.geocode(f"{location_name}, Canada", timeout=5)
        if location:
            return location.latitude, location.longitude
            
        return None, None
    except Exception as e:
        print(f"Error geocoding location: {e}")
        return None, None

@fire_restrictions_bp.route('/burn_restrictions', methods=['GET'])
def get_burn_restrictions():
    """
    Get burn restrictions for a given location or coordinates.
    Supports both PEI and New Brunswick.
    """
    try:
        # Get parameters
        location = request.args.get('location')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        
        # Validate input
        if not location and (not latitude or not longitude):
            return jsonify({
                'error': 'Please provide either latitude/longitude or location name'
            }), 400
        
        # If location name provided, geocode it
        if location:
            lat, lon = geocode_location(location)
            if lat is None or lon is None:
                return jsonify({
                    'error': f'Could not find coordinates for location: {location}'
                }), 400
            latitude, longitude = lat, lon
        else:
            # Convert string coordinates to float
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                return jsonify({
                    'error': 'Invalid latitude or longitude format'
                }), 400
        
        # Detect province and county
        province, county = detect_province_and_county(latitude, longitude)
        
        if not province:
            return jsonify({
                'error': 'Coordinates appear to be outside of supported provinces (PEI, NB)'
            }), 400
        
        if not county:
            return jsonify({
                'error': f'Could not determine county for the given coordinates in {province}'
            }), 404
        
        # Get burn restrictions for the province
        restrictions_data = scrape_burn_restrictions(province)
        
        if province == 'PEI':
            # PEI has county-specific restrictions
            if county not in restrictions_data:
                return jsonify({
                    'error': f'No restriction data available for {county} county'
                }), 404
            
            burn_restriction = restrictions_data[county]
        else:  # New Brunswick
            # NB has province-wide restrictions
            burn_restriction = restrictions_data
        
        return jsonify({
            'province': province,
            'county': county,
            'latitude': latitude,
            'longitude': longitude,
            'burn_restriction': burn_restriction
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@fire_restrictions_bp.route('/counties', methods=['GET'])
def get_counties():
    """
    Get list of available counties for both provinces.
    """
    try:
        # PEI counties
        pei_counties = []
        for feature in county_data['features']:
            properties = feature['properties']
            county_name = properties.get('KEYWORD', '').strip()
            if county_name and county_name not in pei_counties:
                pei_counties.append(county_name)
        
        # Load NB county data
        nb_geojson_path = os.path.join(os.path.dirname(__file__), '..', 'new_brunswick_county_zones.geojson')
        with open(nb_geojson_path, 'r') as f:
            nb_county_data = json.load(f)
        
        nb_counties = []
        for feature in nb_county_data['features']:
            properties = feature['properties']
            county_name = properties.get('eng_name', '').strip()
            if county_name and county_name not in nb_counties:
                nb_counties.append(county_name)
        
        return jsonify({
            'PEI': sorted(pei_counties),
            'NB': sorted(nb_counties)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving counties: {str(e)}'
        }), 500

@fire_restrictions_bp.route('/provinces', methods=['GET'])
def get_provinces():
    """
    Get list of supported provinces.
    """
    return jsonify({
        'provinces': ['PEI', 'NB'],
        'full_names': {
            'PEI': 'Prince Edward Island',
            'NB': 'New Brunswick'
        }
    })

