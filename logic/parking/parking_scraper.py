import re
from typing import Any

import requests
from bs4 import BeautifulSoup
from utils.logging_utils import logger

from logic.parking.parking_utils import heb2eng_dict


class ParkingScraper():
    def __init__(self) -> None:
        self.cls_logger = logger

    def get_html_list_of_all_parking_garages(self, url) -> Any:
        """get all the parking garage names"""
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        matchdiv = soup.find('table', id='ctl10_data1')
        matchs = matchdiv.select(".ParkingLinkX")
        return matchs

    def parking_info_scraping(self, match):
        match_parent = match.parent
        parking_url = match_parent.contents[0].attrs['href'].strip()
        url_id = re.match(pattern=r"\S+ID=(\d+)", string=parking_url).group(1)
        name_hebrew = match_parent.contents[0].contents[0].text.strip()
        address_hebrew = match_parent.contents[2].text.strip()
        return url_id, name_hebrew, address_hebrew

    def scrape_for_parking_space_tonnage(self, parking_url_id) -> str:
        """get parking space tonnage of specific parking garage"""

        r = requests.get(parking_url_id)
        soup = BeautifulSoup(r.text, 'lxml')

        self.cls_logger.info(f"scraping parking space tonnage of {parking_url_id}")
        # match = soup.div
        matchdiv = soup.find('div', id="ctl06_data1_UpdatePanel1_0")
        try:
            match = matchdiv.find_all("img")[1]
        except IndexError:
            self.cls_logger.error(f"could not find parking space tonnage of {parking_url_id}")
            return "not_valid"
        rematch = re.match(pattern=r"\S+ParkingIcons/(\w*).png", string=match["src"])
        parking_space_tonnage = rematch.group(1)
        result = heb2eng_dict[parking_space_tonnage]
        self.cls_logger.info(f"{parking_url_id} has {result}")
        return result


def worker_scrape_for_parking_space_tonnage(parking_url_id: str) -> str:
    """get parking space tonnage of specific parking garage"""

    r = requests.get(parking_url_id,timeout=500)
    soup = BeautifulSoup(r.text, 'lxml')

    matchdiv = soup.find('div', id="ctl06_data1_UpdatePanel1_0")
    try:
        match = matchdiv.find_all("img")[1]
    except IndexError:
        return "not_valid"
    rematch = re.match(pattern=r"\S+ParkingIcons/(\w*).png", string=match["src"])
    parking_space_tonnage = rematch.group(1)
    result = heb2eng_dict[parking_space_tonnage]
    return result


if __name__ == "__main__":
    res = worker_scrape_for_parking_space_tonnage("https://www.ahuzot.co.il/Parking/ParkingDetails/?ID=3")
    print(res)
    pass
