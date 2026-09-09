import matplotlib
# Use a non-interactive backend so this module works both in a
# CLI context (plt.show()) and in a web-server context (no display,
# figures rendered to an in-memory PNG buffer instead).
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import io
import base64

from shapely.geometry import box
from rasterio.warp import transform_bounds


def create_aoi_geometry(aoi):
    """
    Create the AOI polygon from its bounding coordinates.
    """

    return box(
        aoi["west"],
        aoi["south"],
        aoi["east"],
        aoi["north"]
    )


def _build_rgb_figure(
    b02,
    b03,
    b04,
    profile,
    aoi
):
    """
    Build the Sentinel-2 RGB-with-AOI figure.

    Shared by the CLI display function and the web
    render function so the plotting logic exists once.
    """

    # Convert bands to floating point
    b02 = b02.astype(float)
    b03 = b03.astype(float)
    b04 = b04.astype(float)

    # Stretch each band independently
    def stretch_band(band):
        low, high = np.percentile(band, (2, 98))

        return np.clip(
            (band - low) / (high - low),
            0,
            1
        )

    red = stretch_band(b04)
    green = stretch_band(b03)
    blue = stretch_band(b02)

    # Create RGB image
    rgb = np.dstack(
        (red, green, blue)
    )

    # Raster bounds in Sentinel-2 CRS
    left, bottom, right, top = transform_bounds(
        profile["crs"],
        "EPSG:4326",
        profile["transform"].c,
        profile["transform"].f
        + profile["transform"].e * profile["height"],
        profile["transform"].c
        + profile["transform"].a * profile["width"],
        profile["transform"].f
    )

    # Create AOI
    aoi_geometry = create_aoi_geometry(aoi)

    aoi_gdf = gpd.GeoDataFrame(
        {"name": ["AOI"]},
        geometry=[aoi_geometry],
        crs="EPSG:4326"
    )

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.imshow(
        rgb,
        extent=[
            left,
            right,
            bottom,
            top
        ]
    )

    aoi_gdf.boundary.plot(
        ax=ax,
        linewidth=2
    )

    ax.set_title(
        "Sentinel-2 RGB Image with AOI"
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    return fig


def visualize_rgb_with_aoi(
    b02,
    b03,
    b04,
    profile,
    aoi
):
    """
    Display Sentinel-2 RGB imagery with the AOI boundary.
    (CLI usage.)
    """

    _build_rgb_figure(b02, b03, b04, profile, aoi)
    plt.show()


def render_rgb_with_aoi(
    b02,
    b03,
    b04,
    profile,
    aoi
):
    """
    Render Sentinel-2 RGB imagery with the AOI boundary
    to a base64-encoded PNG string. (Web usage.)
    """

    fig = _build_rgb_figure(b02, b03, b04, profile, aoi)
    return _figure_to_base64_png(fig)


def _build_ndvi_figure(
    ndvi,
    profile,
    aoi
):
    """
    Build the NDVI-with-AOI figure.

    Shared by the CLI display function and the web
    render function so the plotting logic exists once.
    """

    left, bottom, right, top = transform_bounds(
        profile["crs"],
        "EPSG:4326",
        profile["transform"].c,
        profile["transform"].f
        + profile["transform"].e * profile["height"],
        profile["transform"].c
        + profile["transform"].a * profile["width"],
        profile["transform"].f
    )

    aoi_geometry = create_aoi_geometry(aoi)

    aoi_gdf = gpd.GeoDataFrame(
        {"name": ["AOI"]},
        geometry=[aoi_geometry],
        crs="EPSG:4326"
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    image = ax.imshow(
        ndvi,
        extent=[
            left,
            right,
            bottom,
            top
        ],
        vmin=-1,
        vmax=1
    )

    aoi_gdf.boundary.plot(
        ax=ax,
        linewidth=2
    )

    plt.colorbar(
        image,
        ax=ax,
        label="NDVI"
    )

    ax.set_title("NDVI Map with AOI")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    return fig


def visualize_ndvi(
    ndvi,
    profile,
    aoi
):
    """
    Display the NDVI map with the AOI boundary.
    (CLI usage.)
    """

    _build_ndvi_figure(ndvi, profile, aoi)
    plt.show()


def render_ndvi(
    ndvi,
    profile,
    aoi
):
    """
    Render the NDVI map with the AOI boundary to a
    base64-encoded PNG string. (Web usage.)
    """

    fig = _build_ndvi_figure(ndvi, profile, aoi)
    return _figure_to_base64_png(fig)


def _figure_to_base64_png(fig):
    """
    Encode a Matplotlib figure as a base64 PNG string
    and close the figure to free memory.
    """

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=120)
    plt.close(fig)

    buffer.seek(0)

    encoded = base64.b64encode(
        buffer.read()
    ).decode("utf-8")

    return f"data:image/png;base64,{encoded}"