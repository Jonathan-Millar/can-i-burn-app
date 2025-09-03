# Canada Fire Watch

A comprehensive web application that provides current fire burn restriction information for all Canadian provinces and territories based on GPS coordinates or location names.


## Features

- **Canada-wide coverage**: Supports all 10 provinces and 3 territories
- **Coordinate-based lookup**: Enter latitude and longitude to get fire restrictions for any location in Canada
- **Location-based lookup**: Enter a place name (e.g., "Vancouver", "Toronto", "Montreal") and get fire restrictions
- **Province & region detection**: Automatically determines which province/territory and county/region contains the coordinates
- **Real-time data**: Provides current fire restriction status and detailed information from official sources
- **Enhanced reporting**: Comprehensive fire watch reports with risk assessments and recommendations
- **Responsive design**: Works on both desktop and mobile devices
- **Error handling**: Provides clear error messages for invalid inputs or locations outside Canada

## Supported Provinces & Territories

### Provinces
- **British Columbia (BC)**: Fire centre detection, category-based restrictions, real-time data
- **Alberta (AB)**: Region detection, tiered restriction system, forest protection areas
- **Saskatchewan (SK)**: Municipality detection, multi-jurisdictional coordination
- **Manitoba (MB)**: Dual jurisdiction system, seasonal restrictions, municipal coordination
- **Ontario (ON)**: Fire zone restrictions, comprehensive coverage
- **Quebec (QC)**: SOPFEU system, fire danger index, zone-based restrictions, bilingual service
- **New Brunswick (NB)**: Enhanced reporting, multi-source data, risk assessment, recommendations
- **Nova Scotia (NS)**: County-based restrictions, province-wide status
- **Prince Edward Island (PEI)**: County detection, basic restrictions
- **Newfoundland and Labrador (NL)**: Province-wide bans, daily hazard updates, enhanced penalties

### Territories
- **Yukon (YT)**: Multi-level restrictions, territory-wide bans, seasonal fire management
- **Northwest Territories (NT)**: Fire danger ratings, community restrictions, territorial coordination
- **Nunavut (NU)**: Community management, burn permits, arctic fire conditions

## How to Use

1. **Option 1 - Location Name**: Enter a location name like "Vancouver", "Toronto", or "Montreal" in the Location Name field
2. **Option 2 - Coordinates**: Enter latitude and longitude coordinates in the respective fields
3. Click "Check Fire Restrictions" to get the current status

## API Endpoints

The application provides comprehensive REST API endpoints for programmatic access:

### Enhanced Fire Restrictions (All Provinces/Territories)
```
GET /api/enhanced/burn_restrictions?latitude=49.2827&longitude=-123.1207
GET /api/enhanced/burn_restrictions?location=Vancouver
```

### Province-Specific Enhanced Reports
```
GET /api/enhanced/nb_report?county=Saint John
GET /api/enhanced/nb_counties
GET /api/enhanced/ns_counties
```

### Legacy PEI Endpoints
```
GET /api/burn_restrictions?latitude=46.3969&longitude=-63.7981
GET /api/burn_restrictions?location=Summerside
```

### Province Information
```
GET /api/enhanced/provinces
```

## Example API Response

```json
{
  "latitude": 49.2827,
  "longitude": -123.1207,
  "province": "BC",
  "county": "Vancouver",
  "burn_restriction": {
    "status": "Category 1 Fires Allowed",
    "details": "Small campfires are permitted with proper safety measures",
    "source": "BC Wildfire Service",
    "last_updated": "2025-01-27T10:30:00",
    "enhanced_report": {
      "fire_centre": "Coastal",
      "category": 1,
      "restrictions": "Category 1 fires allowed with conditions"
    }
  }
}
```

## Technical Architecture

### Backend
- **Framework**: Flask (Python) with SQLAlchemy
- **Geocoding**: Nominatim (OpenStreetMap) with rate limiting
- **Province Detection**: Advanced coordinate-based province and county detection
- **Data Sources**: Official provincial/territorial fire services and government APIs
- **Database**: SQLite with user management capabilities

### Frontend
- **Technology**: Vanilla HTML/CSS/JavaScript
- **Design**: Responsive with gradient styling and animations
- **User Experience**: Real-time validation and loading states

### Data Sources
- **Provincial Boundaries**: OpenStreetMap and official government data
- **Fire Restrictions**: Real-time data from official provincial/territorial fire services
- **Enhanced Reports**: Comprehensive fire watch data including risk assessments

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
│   ├── main.py                           # Flask application entry point
│   ├── routes/
│   │   ├── fire_restrictions.py          # Legacy PEI API endpoints
│   │   ├── enhanced_fire_restrictions.py # Canada-wide enhanced API
│   │   └── user.py                       # User management endpoints
│   ├── models/
│   │   └── user.py                       # User database models
│   ├── database/
│   │   └── app.db                        # SQLite database
│   ├── static/
│   │   └── index.html                    # Frontend interface
│   ├── utils/
│   │   ├── geo_utils.py                  # Geometry utilities
│   │   ├── province_detector.py          # Province/territory detection
│   │   ├── enhanced_nb_scraper.py       # New Brunswick enhanced scraper
│   │   ├── ns_scraper.py                # Nova Scotia scraper
│   │   ├── ontario_scraper.py           # Ontario scraper
│   │   ├── bc_scraper.py                # British Columbia scraper
│   │   ├── alberta_scraper.py           # Alberta scraper
│   │   ├── saskatchewan_scraper.py      # Saskatchewan scraper
│   │   ├── manitoba_scraper.py          # Manitoba scraper
│   │   ├── quebec_scraper.py            # Quebec scraper
│   │   ├── newfoundland_scraper.py      # Newfoundland scraper
│   │   └── territories_scraper.py       # Territories scraper
│   ├── pei_county_zones.geojson         # PEI county boundary data
│   ├── nova_scotia_county_zones.geojson # Nova Scotia county data
│   └── new_brunswick_county_zones.geojson # New Brunswick county data
├── requirements.txt                      # Python dependencies
└── README.md                            # This file
```

## Testing

The application has been tested with:
- ✅ All 10 provinces and 3 territories
- ✅ Major cities across Canada (Vancouver, Toronto, Montreal, etc.)
- ✅ Rural and remote locations
- ✅ Error handling for coordinates outside Canada
- ✅ Error handling for invalid inputs
- ✅ Mobile responsiveness
- ✅ Enhanced reporting features

## Key Features by Province

### Enhanced Reporting (New Brunswick)
- Multi-source data integration
- Risk assessment and recommendations
- County-specific conditions
- Real-time updates

### Real-time Data (British Columbia)
- Fire centre detection
- Category-based restrictions
- Live data from BC Wildfire Service

### Advanced Systems (Quebec)
- SOPFEU integration
- Fire danger index
- Zone-based restrictions
- Bilingual service support

## Future Enhancements

1. **Real-time Integration**: Enhanced real-time data feeds from all provinces
2. **Historical Data**: Track fire restriction changes over time
3. **Notifications**: Email/SMS alerts for restriction changes
4. **Weather Integration**: Include weather conditions affecting fire risk
5. **Mobile App**: Native mobile applications for iOS and Android
6. **Caching**: Implement data caching for better performance
7. **API Rate Limiting**: Enhanced API management and monitoring
8. **Machine Learning**: Predictive fire risk modeling

## License

This project is created for demonstration purposes. Please ensure compliance with data source licenses when using in production.

## Support

For questions or issues, please contact the development team.

## Contributing

This project welcomes contributions! Please see our contributing guidelines for more information on how to submit pull requests, report issues, or suggest new features.

