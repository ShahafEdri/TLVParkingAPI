from logging import Logger

import pandas as pd
from pandas.errors import EmptyDataError
from tabulate import tabulate

CLS_ROOT = 'parking_db/'


class DBHandler:
    def __init__(self):
        # set logger
        self.cls_logger = Logger(__name__)
        # TODO move to utils
        _cls_file = 'parking_info.csv'
        self.prk_info_path = CLS_ROOT + _cls_file
        self.info_db_headers = ['parking_id', 'name_hebrew', 'name_english', 'address_hebrew', 'address_english', 'geo_lat', 'geo_lng']

        try:
            temp_df = pd.read_csv(self.prk_info_path)
            temp_df.set_index('parking_id', inplace=True)
            # trasform index to int
            temp_df.index = temp_df.index.astype(int)
            # sort by address engilsh
            temp_df.sort_index(inplace=True)

        except:
            temp_df = pd.DataFrame(columns=self.info_db_headers)
            temp_df.set_index('parking_id', inplace=True)
            temp_df.to_csv(self.prk_info_path, index=True)
        self.prk_info_df = temp_df

        # TODO move to utils
        _cls_file = 'parking_tonnage.csv'
        self.prk_tnng_path = CLS_ROOT + _cls_file
        self.tonnage_headers = ['timestamp', 'parking_id', 'tonnage']
        # try to read csv if not, create new one
        try:
            temp_df = pd.read_csv(self.prk_tnng_path)
            temp_df.set_index('timestamp', inplace=True)
            # sort df by timestamp in ascending order (oldest first)
            temp_df.sort_index(inplace=True)
        except (FileNotFoundError, EmptyDataError):
            temp_df = pd.DataFrame(columns=self.tonnage_headers)
            temp_df.set_index('timestamp', inplace=True)
            temp_df.to_csv(self.prk_tnng_path, index=True)
        self.prk_tnng_db = temp_df
        # add group by parking space id
        self.prk_tnng_db_by_id = self.prk_tnng_db.groupby(self.tonnage_headers[1])

    def add_new_parking_tonnage(self, parking_id: int, tonnage: str):
        '''Add new parking tonnage to db'''
        # get current timestamp with format '%Y-%m-%d %H:%M:%S'
        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        # create new dataframe with parking space id, parking tonnage and timestamp
        temp_df = pd.DataFrame([[timestamp, parking_id, tonnage]], columns=self.tonnage_headers)
        # set index to timestamp
        temp_df.set_index(self.tonnage_headers[0], inplace=True)
        # concatenate with current db and sort by timestamp
        self.prk_tnng_db = pd.concat([self.prk_tnng_db, temp_df])
        # sort by timestamp
        self.prk_tnng_db.sort_index(inplace=True)
        # rewrite df to csv
        self.prk_tnng_db.to_csv(self.prk_tnng_path, index=True)

    def update_parking_tonnage_by_dict(self, parking_tonnage_dict, rewrite_db: bool = True):
        '''Add parking tonnage to db'''
        pass

    def get_last_parking_tonnage(self, parking_id):
        '''Get latest parking tonnage from db'''
        # get last tonnage in db for parking space id
        return self.prk_tnng_db_by_id.get_group(parking_id).iloc[-1]['tonnage']

    def get_parking_tonnage_at_timestamp(self, parking_id, timestamp):
        '''Get parking tonnage for a specific timestamp'''
        # get tonnage for parking space id and timestamp
        return self.prk_tnng_db_by_id.get_group(parking_id).loc[timestamp]['tonnage']

    def get_parking_tonnage_between_timestamps(self, parking_id, timestamp_start, timestamp_end):
        '''Get parking tonnage for a specific timestamp'''
        # get tonnage for parking space id between timestamp start and timestamp end
        return self.prk_tnng_db_by_id.get_group(parking_id).loc[timestamp_start:timestamp_end]['tonnage']

    def get_parking_tonnage_for_day(self, parking_id, day):
        '''Get parking tonnage for a specific day'''
        # get tonnage for parking space id and day
        return self.prk_tnng_db_by_id.get_group(parking_id).loc[day]['tonnage']

    def get_parking_tonnage_for_month(self, parking_id, month):
        '''Get parking tonnage for a specific month'''
        # get tonnage for parking space id and month
        return self.prk_tnng_db_by_id.get_group(parking_id).loc[month]['tonnage']

    def get_parking_tonnage_from_timestamp_to_now(self, parking_id, timestamp):
        '''Get parking tonnage for a specific timestamp'''
        # get tonnage for parking space id up to timestamp
        return self.prk_tnng_db_by_id.get_group(parking_id).loc[timestamp:]['tonnage']

    def get_parking_tonnage_up_to_count(self, parking_id, count):
        '''Get parking tonnage up to specific count'''
        # get tonnage for parking space id up to count
        return self.prk_tnng_db_by_id.get_group(parking_id).iloc[-count:]['tonnage']

    def delete_parking_tonnage_timestamp(self, parking_id, timestamp):
        '''Delete parking tonnage for a specific timestamp'''
        # delete parking tonnage for parking space id and timestamp
        self.prk_tnng_db_by_id.get_group(parking_id).drop(timestamp, inplace=True)
        # rewrite df to csv
        self.prk_tnng_db.to_csv(self.prk_tnng_path, index=True)
        

    def get_parking_ids(self) -> list:
        '''Get all parking space ids'''
        # get all parking space ids
        return self.prk_info_df.index.tolist()

    def update_all_parking_space_information(self, parking_space_by_id_dict: dict):
        '''Update all parking space information'''
        # transform dict to df
        # dict to dataframe with parking space id as index
        temp_df = pd.DataFrame.from_dict(parking_space_by_id_dict, orient='index')
        # set index to parking space id
        temp_df.set_index('parking_id', inplace=True)
        # trasform index to int
        temp_df.index = temp_df.index.astype(int)
        # sort index in ascending number order

        # check if there are new parking_id that are not in cls_df yet
        new_parking_id_df = temp_df[temp_df.index.isin(self.prk_info_df.index) == False]
        # print log of those new parking_id and there df values with tabulate
        if new_parking_id_df.empty == False:
            pass
            # self.cls_logger.info("New parking space found:")
            # self.cls_logger.info(tabulate(new_parking_id_df, headers='keys', tablefmt='psql'))
            # add new parking space to cls_df


if __name__ == '__main__':
    from parking_manager import ParkingManager

    # parking = Parking()
    pid = 1
    tonnage = "free"
    # response = parking.get_parking_space_tonnage(str(pid))
    dbh = DBHandler()
    t1 = "2022-07-16 15:38:10"
    t2 = "2022-07-16 15:40:15"
    result = dbh.get_parking_tonnage_up_to_count(pid, 3)
    print(result)
