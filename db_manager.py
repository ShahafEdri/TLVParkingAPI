from db_handler import DBHandler
from parking_manager import ParkingManager
from logging import getLogger


class DBManager:
    def __init__(self):
        self.dbh = DBHandler()
        self.pm = ParkingManager()
        self.logger = getLogger()

    def add_parking_tonnage(self, parking_space_id: int):
        '''Add parking tonnage to db'''
        parking_tonnage = self.pm.get_parking_space_tonnage(parking_space_id)
        self.dbh.update_parking_tonnage(parking_space_id, parking_tonnage)

    def get_last_parking_tonnage(self, parking_space_id):
        '''Get latest parking tonnage from db'''
        return self.dbh.get_last_parking_tonnage(parking_space_id)

    def update_all_parking_spaces_tonnages_seqential(self):
        '''Update all parking spaces tonnages'''
        for parking_space_id in self.dbh.get_parking_space_ids():
            self.add_parking_tonnage(parking_space_id)


if __name__ == '__main__':
    dbm = DBManager()
    dbm.update_all_parking_spaces_tonnages_seqential()
