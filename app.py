from datetime import date, timedelta

from query_parser import parse_query
from geocoding import get_coordinates
from aoi import create_bounding_box
from catalog import (
    connect_to_catalog,
    search_scenes,
    select_scene
)
from imagery import retrieve_scene_data
from analysis import (
    calculate_ndvi,
    calculate_ndvi_statistics
)
from visualization import (
    visualize_rgb_with_aoi,
    visualize_ndvi
)


def process_query(query):
    """
    Process a geographic remote-sensing query
    and return the analysis results.
    """

    # -----------------------------------------
    # Step 1: Parse query
    # -----------------------------------------

    parsed_query = parse_query(query)

    if parsed_query is None:
        return {
            "success": False,
            "error": "Could not understand the query."
        }

    analysis = parsed_query["analysis"]
    location = parsed_query["location"]

    # -----------------------------------------
    # Step 2: Check supported analysis
    # -----------------------------------------

    if analysis not in ["vegetation", "ndvi"]:
        return {
            "success": False,
            "error": (
                f"Analysis '{analysis}' is not "
                "supported yet."
            )
        }

    # -----------------------------------------
    # Step 3: Geocode location
    # -----------------------------------------

    latitude, longitude, address = get_coordinates(
        location
    )

    if latitude is None:
        return {
            "success": False,
            "error": "Location could not be found."
        }

    # -----------------------------------------
    # Step 4: Create AOI
    # -----------------------------------------

    aoi = create_bounding_box(
        latitude,
        longitude
    )

    # -----------------------------------------
    # Step 5: Connect to STAC catalogue
    # -----------------------------------------

    catalog = connect_to_catalog()

    # -----------------------------------------
    # Step 6: Search Sentinel-2 scenes
    # -----------------------------------------

    end_date = date.today()

    start_date = end_date - timedelta(
        days=60
    )

    scenes = search_scenes(
        catalog,
        aoi,
        start_date.isoformat(),
        end_date.isoformat(),
        max_cloud_cover=60
    )

    # -----------------------------------------
    # Step 7: Widen date range if necessary
    # -----------------------------------------

    if not scenes:

        start_date = end_date - timedelta(
            days=120
        )

        scenes = search_scenes(
            catalog,
            aoi,
            start_date.isoformat(),
            end_date.isoformat(),
            max_cloud_cover=60
        )

    if not scenes:
        return {
            "success": False,
            "error": (
                "No suitable Sentinel-2 scenes "
                "were found."
            )
        }

    # -----------------------------------------
    # Step 8: Select scene
    # -----------------------------------------

    selected_scene = select_scene(scenes)

    if selected_scene is None:
        return {
            "success": False,
            "error": "Could not select a satellite scene."
        }

    # -----------------------------------------
    # Step 9: Retrieve satellite data
    # -----------------------------------------

    data = retrieve_scene_data(
        selected_scene,
        aoi
    )

    # -----------------------------------------
    # Step 10: Calculate NDVI
    # -----------------------------------------

    ndvi = calculate_ndvi(
        data["b04_clean"],
        data["b08_clean"]
    )

    # -----------------------------------------
    # Step 11: Calculate statistics
    # -----------------------------------------

    stats = calculate_ndvi_statistics(
        ndvi
    )

    # -----------------------------------------
    # Step 12: Return results
    # -----------------------------------------

    return {
        "success": True,
        "analysis": analysis,
        "location": location,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "aoi": aoi,
        "scene_id": selected_scene.id,
        "acquisition_date": (
            selected_scene.datetime.isoformat()
        ),
        "cloud_cover": selected_scene.properties.get(
            "eo:cloud_cover"
        ),
        "ndvi_statistics": stats,
        "ndvi": ndvi,
        "b02": data["b02"],
        "b03": data["b03"],
        "b04": data["b04"],
        "profile": data["profile"]
    }


def main():
    """
    Command-line interface for testing the pipeline.
    """

    query = input(
        "Enter your geographic query: "
    ).strip()

    print("\nProcessing query...")

    result = process_query(query)

    if not result["success"]:
        print(
            f"\n❌ {result['error']}"
        )
        return

    print("\n--- Query Interpretation ---")
    print(
        f"Analysis : {result['analysis']}"
    )
    print(
        f"Location : {result['location']}"
    )

    print("\n--- Geocoding Result ---")
    print(
        f"Address   : {result['address']}"
    )
    print(
        f"Latitude  : {result['latitude']}"
    )
    print(
        f"Longitude : {result['longitude']}"
    )

    print("\n--- AOI ---")
    print(
        f"West  : {result['aoi']['west']}"
    )
    print(
        f"South : {result['aoi']['south']}"
    )
    print(
        f"East  : {result['aoi']['east']}"
    )
    print(
        f"North : {result['aoi']['north']}"
    )

    print("\n--- Selected Scene ---")
    print(
        f"Scene ID    : {result['scene_id']}"
    )
    print(
        f"Acquisition : {result['acquisition_date']}"
    )
    print(
        f"Cloud cover : {result['cloud_cover']}"
    )

    print("\n--- NDVI Statistics ---")

    stats = result["ndvi_statistics"]

    print(
        f"Minimum : {stats['min']:.4f}"
    )
    print(
        f"Maximum : {stats['max']:.4f}"
    )
    print(
        f"Mean    : {stats['mean']:.4f}"
    )

    print(
        "\nDisplaying RGB satellite imagery..."
    )

    visualize_rgb_with_aoi(
        result["b02"],
        result["b03"],
        result["b04"],
        result["profile"],
        result["aoi"]
    )

    print(
        "\nDisplaying NDVI map..."
    )

    visualize_ndvi(
        result["ndvi"],
        result["profile"],
        result["aoi"]
    )

    print(
        "\n--- Processing Complete ---"
    )


if __name__ == "__main__":
    main()