import pytest
from utils.google_api import translator
from utils.google_api import google_maps_api


def test_translate():
    assert translator.translate('hello', src='en', dest='iw').text == 'שלום'


@pytest.mark.parametrize("input_address, expected_result", [
    ("Arlozorov St 17", {"formatted_address": "Arlozorov St 17, Tel Aviv-Yafo, Israel",
                         "lat": 32.0872133,
                         "lng": 34.7744164}),
])
def test_google_maps_api(input_address: str, expected_result: dict):
    rest = google_maps_api.get_address_reponse(address=input_address).json()
    assert all((rest["candidates"][0]['formatted_address'] == expected_result['formatted_address'],
                rest["candidates"][0]['geometry']['location']['lat'] == expected_result['lat'],
                rest["candidates"][0]['geometry']['location']['lng'] == expected_result['lng'])),\
        """check that the address is correct, and that the lat and lng are correct"""
