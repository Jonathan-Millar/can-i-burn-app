from flask import Blueprint, request, jsonify
import json
from ..utils.province_detector import detect_province_and_county
from src.utils.enhanced_nb_scraper import get_enhanced_nb_fire_report
from src.utils.ns_scraper import get_ns_fire_report
from src.utils.ontario_scraper import get_ontario_fire_restrictions
from src.utils.bc_scraper import get_bc_fire_restrictions
from src.utils.alberta_scraper import get_alberta_fire_restrictions
from src.utils.saskatchewan_scraper import get_saskatchewan_fire_restrictions
from src.utils.manitoba_scraper import get_manitoba_fire_restrictions
from src.utils.quebec_scraper import get_quebec_fire_restrictions
from src.utils.newfoundland_scraper import get_nl_fire_restrictions
from src.utils.territories_scraper import get_territory_fire_restrictions
import requests
from datetime import datetime

enhanced_fire_restrictions_bp = Blueprint("enhanced_fire_restrictions", __name__)

def geocode_location(location_name):
    """Convert location name to coordinates using Nominatim."""
    try:
        # Try different location formats for better results
        search_queries = [
            f"{location_name}, Canada",
            f"{location_name}, PEI, Canada", 
            f"{location_name}, Prince Edward Island, Canada",
            f"{location_name}, NB, Canada",
            f"{location_name}, New Brunswick, Canada",
            f"{location_name}, NS, Canada",
            f"{location_name}, Nova Scotia, Canada",
            f"{location_name}, ON, Canada",
            f"{location_name}, Ontario, Canada",
            f"{location_name}, BC, Canada",
            f"{location_name}, British Columbia, Canada",
            f"{location_name}, AB, Canada",
            f"{location_name}, Alberta, Canada",
            f"{location_name}, SK, Canada",
            f"{location_name}, Saskatchewan, Canada",
            f"{location_name}, MB, Canada",
            f"{location_name}, Manitoba, Canada",
            f"{location_name}, QC, Canada",
            f"{location_name}, Quebec, Canada",
            f"{location_name}, Québec, Canada",
            f"{location_name}, NL, Canada",
            f"{location_name}, Newfoundland and Labrador, Canada",
            f"{location_name}, Newfoundland, Canada",
            f"{location_name}, YT, Canada",
            f"{location_name}, Yukon, Canada",
            f"{location_name}, Yukon Territory, Canada",
            f"{location_name}, NT, Canada",
            f"{location_name}, NWT, Canada",
            f"{location_name}, Northwest Territories, Canada",
            f"{location_name}, NU, Canada",
            f"{location_name}, Nunavut, Canada"
        ]
        
        for query in search_queries:
            url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]["lat"]), float(data[0]["lon"])
        
        return None, None
        
    except Exception as e:
        print(f"Error geocoding location: {e}")
        return None, None

def scrape_burn_restrictions(province, county=None):
    """Scrape burn restrictions for the specified province and county."""
    if province == "PEI":
        # PEI restrictions (simulated data for now)
        pei_restrictions = {
            "PRINCE": {"status": "No Burning", "details": "Fire closure order in place - all fires banned"},
            "QUEENS": {"status": "No Burning", "details": "Fire closure order in place - all fires banned"},
            "KINGS": {"status": "No Burning", "details": "Fire closure order in place - all fires banned"}
        }
        
        county_restriction = pei_restrictions.get(county, {
            "status": "No Burning", 
            "details": "Fire closure order in place - all fires banned"
        })
        
        return {
            "burn_restriction": {
                "status": county_restriction["status"],
                "details": county_restriction["details"],
                "source": "Prince Edward Island Fire Services",
                "last_updated": datetime.now().isoformat()
            }
        }
    
    elif province == "NB":
        # Use enhanced New Brunswick scraper
        enhanced_report = get_enhanced_nb_fire_report(county)
        
        # Extract the key information for API response
        status = enhanced_report["summary"].get("overall_status", "Unknown")
        details = enhanced_report["summary"].get("status_message", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": "New Brunswick Department of Natural Resources",
                "last_updated": enhanced_report["timestamp"],
                "enhanced_report": enhanced_report  # Include full enhanced report
            }
        }
    
    elif province == "NS":
        # Use Nova Scotia scraper
        ns_report = get_ns_fire_report(county)
        
        # Extract the key information for API response
        status = ns_report["summary"].get("overall_status", "Unknown")
        details = ns_report["summary"].get("status_message", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": "Nova Scotia Department of Natural Resources",
                "last_updated": ns_report["timestamp"],
                "enhanced_report": ns_report  # Include full enhanced report
            }
        }
    
    elif province == "ON":
        # Use Ontario scraper
        ontario_report = get_ontario_fire_restrictions()
        
        # Extract the key information for API response
        status = ontario_report.get("status", "Unknown")
        details = ontario_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": ontario_report.get("source", "Ontario Ministry of Natural Resources and Forestry"),
                "last_updated": ontario_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": ontario_report  # Include full enhanced report
            }
        }
    
    elif province == "BC":
        # Use British Columbia scraper
        bc_report = get_bc_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = bc_report.get("status", "Unknown")
        details = bc_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": bc_report.get("source", "BC Wildfire Service"),
                "last_updated": bc_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": bc_report  # Include full enhanced report
            }
        }
    
    elif province == "AB":
        # Use Alberta scraper
        ab_report = get_alberta_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = ab_report.get("status", "Unknown")
        details = ab_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": ab_report.get("source", "Alberta Wildfire"),
                "last_updated": ab_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": ab_report  # Include full enhanced report
            }
        }
    
    elif province == "SK":
        # Use Saskatchewan scraper
        sk_report = get_saskatchewan_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = sk_report.get("status", "Unknown")
        details = sk_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": sk_report.get("source", "Saskatchewan Public Safety Agency"),
                "last_updated": sk_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": sk_report  # Include full enhanced report
            }
        }
    
    elif province == "MB":
        # Use Manitoba scraper
        mb_report = get_manitoba_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = mb_report.get("status", "Unknown")
        details = mb_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": mb_report.get("source", "Manitoba Wildfire Service"),
                "last_updated": mb_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": mb_report  # Include full enhanced report
            }
        }
    
    elif province == "QC":
        # Use Quebec scraper
        qc_report = get_quebec_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = qc_report.get("status", "Unknown")
        details = qc_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": qc_report.get("source", "SOPFEU"),
                "last_updated": qc_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": qc_report  # Include full enhanced report
            }
        }
    
    elif province == "NL":
        # Use Newfoundland and Labrador scraper
        nl_report = get_nl_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = nl_report.get("status", "Unknown")
        details = nl_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": nl_report.get("source", "NL Fisheries, Forestry and Agriculture"),
                "last_updated": nl_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": nl_report  # Include full enhanced report
            }
        }
    
    elif province in ["YT", "NT", "NU"]:
        # Use territories scraper
        territory_report = get_territory_fire_restrictions(latitude=None, longitude=None, location_name=county)
        
        # Extract the key information for API response
        status = territory_report.get("status", "Unknown")
        details = territory_report.get("details", "Unable to determine current restrictions")
        
        return {
            "burn_restriction": {
                "status": status,
                "details": details,
                "source": territory_report.get("source", "Canadian Territories"),
                "last_updated": territory_report.get("last_updated", datetime.now().isoformat()),
                "enhanced_report": territory_report  # Include full enhanced report
            }
        }
    
    return None

@enhanced_fire_restrictions_bp.route("/api/enhanced/burn_restrictions", methods=["GET"])
def get_enhanced_burn_restrictions():
    """Get enhanced burn restrictions for specified coordinates or location."""
    try:
        latitude = request.args.get("latitude", type=float)
        longitude = request.args.get("longitude", type=float)
        location = request.args.get("location")
        
        # If location name provided, geocode it
        if location and not (latitude and longitude):
            latitude, longitude = geocode_location(location)
            if not latitude or not longitude:
                return jsonify({"error": f"Could not find coordinates for location: {location}"}), 400
        
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        # Detect province and county using Nominatim
        province, county = detect_province_and_county(latitude, longitude)
        if not province:
            return jsonify({"error": "Location is outside supported provinces and territories (PEI, NB, NS, ON, BC, AB, SK, MB, QC, NL, YT, NT, NU)"}), 400
        
        if not county:
            # If Nominatim didn't return a specific county, try to get province-wide status
            # This is particularly useful for NS where county GeoJSON is problematic
            print(f"Warning: No specific county found for {latitude}, {longitude}. Proceeding with province-wide lookup.")

        # Get burn restrictions
        restrictions = scrape_burn_restrictions(province, county)
        if not restrictions:
            return jsonify({"error": "Could not fetch burn restrictions"}), 500
        
        # Prepare response
        response = {
            "latitude": latitude,
            "longitude": longitude,
            "province": province,
            "county": county,
            **restrictions
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@enhanced_fire_restrictions_bp.route("/api/enhanced/nb_report", methods=["GET"])
def get_nb_enhanced_report():
    """Get comprehensive enhanced fire watch report for New Brunswick."""
    try:
        county = request.args.get("county")
        latitude = request.args.get("latitude", type=float)
        longitude = request.args.get("longitude", type=float)
        location = request.args.get("location")
        
        # If location provided, try to determine county
        if location and not county:
            if latitude and longitude:
                # Use Nominatim to get county for NB
                province, detected_county = detect_province_and_county(latitude, longitude)
                if province == 'NB':
                    county = detected_county
            else:
                # Try to geocode and get county
                lat, lon = geocode_location(location)
                if lat and lon:
                    province, detected_county = detect_province_and_county(lat, lon)
                    if province == 'NB':
                        county = detected_county
        
        # Get enhanced report
        report = get_enhanced_nb_fire_report(county)
        
        # Add location information if available
        if latitude and longitude:
            report["query_location"] = {
                "latitude": latitude,
                "longitude": longitude,
                "county": county
            }
        elif location:
            report["query_location"] = {
                "location_name": location,
                "county": county
            }
        
        return jsonify(report)
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@enhanced_fire_restrictions_bp.route("/api/enhanced/provinces", methods=["GET"])
def get_enhanced_provinces():
    """Get list of supported provinces with enhanced features."""
    return jsonify({
        "provinces": [
            {
                "code": "PEI", 
                "name": "Prince Edward Island",
                "features": ["county_detection_via_geolocator", "basic_restrictions"]
            },
            {
                "code": "NB", 
                "name": "New Brunswick",
                "features": ["county_detection_via_geolocator", "enhanced_reporting", "multi_source_data", "risk_assessment", "recommendations"]
            },
            {
                "code": "NS", 
                "name": "Nova Scotia",
                "features": ["county_detection_via_geolocator", "basic_restrictions"]
            },
            {
                "code": "ON", 
                "name": "Ontario",
                "features": ["county_detection_via_geolocator", "fire_zone_restrictions"]
            },
            {
                "code": "BC", 
                "name": "British Columbia",
                "features": ["fire_centre_detection", "category_based_restrictions", "real_time_data"]
            },
            {
                "code": "AB", 
                "name": "Alberta",
                "features": ["region_detection", "tiered_restriction_system", "forest_protection_area"]
            },
            {
                "code": "SK", 
                "name": "Saskatchewan",
                "features": ["municipality_detection", "multi_jurisdictional_system", "provincial_municipal_coordination"]
            },
            {
                "code": "MB", 
                "name": "Manitoba",
                "features": ["dual_jurisdiction_system", "seasonal_restrictions", "municipal_coordination"]
            },
            {
                "code": "QC", 
                "name": "Quebec",
                "features": ["sopfeu_system", "fire_danger_index", "zone_based_restrictions", "bilingual_service"]
            },
            {
                "code": "NL", 
                "name": "Newfoundland and Labrador",
                "features": ["province_wide_bans", "daily_hazard_updates", "enhanced_penalties", "seasonal_variations"]
            },
            {
                "code": "YT", 
                "name": "Yukon Territory",
                "features": ["multi_level_restrictions", "territory_wide_bans", "seasonal_fire_management"]
            },
            {
                "code": "NT", 
                "name": "Northwest Territories",
                "features": ["fire_danger_ratings", "community_restrictions", "territorial_coordination"]
            },
            {
                "code": "NU", 
                "name": "Nunavut",
                "features": ["community_management", "burn_permits", "arctic_fire_conditions"]
            }
        ]
    })

@enhanced_fire_restrictions_bp.route("/api/enhanced/nb_counties", methods=["GET"])
def get_nb_counties_with_status():
    """Get New Brunswick counties with current fire restriction status."""
    try:
        # Get enhanced report for all counties
        report = get_enhanced_nb_fire_report()
        
        counties_with_status = []
        if "county_conditions" in report and "restrictions" in report["county_conditions"]:
            for county, data in report["county_conditions"]["restrictions"].items():
                counties_with_status.append({
                    "name": county,
                    "status": data.get("status", "Unknown"),
                    "risk_level": data.get("risk_level", "Unknown"),
                    "condition": data.get("condition", "Unknown")
                })
        
        return jsonify({
            "counties": counties_with_status,
            "last_updated": report.get("timestamp"),
            "validity_period": report.get("county_conditions", {}).get("validity_period")
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@enhanced_fire_restrictions_bp.route("/api/enhanced/ns_counties", methods=["GET"])
def get_ns_counties_with_status():
    """Get Nova Scotia counties with current fire restriction status."""
    try:
        # Get enhanced report for all counties
        report = get_ns_fire_report()
        
        counties_with_status = []
        if "county_restrictions" in report:
            for county, data in report["county_restrictions"].items():
                counties_with_status.append({
                    "name": county,
                    "status": data.get("status", "Unknown"),
                    "details": data.get("details", "Unknown")
                })
        
        return jsonify({
            "counties": counties_with_status,
            "last_updated": report.get("timestamp"),
            "province_wide_status": report.get("province_wide_status")
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


