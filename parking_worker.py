

from logging import Logger
import re
from typing import Any

from googletrans import Translator
from google_maps_utils import GoogleMapsAPI
from parking_scraper import Parking_Scraper
from parking_utils import PARKING_URL_SPECIFIC_PREFIX, heb2eng_dict, ignored_parking_names


class Parking_Worker():
    def __init__(self) -> None:
        self.cls_root = 'parking/'
        self.cls_logger = Logger(__name__)
        self.gmps = GoogleMapsAPI()
        self.gtrn = Translator()
        self.ignored_parking_names = ignored_parking_names
        self.ps = Parking_Scraper()


    def get_parking_info(self,name_hebrew:str, address_hebrew:str) -> Any:
        if name_hebrew in (self.ignored_parking_names):
            self.cls_logger.error(f"could not find {name_hebrew} in google maps")
            return None
        name_english = self.gtrn.translate(name_hebrew, src='iw', dest='en').text
        address_gmaps_json = self.gmps.get_address_reponse(name_hebrew, address_hebrew, json_flag=True, oriented_flag=True)
        address_english = address_gmaps_json['formatted_address']
        geo_lat, geo_lng = self.gmps.get_lat_lng_from_json(address_gmaps_json, oriented=True)
        return name_english, address_english, geo_lat, geo_lng

    def get_parking_space_tonnage(self, parking_url_id) -> str:
        """get parking space tonnage of specific parking garage"""

        full_parking_url = PARKING_URL_SPECIFIC_PREFIX + parking_url_id
        parking_space_tonnage = self.ps.scrape_for_parking_space_tonnage(full_parking_url)
        # self.cls_logger.info(f"{parking_url_id} has {f}")
        return parking_space_tonnage