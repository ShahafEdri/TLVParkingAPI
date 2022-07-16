import requests

URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"


class GoogleMapsAPI():
    def __init__(self):
        self.url = URL
        self.params = {
            "language": "en",
            "fields": "formatted_address,name,geometry",
            "input": "",  # the address
            "inputtype": "textquery",
            "key": self.get_api_key()
        }

    # read file from pc and return the apikey as string
    @staticmethod
    def get_api_key():
        with open("C:/Users/shahafe/api_key.txt", "r") as f:
            api_key = f.read()
        return api_key

    def get_address_reponse(self, name=None, address="", json_flag=False, text_flag=False, oriented_flag=False):
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
            # return response_json['status']
            if address != name:
                return self.get_address_reponse(name, name, json_flag, text_flag, oriented_flag)
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

    def get_lat_lng(self, address):
        json = self.get_address_reponse(address=address)
        lat = json['candidates'][0]['geometry']['location']['lat']
        lng = json['candidates'][0]['geometry']['location']['lng']
        return lat, lng


if __name__ == "__main__":
    gm = GoogleMapsAPI()
    location = "Arlozorov+17+tel-aviv"
    print(gm.get_address_reponse(address=location))
