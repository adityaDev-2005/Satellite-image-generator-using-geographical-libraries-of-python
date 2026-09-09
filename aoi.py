# we will be creating bounding boxes around the region by calculating the 4 directions coordinates

def create_bounding_box(latitude, longitude, half_size=0.05):
    """
    Create a bounding-box AOI around a geographic point.

    Parameters:
        latitude (float): Latitude of the center point.
        longitude (float): Longitude of the center point.
        half_size (float): Half the width/height of the AOI in degrees.

    Returns:
        dict: Bounding box containing west, south, east, and north.
    """

    return {
        "west": longitude - half_size,
        "south": latitude - half_size,
        "east": longitude + half_size,
        "north": latitude + half_size
    }


if __name__ == "__main__":
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))

    aoi = create_bounding_box(latitude, longitude)

    print("\nAOI bounding box:")
    print(f"West  : {aoi['west']}")
    print(f"South : {aoi['south']}")
    print(f"East  : {aoi['east']}")
    print(f"North : {aoi['north']}")