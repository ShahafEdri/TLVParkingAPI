import re
from typing import Any, Dict, Optional
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
from google_maps_utils import GoogleMapsAPI
from parking_scraper import Parking_Scraper
from parking_utils import PARKING_URL_SPECIFIC_PREFIX, heb2eng_dict, PARKING_URL_ALL, ignored_parking_names
from logging import Logger
from logging import getLogger

from parking_worker import Parking_Worker


class ParkingManager():

    def __init__(self):
        self.cls_root = 'parking/'
        self.ignored_parking_names = ignored_parking_names
        self.cls_logger = Logger(__name__)
        self.ps = Parking_Scraper()
        self.pw = Parking_Worker()

    def get_parking_space_tonnage(self, parking_url_id) -> str:
        """get parking space tonnage of specific parking garage"""

        full_parking_url = PARKING_URL_SPECIFIC_PREFIX + parking_url_id
        parking_space_tonnage = self.ps.scrape_for_parking_space_tonnage(full_parking_url)
        # self.cls_logger.info(f"{parking_url_id} has {f}")
        return parking_space_tonnage

    def get_parking_garages_dict(self) -> Optional[Dict[str, Dict[str, Any]]]:
        '''get all the parking garage names'''
        # self.cls_logger.info(f"find all parking garages in Ahuzot Hachof website")
        all_scrape_parking_matchs = self.ps.get_html_list_of_all_parking_garages(url=PARKING_URL_ALL)
        # self.cls_logger.info(f"{len(all_scrape_parking_matchs)} parking garages found")

        # self.cls_logger.info(f"scraping data from Ahuzot Hachof website")
        parking_names_and_locations = dict()
        for match in all_scrape_parking_matchs:
            url_id, name_hebrew, address_hebrew = self.ps.parking_data_scraping(match_parent=match)
            if name_hebrew in (self.ignored_parking_names):
                self.cls_logger.error(f"could not find {name_hebrew} in google maps")
                continue
            name_english, address_english, geo_lat, geo_lng = self.pw.get_parking_info(name_hebrew, address_hebrew)

            # dict_name = name_english.lower().replace(' ', '_')
            parking_names_and_locations[url_id] = {
                "parking_space_id": url_id,
                "name_hebrew": name_hebrew,
                "name_english": name_english,
                "address_hebrew": address_hebrew,
                "address_english": address_english,
                "geo_lat": geo_lat,
                "geo_lng": geo_lng,
            }
        # self.cls_logger.info(f"{len(parking_names_and_locations)} parking garages scraped")
        return parking_names_and_locations


if __name__ == "__main__":
    p = ParkingManager()
    # while(True):
    #     parking_garage = "Arlozorov"
    #     pst = p.get_parking_space_tonnage(str(Parking_Names_Tlv_Dict[parking_garage]))  # pst=parking_space_tonnage
    #     print(f"parking_garage => {parking_garage}, status => {pst}")
    #     sleep(10)

    parking_names_dict = p.get_parking_garages_dict()
    print(parking_names_dict)
