import requests

# Function to get the earthquake data from USGS
def get_earthquake_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None

# Pytest for checking if the USGS API is accessible
def test_usgs_api_accessible():
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'
    r = requests.get(url)
    assert r.status_code == 200, "USGS API is not accessible."

# Pytest for checking if the data is correctly parsed and contains valid information
def test_earthquake_data_parsing():
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'
    theJson = get_earthquake_data(url)
    assert theJson is not None, "Failed to retrieve earthquake data from USGS."

    assert isinstance(theJson, dict), "Parsed JSON data is not a dictionary."
    assert 'metadata' in theJson, "JSON data does not contain 'metadata' key."
    assert 'features' in theJson, "JSON data does not contain 'features' key."

    quake_count = theJson['metadata']['count']
    assert isinstance(quake_count, int), "Quake count is not an integer."
    assert quake_count >= 0, "Invalid quake count value."

    for i in range(quake_count):
        assert 'properties' in theJson['features'][i], "Quake data does not contain 'properties' key."
        assert 'geometry' in theJson['features'][i], "Quake data does not contain 'geometry' key."

        properties = theJson['features'][i]['properties']
        assert 'place' in properties, "Quake properties do not contain 'place' key."
        assert 'mag' in properties, "Quake properties do not contain 'mag' key."

        geometry = theJson['features'][i]['geometry']
        assert 'coordinates' in geometry, "Quake geometry does not contain 'coordinates' key."

        coordinates = geometry['coordinates']
        assert isinstance(coordinates, list), "Quake coordinates are not in the list format."
        assert len(coordinates) == 3, "Invalid number of coordinates for the earthquake."

        for coord in coordinates:
            assert isinstance(coord, (int, float)), "Invalid type for coordinate value."

# Note: These tests assume that the USGS API returns data in a valid GeoJSON format.
