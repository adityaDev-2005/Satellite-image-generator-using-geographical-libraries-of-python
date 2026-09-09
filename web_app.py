"""
Flask web layer for the satellite remote-sensing pipeline.

This module handles ONLY:
  - HTTP routing
  - request/response (JSON) handling
  - converting NumPy array results into browser-displayable
    base64 PNG images

It does NOT contain any remote-sensing logic. The entire
pipeline (query parsing, geocoding, AOI, STAC search, band
retrieval, NDVI calculation) lives in app.py and the modules
it imports. process_query() is the single source of truth.
"""

import logging

from flask import Flask, render_template, request, jsonify

from app import process_query
from visualization import render_rgb_with_aoi, render_ndvi


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the dashboard page."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Run the remote-sensing pipeline for a user query and
    return a JSON-safe response (images as base64 PNG).
    """

    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()

    if not query:
        return jsonify({
            "success": False,
            "error": "Please enter a query."
        }), 400

    try:
        result = process_query(query)
    except Exception:
        # Never leak a traceback to the browser; log it
        # server-side for debugging instead.
        logger.exception(
            "process_query failed for query: %s", query
        )
        return jsonify({
            "success": False,
            "error": (
                "Something went wrong while processing "
                "this request. Please try again."
            )
        }), 500

    if not result["success"]:
        # Pass through the existing, already user-friendly
        # error messages produced by process_query().
        return jsonify(result), 200

    # Convert NumPy-array outputs into browser-displayable
    # images. This is the only place array -> PNG conversion
    # happens; the pipeline itself never deals with images.
    rgb_image = render_rgb_with_aoi(
        result["b02"],
        result["b03"],
        result["b04"],
        result["profile"],
        result["aoi"]
    )

    ndvi_image = render_ndvi(
        result["ndvi"],
        result["profile"],
        result["aoi"]
    )

    response = {
        "success": True,
        "analysis": result["analysis"],
        "location": result["location"],
        "address": result["address"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "aoi": result["aoi"],
        "scene_id": result["scene_id"],
        "acquisition_date": result["acquisition_date"],
        "cloud_cover": result["cloud_cover"],
        "ndvi_statistics": {
            "min": float(result["ndvi_statistics"]["min"]),
            "max": float(result["ndvi_statistics"]["max"]),
            "mean": float(result["ndvi_statistics"]["mean"])
        },
        "rgb_image": rgb_image,
        "ndvi_image": ndvi_image
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
