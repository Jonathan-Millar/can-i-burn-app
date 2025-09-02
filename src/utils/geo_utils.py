import json
import math

def point_in_polygon(point_lat, point_lon, polygon_coords):
    """
    Determine if a point is inside a polygon using the ray casting algorithm.
    polygon_coords should be a list of [lon, lat] coordinate pairs.
    """
    x, y = point_lon, point_lat
    n = len(polygon_coords)
    inside = False

    p1x, p1y = polygon_coords[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def get_county_from_coordinates(latitude, longitude, county_data):
    """
    Determine which PEI county contains the given coordinates.
    """
    for feature in county_data['features']:
        geometry = feature['geometry']
        properties = feature['properties']
        county_name = properties.get('KEYWORD', 'Unknown').strip()
        
        if geometry['type'] == 'MultiPolygon':
            # Handle MultiPolygon geometry
            for polygon in geometry['coordinates']:
                # Each polygon is a list of rings, first ring is exterior
                exterior_ring = polygon[0]
                if point_in_polygon(latitude, longitude, exterior_ring):
                    return county_name
        elif geometry['type'] == 'Polygon':
            # Handle simple Polygon geometry
            exterior_ring = geometry['coordinates'][0]
            if point_in_polygon(latitude, longitude, exterior_ring):
                return county_name
    
    return None

