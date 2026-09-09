import rasterio
import planetary_computer
import numpy as np

from rasterio.warp import transform_bounds, reproject, Resampling


def read_band(asset, aoi):
    """
    Read only the portion of a Sentinel-2 raster
    that overlaps the AOI.
    """

    signed_asset = planetary_computer.sign(asset)

    with rasterio.open(signed_asset.href) as src:

        bounds = transform_bounds(
            "EPSG:4326",
            src.crs,
            aoi["west"],
            aoi["south"],
            aoi["east"],
            aoi["north"]
        )

        window = rasterio.windows.from_bounds(
            *bounds,
            transform=src.transform
        )

        data = src.read(1, window=window)

        window_transform = src.window_transform(window)

        profile = src.profile.copy()

        profile.update(
            height=data.shape[0],
            width=data.shape[1],
            transform=window_transform
        )

        return data, profile, src.crs


def align_scl_to_band(scl_data, scl_profile, target_profile):
    """
    Resample SCL data onto the same grid as a 10 m band.
    """

    aligned_scl = np.empty(
        (
            target_profile["height"],
            target_profile["width"]
        ),
        dtype=scl_data.dtype
    )

    reproject(
        source=scl_data,
        destination=aligned_scl,
        src_transform=scl_profile["transform"],
        src_crs=scl_profile["crs"],
        dst_transform=target_profile["transform"],
        dst_crs=target_profile["crs"],
        resampling=Resampling.nearest
    )

    return aligned_scl


def create_valid_mask(scl_data):
    """
    Create a mask for valid pixels using SCL classes.

    True  = keep pixel
    False = remove pixel
    """

    invalid_classes = [
        0,
        1,
        2,
        3,
        7,
        8,
        9,
        10,
        11
    ]

    mask = ~np.isin(
        scl_data,
        invalid_classes
    )

    return mask


def apply_mask(b04_data, b08_data, valid_mask):
    """
    Mask invalid pixels from the Red and NIR bands.
    """

    b04_clean = np.where(
        valid_mask,
        b04_data,
        np.nan
    )

    b08_clean = np.where(
        valid_mask,
        b08_data,
        np.nan
    )

    return b04_clean, b08_clean


def read_rgb(scene, aoi):
    """
    Read Sentinel-2 Blue, Green and Red bands
    for the given AOI.
    """

    b02_data, _, _ = read_band(
        scene.assets["B02"],
        aoi
    )

    b03_data, _, _ = read_band(
        scene.assets["B03"],
        aoi
    )

    b04_data, b04_profile, _ = read_band(
        scene.assets["B04"],
        aoi
    )

    return (
        b02_data,
        b03_data,
        b04_data,
        b04_profile
    )


def retrieve_scene_data(scene, aoi):
    """
    Retrieve and prepare the Sentinel-2 data
    required for RGB visualization and NDVI analysis.
    """

    # Read Red and NIR bands
    b04_data, b04_profile, _ = read_band(
        scene.assets["B04"],
        aoi
    )

    b08_data, _, _ = read_band(
        scene.assets["B08"],
        aoi
    )

    # Read Scene Classification Layer
    scl_data, scl_profile, _ = read_band(
        scene.assets["SCL"],
        aoi
    )

    # Align SCL to the 10 m B04 grid
    aligned_scl = align_scl_to_band(
        scl_data,
        scl_profile,
        b04_profile
    )

    # Create valid-pixel mask
    valid_mask = create_valid_mask(
        aligned_scl
    )

    # Apply mask to Red and NIR
    b04_clean, b08_clean = apply_mask(
        b04_data,
        b08_data,
        valid_mask
    )

    # Read Blue and Green for RGB
    b02_data, _, _ = read_band(
        scene.assets["B02"],
        aoi
    )

    b03_data, _, _ = read_band(
        scene.assets["B03"],
        aoi
    )

    return {
        "b02": b02_data,
        "b03": b03_data,
        "b04": b04_data,
        "b08": b08_data,
        "b04_clean": b04_clean,
        "b08_clean": b08_clean,
        "valid_mask": valid_mask,
        "profile": b04_profile
    }