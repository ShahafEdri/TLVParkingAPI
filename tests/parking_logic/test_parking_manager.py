from logic.parking import parking_manager_obj


def test_get_all_parking_garages_info(parking_lots: dict):
    res = parking_manager_obj.get_all_parking_garages_info()
    # check that values are in dict
    list_of_keys_to_be_found_in_res = list(list(parking_lots.values())[0].keys())
    parking_lot_for_validation = list(parking_lots.keys())[0]
    assert all(x in res[parking_lot_for_validation] for x in list_of_keys_to_be_found_in_res)
    # check that vlaues 123 3 and 45 are in dict in one line
    parking_ids = list(parking_lots.keys())
    assert all(x in res for x in parking_ids)


def test_get_parking_space_tonnage_parallel(parking_lots, tonnage_legitimate_values):
    parking_ids = list(parking_lots.keys())
    res = parking_manager_obj.get_parking_space_tonnage_parallel(parking_ids)
    # check that values in dict or only on of lagitimate values
    assert all(x in tonnage_legitimate_values for x in res.values())
