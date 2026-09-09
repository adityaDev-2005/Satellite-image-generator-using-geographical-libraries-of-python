# returns the lat and long of the places entered 

from geopy.geocoders import Nominatim
from functools import lru_cache


# Create the geocoder once and reuse it
geolocator = Nominatim(user_agent="satellite_remote_sensing_app")


# Cache previous geocoding results
# so repeated searches do not make another request
@lru_cache(maxsize=100)
def get_coordinates(place_name):
    """
    Convert a place name into latitude, longitude, and
    the full address returned by the geocoding service.
    """

    place_name = place_name.strip()

    location = geolocator.geocode(
        place_name,
        exactly_one=True,
        addressdetails=True
    )

    if location:
        return location.latitude, location.longitude, location.address

    return None, None, None


if __name__ == "__main__":
    place = input("Enter a place name: ").strip()

    lat, lon, address = get_coordinates(place)

    if lat is not None:
        print("\nLocation found:")
        print(f"Address   : {address}")
        print(f"Latitude  : {lat}")
        print(f"Longitude : {lon}")
    else:
        print("\n❌ Place not found.")