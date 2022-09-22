

from logging import Logger
import re
from typing import Any

from utils.google_api import translator, google_maps_api

from logic.parking.parking_scraper import ParkingScraper
from logic.parking.parking_utils import PARKING_URL_SPECIFIC_PREFIX, heb2eng_dict, ignored_parking_names
from utils.logging_utils import logger


class Parking_Worker():
    def __init__(self) -> None:
        self.cls_root = 'parking/'
        self.cls_logger = logger
        self.gmps = google_maps_api
        self.gtrns = translator
        self.ignored_parking_names = ignored_parking_names
        self.ps = ParkingScraper()

    def get_parking_info(self, name_hebrew: str, address_hebrew: str) -> Any:
        if name_hebrew in (self.ignored_parking_names):
            self.cls_logger.error(f"could not find {name_hebrew} in google maps")
            return None
        name_english = self.gtrns.translate(name_hebrew, src='iw', dest='en').text
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
