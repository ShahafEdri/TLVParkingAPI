from logic.parking import parking_scraper_obj
from logic.parking.parking_scraper import worker_scrape_for_parking_space_tonnage


def test_worker_scrape_for_parking_space_tonnage(parking_lots: dict, tonnage_legitimate_values: list):
    parking_url_id = f"https://www.parking.gov.il/He/Pages/ParkingLot.aspx?ID={parking_lots.keys()[0]}"
    res = worker_scrape_for_parking_space_tonnage(parking_url_id)
    assert res in tonnage_legitimate_values, f"res: {res} is not in {tonnage_legitimate_values}"
