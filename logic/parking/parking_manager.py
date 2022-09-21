import multiprocessing as mp
import re
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup

from utils.google_api.google_translate_utils import 
from utils.google_api.google_maps import GoogleMapsAPI
from googletrans import Translator
from utils.general_utils import singleton
from utils.logging_utils import logger

from parking import parking_manger_obj
from parking.parking_scraper import (Parking_Scraper,
                                     worker_scrape_for_parking_space_tonnage)
from parking.parking_utils import (PARKING_URL_ALL,
                                   PARKING_URL_SPECIFIC_PREFIX, ParkingUtils,
                                   heb2eng_dict, ignored_parking_names)
from parking.parking_worker import Parking_Worker


@singleton
class ParkingManager():

    def __init__(self):
        self.cls_root = 'parking/'
        self.ignored_parking_names = ignored_parking_names
        self.cls_logger = logger
        self.ps = Parking_Scraper()
        self.pw = Parking_Worker()
        self.pu = ParkingUtils()

    def get_parking_space_tonnage_parallel(self, parking_ids: list) -> Dict[str, str]:
        """get parking space tonnage of specific parking garage"""
        with mp.Pool(processes=mp.cpu_count()) as pool:
            # add parrking_url_prefix to each parking_id
            parking_urls = [PARKING_URL_SPECIFIC_PREFIX + str(parking_id) for parking_id in parking_ids]
            results = pool.map(worker_scrape_for_parking_space_tonnage, parking_urls)
        return dict(zip(parking_ids, results))

    def get_parking_space_tonnage(self, parking_url_id) -> str:
        """get parking space tonnage of specific parking garage"""
        full_parking_url = PARKING_URL_SPECIFIC_PREFIX + parking_url_id
        parking_space_tonnage = self.ps.scrape_for_parking_space_tonnage(full_parking_url)
        # self.cls_logger.info(f"{parking_url_id} has {f}")
        return parking_space_tonnage

    def get_all_parking_garages_info(self) -> Optional[Dict[str, Dict[str, Any]]]:
        '''get all the parking garage names'''
        # self.cls_logger.info(f"find all parking garages in Ahuzot Hachof website")
        all_scrape_parking_matchs = self.ps.get_html_list_of_all_parking_garages(url=PARKING_URL_ALL)
        # self.cls_logger.info(f"{len(all_scrape_parking_matchs)} parking garages found")

        # self.cls_logger.info(f"scraping data from Ahuzot Hachof website")
        parking_names_and_locations = dict()
        db_headers = self.pu.get_parking_info_db_headers()
        for match in all_scrape_parking_matchs:
            url_id, name_hebrew, address_hebrew = self.ps.parking_info_scraping(match=match)
            if name_hebrew in (self.ignored_parking_names):
                self.cls_logger.error(f"could not find {name_hebrew} in google maps")
                continue
            # name_english, address_english, geo_lat, geo_lng = self.pw.get_parking_info(name_hebrew, address_hebrew)
            name_english, address_english, geo_lat, geo_lng = None, None, None, None

            parking_names_and_locations[url_id] = {
                db_headers[0]: url_id,
                db_headers[1]: name_hebrew,
                db_headers[2]: name_english,
                db_headers[3]: address_hebrew,
                db_headers[4]: address_english,
                db_headers[5]: geo_lat,
                db_headers[6]: geo_lng,
            }
        # self.cls_logger.info(f"{len(parking_names_and_locations)} parking garages scraped")
        return parking_names_and_locations


if __name__ == "__main__":
    pm = ParkingManager()
    # while(True):
    #     parking_garage = "Arlozorov"
    #     pst = p.get_parking_space_tonnage(str(Parking_Names_Tlv_Dict[parking_garage]))  # pst=parking_space_tonnage
    #     print(f"parking_garage => {parking_garage}, status => {pst}")
    #     sleep(10)

    result = pm.get_all_parking_garages_info()

    # result = pm.get_parking_space_tonnage_parallel()
    print(result)
