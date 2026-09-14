🛰️ Satellite Image Generator & EO Analysis Tool

A Python-based Earth Observation (EO) tool that takes a natural-language place query, resolves it to an Area of Interest (AOI), fetches real satellite imagery via the Sentinel-2 STAC catalog, and generates true-color RGB visualizations and NDVI (vegetation index) analysis — all served through a Flask web dashboard.

Features

🔍 Natural-language query parsing — e.g. "vegetation near Vijayawada"
📍 Geocoding — place name → latitude/longitude → AOI bounding box
🛰️ Sentinel-2 STAC catalog search — finds and selects the best matching satellite scene
🎨 True-color RGB visualization — with AOI bounding box overlay
🌱 NDVI (vegetation index) analysis — with statistics and metadata
🌐 Web dashboard — dark EO-styled UI with an interactive Leaflet map, zoomable/pannable image viewer, and downloadable results

Project Structure
├── app.py                # Core CLI pipeline (process_query)

├── web_app.py             # Flask web server wrapping the pipeline

├── query_parser.py         # Natural-language query parsing

├── geocoding.py              # Place name → lat/lon

├── aoi.py                     # AOI bounding box generation

├── catalog.py                   # Sentinel-2 STAC catalog search

├── imagery.py                     # Scene/band retrieval

├── analysis.py                      # NDVI computation

├── visualization.py                   # RGB/NDVI rendering (CLI + base64 PNG for web)

├── templates/                          # Flask HTML templates

├── static/                              # CSS/JS for the dashboard

└── requirements.txt

Installation : 
Clone the repository : 

git clone https://github.com/adityaDev-2005/Satellite-image-generator-using-geographical-libraries-of-python.git

cd Satellite-image-generator-using-geographical-libraries-of-python

Create the virtual environment :

python -m venv venv

Activate the environment : 

source venv/bin/activate   # On Windows: venv\Scripts\activate

Install the dependencies : 
pip install -r requirements.txt

View the app : 

Option 1: Web Dashboard (recommended)

python web_app.py

Then open your browser to http://localhost:5000 and enter a query, for example:

vegetation near Vijayawada

Option 2: Command Line

python app.py

Follow the prompt to enter your query directly in the terminal.

Example Query
Query: vegetation near Cuttack

This will:

Geocode "Cuttack" to latitude/longitude
Build an AOI bounding box around it
Search the Sentinel-2 STAC catalog for the best matching scene
Retrieve the Red + NIR bands
Compute NDVI (vegetation index)
Render the RGB image (with AOI overlay) and NDVI map, along with statistics
Requirements

All dependencies are listed in requirements.txt, including geospatial, STAC, imaging, and Flask libraries.

Notes
Requires an internet connection to query the Sentinel-2 STAC catalog and the geocoding service.
Built as a lightweight, end-to-end EO workflow demonstration rather than a production-grade remote-sensing platform.
