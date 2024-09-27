import pandas as pd
from datetime import datetime, timedelta

class TreatData():

    def __init__(self) -> None:
        pass


    def create_features(self, dataframe):
        
        dataframe['part_time_h'] = dataframe['time'].apply(lambda t: int(t.split(':')[0]))
        dataframe['part_time_m'] = dataframe['time'].apply(lambda t: int(t.split(':')[1]))
        dataframe['part_time_s'] = dataframe['time'].apply(lambda t: int(t.split(':')[2]))

        dataframe['total_time_s'] = dataframe['time'].apply(lambda t: int(t.split(':')[0])*3600 + int(t.split(':')[1])*60 + int(t.split(':')[2]))
        dataframe['total_time_m'] = dataframe['total_time_s'] / 60
        dataframe['total_time_h'] = dataframe['total_time_m'] / 60
        
        dataframe['dist_num'] = dataframe['distance'].str.replace('KM', '')
        dataframe['dist_num'] = pd.to_numeric(dataframe['dist_num'])
        
        start_datetime = datetime(1900, 1, 1)
        def from_ordinal(ordinal, start_datetime=start_datetime):
            return start_datetime + timedelta(hours=ordinal)

        dataframe['pace'] = dataframe['total_time_h'] / dataframe['dist_num']
        dataframe['pace'] = dataframe['pace'].apply(lambda x: from_ordinal(x)).dt.time

        return dataframe
    

    def define_types(self, dataframe):

        numeric_columns = ['pos', 'num', 'age', 'ag', 'part_time_h', 'part_time_m', 'part_time_s', 'total_time_s', 'total_time_m', 'total_time_h']
        for column in numeric_columns:
            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')

        string_columns = ['athlete', 'group', 'team']
        for column in string_columns:
            dataframe[column] = dataframe[column].str.replace(r'\n', ' ')

        return dataframe