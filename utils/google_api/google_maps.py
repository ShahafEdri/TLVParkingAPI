import os
import requests
from utils.google_api import get_google_api_key

URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"


class GoogleMapsAPI():
    def __init__(self):
        self.url = URL
        self.params = {
            "language": "en",
            "fields": "formatted_address,name,geometry",
            "input": "",  # the address
            "inputtype": "textquery",
            "key": get_google_api_key()
        }

    def get_address_reponse(self, address="", json_flag=False, text_flag=False, oriented_flag=False):
        """
        get the response of the address
        :param address: the address on which to return the address
        :param json: if true return the response in json format
        :param text: if true return the response in text format
        :param oriented_flag: if true return the json response oriented_flag straight to the match result
        """
        self.params['input'] = address  # that would save the last address used in the search
        response = requests.request("GET", URL, params=self.params)
        response_json = response.json()
        if not response.ok:
            print(response.text)
            raise Exception("Error in get_address_reponse")
        elif response_json['status'] == 'ZERO_RESULTS':
            raise ValueError("No results found, wrong address?")
        else:
            return self.reponse_parser(response, response_json, json_flag, oriented_flag, text_flag)

    def reponse_parser(self, response, response_json, json_flag, oriented_flag, text_flag):
        if json_flag:
            if oriented_flag:
                return response_json["candidates"][0]
            else:
                return response_json
        elif text_flag:
            return response.text
        return response

    def get_lat_lng_from_json(self, json_response, oriented=False):
        if oriented == False:
            json_response = json_response["candidates"][0]
        lat = json_response['geometry']['location']['lat']
        lng = json_response['geometry']['location']['lng']
        return lat, lng


if __name__ == "__main__":
    gm = GoogleMapsAPI()
    location = "Arlozorov+17+tel-aviv"
    print(gm.get_address_reponse(address=location))
