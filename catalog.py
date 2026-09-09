# Here we are using the STAC API with the help of
# Microsoft Planetary Computer, which provides access
# to various open geospatial datasets.

# Sentinel-2 is a high-resolution multispectral Earth
# observation mission that systematically acquires
# optical imagery of land and coastal areas to monitor
# environmental changes.


from pystac_client import Client


STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"


def connect_to_catalog():
    """
    Connect to the Microsoft Planetary Computer STAC catalogue.
    """

    catalog = Client.open(STAC_URL)

    return catalog


def search_scenes(
    catalog,
    aoi,
    start_date,
    end_date,
    max_cloud_cover=60
):
    """
    Search Sentinel-2 scenes that intersect the AOI
    within a given date range and cloud-cover limit.
    """

    bbox = [
        aoi["west"],
        aoi["south"],
        aoi["east"],
        aoi["north"]
    ]

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start_date}/{end_date}",
        query={
            "eo:cloud_cover": {
                "lt": max_cloud_cover
            }
        },
        max_items=10
    )

    return list(search.items())


def select_scene(scenes):
    """
    Select the scene with the lowest cloud cover.
    """

    if not scenes:
        return None

    return min(
        scenes,
        key=lambda scene: scene.properties.get(
            "eo:cloud_cover",
            100
        )
    )


if __name__ == "__main__":

    catalog = connect_to_catalog()

    print("Connected to STAC catalogue.")
    print(f"Catalogue title: {catalog.title}")

    collection = catalog.get_collection(
        "sentinel-2-l2a"
    )

    print(f"Collection ID: {collection.id}")
    print(f"Collection title: {collection.title}")

    test_aoi = {
        "west": 85.7894521,
        "south": 20.2102964,
        "east": 85.8894521,
        "north": 20.3102964
    }

    scenes = search_scenes(
        catalog,
        test_aoi,
        "2026-08-01",
        "2026-09-05",
        max_cloud_cover=60
    )

    print(f"\nFound {len(scenes)} suitable scenes.")

    for scene in scenes:

        print("\nScene ID:", scene.id)
        print("Date:", scene.datetime)
        print(
            "Cloud cover:",
            scene.properties.get("eo:cloud_cover")
        )

    selected_scene = select_scene(scenes)

    if selected_scene:

        print("\n--- Selected Scene ---")
        print("Scene ID:", selected_scene.id)
        print("Date:", selected_scene.datetime)
        print(
            "Cloud cover:",
            selected_scene.properties.get(
                "eo:cloud_cover"
            )
        )

        print("\n--- Available Assets ---")

        for asset_name, asset in selected_scene.assets.items():
            print(
                f"{asset_name}: {asset.title}"
            )

    else:

        print("\nNo suitable scenes found.")

        print(
            "Try widening the date range "
            "or increasing the cloud threshold."
        )