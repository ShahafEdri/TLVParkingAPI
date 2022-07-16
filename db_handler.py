from logging import Logger

import pandas as pd
from pandas.errors import EmptyDataError
from tabulate import tabulate

CLS_ROOT = 'parking_db/'


class DBHandler:
    def __init__(self):
        # set logger
        self.cls_logger = Logger(__name__)

        self.cldf = dict()
        '''cldf (aka class_garages_dataframes) is a dictionary of dataframes, key: parking space id, value: df, sorted by timestamp'''

        cls_file = 'parking.csv'
        self.cls_path = CLS_ROOT + cls_file
        try:
            temp_df = pd.read_csv(self.cls_path)
            temp_df.set_index('parking_space_id', inplace=True)
            # trasform index to int
            temp_df.index = temp_df.index.astype(int)
            # sort by address engilsh
            temp_df.sort_index(inplace=True)

        except:
            temp_df = pd.DataFrame(columns=['parking_space_id', 'name_hebrew', 'name_english',
                                   'address_hebrew', 'address_english', 'geo_lat', 'geo_lng'])
            temp_df.to_csv(self.cls_path, index=True)
        self.cls_df = temp_df

        # open dictionary to store db of each parking space by id
        self.tonnage_headers = ['timestamp', 'parking_tonnage']
        for id in self.cls_df.index:
            cls_garage_file = self.get_parking_csv_path(id)
            # try to read csv if not, create new one
            try:
                temp_df = pd.read_csv(cls_garage_file)
                temp_df.set_index('timestamp', inplace=True)
                # sort df by timestamp in ascending order (oldest first)
                temp_df.sort_index(inplace=True)
            except (FileNotFoundError, EmptyDataError):
                temp_df = pd.DataFrame(columns=tonnage_headers)
                temp_df.set_index('timestamp', inplace=True)
                temp_df.to_csv(cls_garage_file, index=True)
            self.cldf[id] = temp_df

    @staticmethod
    def get_parking_csv_path(id):
        name_prefix = 'parking_garage_'
        file_type = '.csv'
        cls_garage_file = CLS_ROOT + name_prefix + str(id) + file_type
        return cls_garage_file

    def update_parking_tonnage(self, parking_space_id: int, parking_tonnage: str, rewrite_db: bool = False):
        '''Add parking tonnage to db'''
        # get current timestamp
        timestamp = pd.Timestamp.now()
        # create new dataframe with timestamp and parking tonnage
        temp_df = pd.DataFrame(data=[[timestamp, parking_tonnage]], columns=self.tonnage_headers) 
        temp_df.set_index(self.tonnage_headers[0], inplace=True)
        # save to csv without header
        self.cldf[parking_space_id].to_csv(self.get_parking_csv_path(parking_space_id), mode='a', index=True, header=False)
        # add new row to df
        self.cldf[parking_space_id].loc[timestamp] = parking_tonnage
        # rewrite df to csv
        if rewrite_db:
            self.cldf[parking_space_id].to_csv(self.get_parking_csv_path(parking_space_id), index=True)

    def get_last_parking_tonnage(self, parking_space_id):
        '''Get latest parking tonnage from db'''
        return self.cldf[parking_space_id].iloc[-1]['parking_tonnage']

    def get_parking_tonnage_at_timestamp(self, parking_space_id, timestamp):
        '''Get parking tonnage for a specific timestamp'''
        return self.cldf[parking_space_id].loc[self.cldf[parking_space_id]['timestamp'] == timestamp]['parking_tonnage'].values[0]

    def get_parking_tonnage_between_timestamps(self, parking_space_id, timestamp_start, timestamp_end):
        '''Get parking tonnage for a specific timestamp'''
        return self.cldf[parking_space_id].loc[(self.cldf[parking_space_id]['timestamp'] >= timestamp_start) &
                                               (self.cldf[parking_space_id]['timestamp'] <= timestamp_end)]['parking_tonnage'].values

    def get_parking_tonnage_for_day(self, parking_space_id, day):
        '''Get parking tonnage for a specific day'''
        return self.cldf[parking_space_id].loc[self.cldf[parking_space_id]['timestamp'].dt.day == day]['parking_tonnage'].values

    def get_parking_tonnage_for_month(self, parking_space_id, month):
        '''Get parking tonnage for a specific month'''
        return self.cldf[parking_space_id].loc[self.cldf[parking_space_id]['timestamp'].dt.month == month]['parking_tonnage'].values

    def get_parking_tonnage_up_to_timestamp(self, parking_space_id, timestamp):
        '''Get parking tonnage for a specific timestamp'''
        return self.cldf[parking_space_id].loc[self.cldf[parking_space_id]['timestamp'] <= timestamp]['parking_tonnage'].values

    def get_parking_tonnage_by_count(self, parking_space_id, count):
        '''Get parking tonnage for a specific count'''
        return self.cldf[parking_space_id].iloc[-count:]['parking_tonnage'].values

    def delete_parking_tonnage_timestamp(self, parking_space_id, timestamp):
        '''Delete parking tonnage for a specific timestamp'''
        self.cldf[parking_space_id].drop(self.cldf[parking_space_id][self.cldf[parking_space_id]['timestamp'] == timestamp].index, inplace=True)
        self.cldf[parking_space_id].to_csv(self.get_parking_csv_path(parking_space_id), index=True)

    def get_parking_space_ids(self) -> list:
        '''Get all parking space ids'''
        return self.cls_df.index.values

    def update_all_parking_space_information(self, parking_space_by_id_dict: dict):
        '''Update all parking space information'''
        # transform dict to df
        # dict to dataframe with parking space id as index
        temp_df = pd.DataFrame.from_dict(parking_space_by_id_dict, orient='index')
        # set index to parking space id
        temp_df.set_index('parking_space_id', inplace=True)
        # trasform index to int
        temp_df.index = temp_df.index.astype(int)
        # sort index in ascending number order

        # check if there are new parking_space_id that are not in cls_df yet
        new_parking_space_id_df = temp_df[temp_df.index.isin(self.cls_df.index) == False]
        # new_parking_space_id_df = temp_df[temp_df["parking_space_id"].isin(self.cls_df["parking_space_id"]) == False]
        # print log of those new parking_space_id and there df values with tabulate
        if new_parking_space_id_df.empty == False:
            # self.cls_logger.info("New parking space found:")
            # self.cls_logger.info(tabulate(new_parking_space_id_df, headers='keys', tablefmt='psql'))
            # add new parking space to cls_df
            self.cls_df = self.cls_df.append(new_parking_space_id_df)

        self.cls_df.sort_index(inplace=True)
        # write df to csv
        self.cls_df.to_csv(self.cls_path, index=True)


if __name__ == '__main__':
    from parking_manager import ParkingManager

    # parking = Parking()
    pid = 1
    # response = parking.get_parking_space_tonnage(str(pid))
    db = DBHandler()
    for i in range(1, 10):
        db.update_parking_tonnage(pid, str(i))
    # db.update_parking_tonnage(pid, "check")
