import numpy as np
# import matplotlib.pyplot as plt

def calculate_ndvi(b04, b08):
    """
    Calculate NDVI from Red (B04) and NIR (B08) data.
    """

    denominator = b08 + b04

    ndvi = np.divide(
        b08 - b04,
        denominator,
        out=np.full_like(b04, np.nan, dtype=float),
        where=denominator != 0
    )

    return ndvi


def calculate_ndvi_statistics(ndvi):
    """
    Calculate basic statistics for valid NDVI pixels.
    """

    valid_ndvi = ndvi[~np.isnan(ndvi)]

    return {
        "min": np.min(valid_ndvi),
        "max": np.max(valid_ndvi),
        "mean": np.mean(valid_ndvi)
    }


# def visualize_ndvi(ndvi):
#     """
#     Display the NDVI raster.
#     """

#     plt.figure(figsize=(8, 8))

#     plt.imshow(ndvi, vmin=-1, vmax=1)

#     plt.colorbar(label="NDVI")
#     plt.title("NDVI Map")

#     plt.axis("off")
#     plt.show()



if __name__ == "__main__":


    from imagery import (
        read_band,
        align_scl_to_band,
        create_valid_mask,
        apply_mask
    )

    from visualization import visualize_ndvi

    from pystac_client import Client


    STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

    catalog = Client.open(STAC_URL)


    test_aoi = {
        "west": 85.7894521,
        "south": 20.2102964,
        "east": 85.8894521,
        "north": 20.3102964
    }


    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=[
            test_aoi["west"],
            test_aoi["south"],
            test_aoi["east"],
            test_aoi["north"]
        ],
        datetime="2026-08-01/2026-09-05",
        query={
            "eo:cloud_cover": {
                "lt": 60
            }
        },
        max_items=10
    )


    scenes = list(search.items())

    if not scenes:
        print("No suitable scenes found.")
        exit()


    selected_scene = min(
        scenes,
        key=lambda scene: scene.properties.get(
            "eo:cloud_cover",
            100
        )
    )


    b04_data, b04_profile, _ = read_band(
        selected_scene.assets["B04"],
        test_aoi
    )

    b08_data, _, _ = read_band(
        selected_scene.assets["B08"],
        test_aoi
    )

    scl_data, scl_profile, _ = read_band(
        selected_scene.assets["SCL"],
        test_aoi
    )


    aligned_scl = align_scl_to_band(
        scl_data,
        scl_profile,
        b04_profile
    )


    valid_mask = create_valid_mask(aligned_scl)


    b04_clean, b08_clean = apply_mask(
        b04_data,
        b08_data,
        valid_mask
    )


    ndvi = calculate_ndvi(
        b04_clean,
        b08_clean
    )


    stats = calculate_ndvi_statistics(ndvi)

    print("\n--- NDVI Statistics ---")
    print("Minimum:", stats["min"])
    print("Maximum:", stats["max"])
    print("Mean:", stats["mean"])

    visualize_ndvi(
        ndvi,
        b04_profile,
        test_aoi)


    print("\n--- NDVI Result ---")
    print("Shape:", ndvi.shape)
    print("Data type:", ndvi.dtype)