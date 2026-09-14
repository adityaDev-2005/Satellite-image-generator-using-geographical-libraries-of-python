Sentinel-2 Remote Sensing and NDVI Analysis
A Flask-based remote sensing application for analyzing Sentinel-2 satellite imagery using natural-language queries.
The application accepts a location-based query, identifies the requested analysis, retrieves suitable Sentinel-2 Level-2A imagery from Microsoft Planetary Computer, generates an Area of Interest (AOI), calculates NDVI, and presents the results through a web interface.
Overview
The application provides a simple workflow for accessing and analyzing Earth observation data without requiring users to manually provide coordinates or work directly with satellite data catalogs and raster bands.
Example queries:
vegetation near Vijayawada
vegetation around Guntur
forest near Bengaluru
trees around Chennai
ndvi near Vijayawada
The application processes the query through the following workflow:
User Query
    ↓
Query Parser
    ↓
Location Geocoding
    ↓
AOI Generation
    ↓
Sentinel-2 Scene Retrieval
    ↓
B02 / B03 / B04 / B08 + SCL
    ↓
NDVI Calculation
    ↓
RGB + NDVI Visualization
    ↓
Statistics + Metadata
    ↓
NDVI Interpretation
Features
Natural-language query parsing
Location geocoding
Automatic Area of Interest generation
Sentinel-2 Level-2A imagery retrieval
Microsoft Planetary Computer integration
RGB satellite image generation
NDVI calculation
NDVI visualization
NDVI statistics
Sentinel-2 scene metadata
Geographical AOI map
Simple NDVI interpretation
Image viewing and download functionality
Flask-based web interface
Example Queries
Supported Queries
vegetation near Vijayawada
vegetation around Vijayawada
vegetation in Vijayawada
vegetation of Vijayawada
vegetation area near Guntur
vegetated area around Guntur
green areas in Vijayawada
forest near Bengaluru
trees around Chennai
ndvi near Vijayawada
The query parser supports vegetation-related terms such as:
vegetation
vegetation area
vegetated area
green area
green areas
forest
forest area
trees
tree cover
vegetation cover
ndvi
vegetation index
Unsupported Queries
Queries without a supported analysis type are rejected.
Examples:
Vijayawada
urban area near Delhi
water near Chennai
Remote Sensing Methodology
The application uses Sentinel-2 Level-2A imagery for remote sensing analysis.
The following Sentinel-2 bands are used:
Band
Description
Usage
B02
Blue
RGB visualization
B03
Green
RGB visualization
B04
Red
RGB visualization and NDVI
B08
Near Infrared
NDVI
SCL
Scene Classification Layer
Scene information
RGB Visualization
A natural-color RGB image is generated using the following Sentinel-2 bands:
Red   → B04
Green → B03
Blue  → B02
The individual bands are normalized using percentile-based stretching before being combined into the RGB image.
NDVI Calculation
The Normalized Difference Vegetation Index (NDVI) is calculated using the Red and Near-Infrared bands.
The NDVI formula is:
NDVI = (NIR - Red) / (NIR + Red)
For Sentinel-2:
NIR → B08
Red → B04
Therefore:
NDVI = (B08 - B04) / (B08 + B04)
NDVI values generally range from approximately -1 to +1.
Higher positive values generally indicate a stronger vegetation response.
NDVI Interpretation
The application provides a simple interpretation based on the mean NDVI value.
Mean NDVI
Interpretation
< 0
Very low
0 – 0.2
Low
0.2 – 0.4
Moderate
0.4 – 0.6
Strong
≥ 0.6
Very strong
These values provide a general interpretation of vegetation response and should not be treated as universal thresholds for specific crops, ecosystems, or land-cover classes.
NDVI is not a direct measurement of crop health, yield, or biomass.
Satellite Data
Satellite imagery is retrieved from the Microsoft Planetary Computer STAC catalog.
The application searches for suitable Sentinel-2 Level-2A scenes covering the generated Area of Interest and retrieves the required raster bands for analysis.
The processing pipeline uses:
Sentinel-2 Level-2A
B02
B03
B04
B08
SCL
Technologies Used
Programming Language
Python
Backend
Flask
Gunicorn
Geospatial and Remote Sensing
Rasterio
GeoPandas
Shapely
Contextily
Geopy
Satellite Data Access
PySTAC Client
Planetary Computer
Numerical Computing and Visualization
NumPy
Matplotlib
Frontend
HTML
CSS
JavaScript
Project Structure
Satellite-image-generator-using-geographical-libraries-of-python/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── web_app.py
├── query_parser.py
├── requirements.txt
├── .gitignore
└── README.md
File Description
web_app.py
Contains the main Flask web application.
It:
Receives user queries
Processes the requested analysis
Generates RGB and NDVI visualizations
Calculates NDVI statistics
Returns metadata and analysis results to the frontend
app.py
Contains the core satellite image processing and remote sensing analysis pipeline.
query_parser.py
Parses natural-language queries and extracts:
Analysis type
Location
It also validates whether the requested analysis is supported.
templates/index.html
Contains the main web application interface.
static/script.js
Handles frontend interactions, result rendering, NDVI interpretation, and image viewer functionality.
static/style.css
Contains the styling for the web interface.
requirements.txt
Contains the Python dependencies required to run the application.
Installation and Setup
1. Clone the Repository
git clone https://github.com/adityaDev-2005/Satellite-image-generator-using-geographical-libraries-of-python.git
Navigate to the project directory:
cd Satellite-image-generator-using-geographical-libraries-of-python
2. Create a Virtual Environment
python3 -m venv .venv
Activate the virtual environment.
Linux / macOS
source .venv/bin/activate
Windows
.venv\Scripts\activate
3. Install Dependencies
Upgrade pip:
python -m pip install --upgrade pip
Install the required dependencies:
pip install -r requirements.txt
Running the Application
Start the Flask development server:
python web_app.py
The application will be available at:
http://127.0.0.1:5000
Open the address in a web browser and enter a supported query.
Running with Gunicorn
For deployment or production-style execution, the application can be started using Gunicorn:
gunicorn web_app:app
Here:
web_app refers to web_app.py
app refers to the Flask application object
Output
After a successful analysis, the application provides the following results.
RGB Image
A natural-color satellite visualization generated from:
B04 → Red
B03 → Green
B02 → Blue
NDVI Map
A visualization of the calculated NDVI values within the selected Area of Interest.
NDVI Statistics
The application provides statistics including:
Minimum NDVI
Maximum NDVI
Mean NDVI
Median NDVI
Metadata
Information associated with the selected Sentinel-2 scene is displayed along with the analysis results.
AOI Map
The selected geographical location and generated Area of Interest are displayed on a map.
NDVI Interpretation
The application provides a simple interpretation based on the mean NDVI value.
Limitations
Results depend on the availability of suitable Sentinel-2 imagery.
Cloud cover and unsuitable scenes can affect image quality and analysis.
Geocoding accuracy depends on the location returned by the geocoding service.
NDVI interpretation is generalized and should not be used as a standalone measure of crop health or agricultural productivity.
The application currently focuses on vegetation and NDVI analysis.
The application does not perform temporal change detection.
The application does not perform machine-learning-based land-cover classification.
Future Improvements
Possible future improvements include:
Temporal NDVI analysis
Change detection
Additional spectral indices
Improved cloud masking
Multi-date satellite comparison
Land-cover classification
Advanced agricultural analysis
More precise AOI selection
Project Objective
The objective of this project is to provide a simple interface for accessing and analyzing Earth observation data.
The project demonstrates the integration of:
Geospatial processing
Remote sensing
Satellite data access
Raster analysis
Web application development
Data and Attribution
Satellite imagery used by this application is obtained from the Sentinel-2 mission through Microsoft Planetary Computer.
Sentinel-2 is part of the European Union's Copernicus Earth observation programme.
This project is intended for educational, research, and demonstration purposes.
