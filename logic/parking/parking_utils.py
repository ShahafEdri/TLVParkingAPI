CLS_ROOT = 'parking_db/'
PARKING_URL_ALL = "https://www.ahuzot.co.il/Parking/All/"
PARKING_URL_SPECIFIC_PREFIX = "https://www.ahuzot.co.il/Parking/ParkingDetails/?ID="

# XXX: remove
Parking_Names_Tlv_Dict = {  # TODO scrape automatically
    "Arlozorov": 123,
    "Assuta": 122,
    "Telnordo": 45,
    "Rebnitzki": 40
}

# TODO: get from config file
heb2eng_dict = {
    "panui": "available",
    "meat": "almost full",
    "male": "full",
    "sagur": "closed",
    "pail": "active",
}

# TODO: get from config file

ignored_parking_names = [
    'חניון הבעש"ט',  # google maps can't find it
    'חניון הבעש"ט',  # google maps can't find it
]


class ParkingUtils():
    def __init__(self):
        self._parking_info_file = 'parking_info.csv'
        self._parking_info_path = CLS_ROOT + self._parking_info_file
        self._info_db_headers = ['parking_id', 'name_hebrew', 'name_english', 'address_hebrew', 'address_english', 'geo_lat', 'geo_lng']

        self._parking_tonnage_file = 'parking_tonnage.csv'
        self._parking_tonnage_path = CLS_ROOT + self._parking_tonnage_file
        self._tonnage_db_headers = ['timestamp', 'parking_id', 'tonnage']

    def get_parking_info_path(self):
        return self._parking_info_path

    def get_parking_tonnage_path(self):
        return self._parking_tonnage_path

    def get_parking_info_db_headers(self):
        return self._info_db_headers

    def get_parking_tonnage_db_headers(self):
        return self._tonnage_db_headers
