from enum import Enum


Parking_Names_Tlv_Dict = {  # TODO scrape automatically
    "Arlozorov": 123,
    "Assuta": 122,
    "Telnordo": 45,
    "Rebnitzki": 40
}

heb2eng_dict = {
    "panui": "available",
    "meat": "almost full",
    "male": "full",
    "sagur": "closed",
    "pail": "active",
}

PARKING_URL_ALL = "https://www.ahuzot.co.il/Parking/All/"
PARKING_URL_SPECIFIC_PREFIX = "https://www.ahuzot.co.il/Parking/ParkingDetails/?ID="


ignored_parking_names = [
    'חניון הבעש"ט',  # google maps can't find it
    'חניון הבעש"ט',  # google maps can't find it
]
