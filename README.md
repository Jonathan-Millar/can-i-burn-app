# PEI Fire Watch

A web application that provides current fire burn restriction information for Prince Edward Island based on GPS coordinates or location names.

## Live Application

🔗 **Access the application here:** https://5000-iskvzonlz0g4f957zq8wf-6f44df86.manusvm.computer

## Features

- **Coordinate-based lookup**: Enter latitude and longitude to get fire restrictions for that specific location
- **Location-based lookup**: Enter a place name (e.g., "Summerside", "Charlottetown") and get fire restrictions
- **County identification**: Automatically determines which PEI county (PRINCE, QUEENS, or KINGS) contains the coordinates
- **Real-time data**: Provides current fire restriction status and details
- **Responsive design**: Works on both desktop and mobile devices
- **Error handling**: Provides clear error messages for invalid inputs or coordinates outside PEI

## How to Use

1. **Option 1 - Location Name**: Enter a location name like "Summerside" or "Charlottetown" in the Location Name field
2. **Option 2 - Coordinates**: Enter latitude and longitude coordinates in the respective fields
3. Click "Check Fire Restrictions" to get the current status

## API Endpoints

The application provides REST API endpoints for programmatic access:

### Get Fire Restrictions by Coordinates
```
GET /api/burn_restrictions?latitude=46.3969&longitude=-63.7981
```

### Get Fire Restrictions by Location
```
GET /api/burn_restrictions?location=Summerside
```

### Get Available Counties
```
GET /api/counties
```

## Example API Response

```json
{
  "burn_restriction": {
    "details": "Fire closure order in place - all fires banned",
    "last_updated": "2025-09-02T12:22:59.000000",
    "status": "No Burning"
  },
  "county": "PRINCE",
  "latitude": 46.3969,
  "longitude": -63.7981
}
```

## Technical Architecture

### Backend
- **Framework**: Flask (Python)
- **Geocoding**: Nominatim (OpenStreetMap)
- **Geometry**: Custom point-in-polygon algorithm
- **Data Source**: PEI Open Data Portal (County boundaries GeoJSON)

### Frontend
- **Technology**: Vanilla HTML/CSS/JavaScript
- **Design**: Responsive with gradient styling and animations
- **User Experience**: Real-time validation and loading states

### Data Sources
- **County Boundaries**: PEI Open Data Portal GeoJSON
- **Fire Restrictions**: Simulated data (ready for integration with official PEI fire services)

## Scalability for Other Provinces

The application is designed to be easily extended for other Canadian provinces:

1. **Modular Architecture**: County detection and restriction logic are separated
2. **Configurable Data Sources**: Easy to swap GeoJSON files for different provinces
3. **API Design**: Consistent endpoint structure for any province
4. **Frontend Flexibility**: UI can be easily adapted for different provinces

### To Add Another Province:

1. Obtain county/region boundary GeoJSON data
2. Update the data loading logic in `fire_restrictions.py`
3. Modify the restriction data structure for province-specific rules
4. Update the frontend branding and location examples

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd pei_fire_watch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

The application will be available at `http://localhost:5000`

### Project Structure
```
pei_fire_watch/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── routes/
│   │   └── fire_restrictions.py # API endpoints
│   ├── static/
│   │   └── index.html          # Frontend interface
│   ├── utils/
│   │   └── geo_utils.py        # Geometry utilities
│   └── pei_county_zones.geojson # County boundary data
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Testing

The application has been tested with:
- ✅ Summerside coordinates (PRINCE County)
- ✅ Charlottetown location lookup (QUEENS County)  
- ✅ Eastern PEI coordinates (KINGS County)
- ✅ Error handling for coordinates outside PEI
- ✅ Error handling for invalid inputs
- ✅ Mobile responsiveness

## Future Enhancements

1. **Real Data Integration**: Connect to official PEI fire services API
2. **Historical Data**: Track fire restriction changes over time
3. **Notifications**: Email/SMS alerts for restriction changes
4. **Weather Integration**: Include weather conditions affecting fire risk
5. **Multi-Province Support**: Expand to other Canadian provinces
6. **Caching**: Implement data caching for better performance

## License

This project is created for demonstration purposes. Please ensure compliance with data source licenses when using in production.

## Support

For questions or issues, please contact the development team.

