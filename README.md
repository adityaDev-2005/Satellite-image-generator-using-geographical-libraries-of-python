Sentinel-2 Remote Sensing & NDVI Analysis

A query-driven Earth observation web application that allows users to describe a location and vegetation analysis request in natural language.

The application converts the user's query into a structured request, identifies the location using geocoding, retrieves suitable Sentinel-2 L2A satellite imagery from Microsoft Planetary Computer, calculates NDVI, and presents the results through visualizations, statistics, metadata, and a simple interpretation.

Features

Natural-language geographic queries

Location geocoding using OpenStreetMap Nominatim

Automatic Area of Interest (AOI) generation

Sentinel-2 L2A imagery retrieval

Cloud-aware satellite scene selection

True-color RGB visualization

NDVI calculation and visualization

NDVI minimum, mean, and maximum statistics

Simple NDVI interpretation

Cloud and invalid-pixel masking

Interactive AOI map

Satellite scene metadata

Image viewer with zoom and pan

PNG image download

Project Workflow

User Query
    |
    v
Query Parser
    |
    v
Location Geocoding
    |
    v
Area of Interest (AOI)
    |
    v
Sentinel-2 Scene Search
    |
    v
Satellite Band Retrieval
    |
    +----------------------+
    |                      |
    v                      v
RGB Visualization       NDVI Calculation
                            |
                            v
                     NDVI Visualization
                            |
                            v
                  Statistics & Interpretation
                            |
                            v
                       Web Dashboard

Example Queries

The application accepts several natural-language forms of vegetation queries.

vegetation near Vijayawada
vegetation around Vijayawada
vegetation in Vijayawada
vegetation of Vijayawada

vegetation area near Guntur
vegetated area around Guntur
green areas in Hyderabad
forest near Bengaluru
trees around Chennai
tree cover in Delhi
ndvi near Colombo

The query parser normalizes different expressions into a supported vegetation/NDVI analysis.

Remote Sensing Methodology

Sentinel-2

The application uses Copernicus Sentinel-2 Level-2A imagery.

The application uses the following bands:

Band

Sentinel-2 Band

Used for

Blue

B02

RGB visualization

Green

B03

RGB visualization

Red

B04

RGB visualization and NDVI

Near-Infrared

B08

NDVI

NDVI

The Normalized Difference Vegetation Index (NDVI) is calculated using the Red and Near-Infrared bands:

NDVI = (NIR - Red) / (NIR + Red)

For Sentinel-2:

NDVI = (B08 - B04) / (B08 + B04)

NDVI generally ranges from -1 to +1.

Higher positive values generally indicate a stronger vegetation response, while lower or negative values may correspond to water, bare land, built-up surfaces, or other non-vegetated areas.

The application provides:

Minimum NDVI

Mean NDVI

Maximum NDVI

along with a simple interpretation of the mean NDVI.

Note: NDVI is used here as a vegetation signal. It should not be interpreted as a direct measurement of crop health, yield, or biomass.

Satellite Data

Satellite imagery is accessed through the Microsoft Planetary Computer STAC catalog.

The application searches for Sentinel-2 L2A scenes covering the generated AOI and selects a suitable observation based on cloud-cover information.

The application also displays metadata including:

Scene ID

Acquisition date

Cloud cover

Latitude

Longitude

AOI coordinates

Technologies Used

Backend

Python

Flask

NumPy

Rasterio

GeoPandas

Shapely

Matplotlib

GeoPy

PySTAC Client

Planetary Computer

Gunicorn

Frontend

HTML

CSS

JavaScript

Leaflet.js

Data Sources

Copernicus Sentinel-2 L2A

Microsoft Planetary Computer

OpenStreetMap / Nominatim

Running the Project Locally

1. Clone the Repository

git clone https://github.com/adityaDev-2005/Satellite-image-generator-using-geographical-libraries-of-python.git

Move into the project directory:

cd Satellite-image-generator-using-geographical-libraries-of-python

2. Create a Virtual Environment

It is recommended to use a Python virtual environment.

Linux / macOS

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Windows

python -m venv .venv

Activate it:

.venv\Scripts\activate

3. Install Dependencies

Upgrade pip:

python -m pip install --upgrade pip

Install the required packages:

pip install -r requirements.txt

4. Run the Application

Start the Flask web application:

python web_app.py

The application will start on:

http://127.0.0.1:5000

Open the address in a web browser.

5. Run with Gunicorn

For a production-style run, Gunicorn can be used:

gunicorn web_app:app

The entry point is:

web_app:app

where:

web_app refers to web_app.py

app refers to the Flask application object

Project Structure

Satellite-image-generator-using-geographical-libraries-of-python/
│
├── app.py

├── analysis.py

├── aoi.py

├── catalog.py

├── geocoding.py

├── imagery.py

├── query_parser.py

├── visualization.py

├── web_app.py
│
├── static/

│   ├── script.js

│   └── style.css
│
├── templates/

│   └── index.html
│
├── requirements.txt

├── .gitignore

├── .python-version

└── README.md

Main Modules

query_parser.py

Converts natural-language queries into structured analysis and location information.

geocoding.py

Converts the requested place into geographic coordinates using Nominatim.

aoi.py

Creates the geographic Area of Interest around the selected coordinates.

catalog.py

Searches the Sentinel-2 STAC catalog and selects a suitable satellite scene.

imagery.py

Retrieves the required Sentinel-2 bands.

analysis.py

Performs NDVI calculations and generates statistics.

visualization.py

Creates the RGB and NDVI visualizations.

app.py

Acts as the main remote-sensing pipeline and connects the individual processing modules.

web_app.py

Provides the Flask web interface and converts analysis results into browser-displayable responses.

static/script.js

Handles frontend interaction, result rendering, maps, image viewing, and NDVI interpretation.

templates/index.html

Contains the web dashboard structure.

Output

For a successful query, the application produces the following results.

1. Sentinel-2 RGB Image

A true-color composite using:

B04 / B03 / B02
Red / Green / Blue

The selected AOI is outlined on the image.

2. NDVI Map

A spatial NDVI visualization showing the vegetation response across the selected AOI.

Cloud and invalid pixels are masked where applicable.

3. NDVI Statistics

Minimum
Mean
Maximum

4. Quick Interpretation

The application provides a simple interpretation based on the mean NDVI value.

5. Geographic Information

The dashboard displays:

Location

Address

Coordinates

AOI

Interactive map

6. Satellite Metadata

The selected Sentinel-2 scene information is displayed, including:

Scene ID

Acquisition date

Cloud cover

NDVI Interpretation

The application provides a general interpretation of the mean NDVI value.

Mean NDVI

General interpretation

< 0.0

Very low vegetation signal

0.0 – < 0.2

Low vegetation signal

0.2 – < 0.4

Moderate vegetation signal

0.4 – < 0.6

Strong vegetation signal

≥ 0.6

Very strong vegetation signal

These categories are intended as a simple interpretation of the vegetation signal, not as strict land-cover or crop-health classifications.

Limitations

This project is intended as an Earth observation and remote-sensing analysis application rather than a precision agricultural monitoring system.

Some important limitations include:

Results depend on the availability and quality of Sentinel-2 observations.

Cloud cover can affect satellite observations.

NDVI alone cannot determine crop health, yield, or biomass.

The generated AOI is a fixed geographic bounding box around the geocoded location.

Geocoding results depend on the OpenStreetMap Nominatim service.

Satellite data retrieval and processing require an active internet connection.

Large or complex AOIs may require additional processing time.

Future Improvements

Potential future extensions include:

Temporal vegetation monitoring

Multi-date NDVI comparison

Additional spectral indices

More advanced AOI selection

Improved cloud and atmospheric-quality handling

Time-series visualization

Additional Earth observation datasets

These are intentionally outside the current core implementation.

Data & Attribution

Sentinel-2

Satellite imagery is provided by the Copernicus Sentinel-2 mission.

Microsoft Planetary Computer

Satellite data is accessed through the Microsoft Planetary Computer STAC catalog.

OpenStreetMap / Nominatim

Geographic location search and geocoding use OpenStreetMap data through the Nominatim service.

Leaflet

The interactive geographic map uses Leaflet.
