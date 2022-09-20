import os
import sys

# wd = 'C:/Users/shahafe/Documents/vscode_projects/python_http_request'
# sys.path.append(wd)
# os.chdir(wd)
# print(os.getcwd())
# print(sys.path)
from parking.parking_manager import ParkingManager
from utils.general_utils import singleton
from utils.logging_utils import logger

from db.db_handler import DBHandler


@singleton
class DBManager:
    def __init__(self):
        self.dbh = DBHandler()
        self.pm = ParkingManager()
        self.logger = logger

    # def add_parking_tonnage(self, parking_space_id: int):
    #     '''Add parking tonnage to db'''
    #     parking_tonnage = self.pm.get_parking_space_tonnage(parking_space_id)
    #     self.dbh.update_parking_tonnage(parking_space_id, parking_tonnage)

    def update_all_parking_space_info(self):
        '''Update parking space info'''
        parking_info_dict = self.pm.get_all_parking_garages_info()
        self.dbh.update_all_parking_space_information(parking_info_dict)

    def update_all_parking_spaces_info(self):
        '''Update all parking spaces info'''
        for parking_space_id in self.dbh.get_parking_space_ids():
            self.add_parking_info(parking_space_id)

    def get_last_parking_tonnage(self, parking_space_id):
        '''Get latest parking tonnage from db'''
        return self.dbh.get_last_parking_tonnage(parking_space_id)

    def update_all_parking_spaces_tonnages_seqential(self):
        '''Update all parking spaces tonnages'''
        for parking_space_id in self.dbh.get_parking_space_ids():
            self.add_parking_tonnage(parking_space_id)

    def update_all_parking_spaces_tonnages_parallel(self):
        '''Update all parking spaces tonnages'''
        parking_space_ids = self.dbh.get_parking_ids()
        parking_tonnage_dict = self.pm.get_parking_space_tonnage_parallel(parking_space_ids)
        self.dbh.update_all_parking_tonnages_by_dict(parking_tonnage_dict)


if __name__ == '__main__':
    # dbm = DBManager()
    # dbm.update_all_parking_space_info()
    # get logger
    # dbm.update_all_parking_spaces_tonnages_parallel()
    pass
