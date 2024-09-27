import os
import pandas as pd

class SaveParquet:
    
    def __init__(self) -> None:
        pass
    
    def save_parquet(self, dataframe, parquets_name, year):

        # Getting path of current execution
        abs_path = os.path.dirname(os.path.abspath(__file__))
        root_path = abs_path.rsplit('\\', 1)[0]
        
        # Getting target path
        year =  str(year)
        folder_path = os.path.join(root_path, rf'data\treated')
        filename = f'{parquets_name}.parquet'
        saving_path = os.path.join(folder_path, filename)

        # Saving file
        dataframe.to_parquet(saving_path)

        # Returning status
        return folder_path
    




