import os
from save_parquet import SaveParquet
from get_data import GetData
from get_path import GetPath
from treat_data import TreatData

class Run:
    
    def __init__(self) -> None:
        pass
    
    def check_run(self, saving_path) -> bool:
        list_files = os.listdir(saving_path)
        if self.parquets_name +'.parquet' in list_files:
            return True
        
    
    def run(self, year):
        pdf_path = GetPath().get_pdf_path(year)
        data = GetData().get_data(pdf_path=pdf_path, extract_via='pdfplumber')
        data = TreatData().create_features(dataframe=data)
        data = TreatData().define_types(dataframe=data)
        self.parquets_name = f'results_{year}'
        saving_folder = SaveParquet().save_parquet(dataframe=data, parquets_name=self.parquets_name, year=year)
        if self.check_run(saving_folder) == True:
            print('Sucesso!\nArquivo salvo no repositório')
        else:
            print('Ops!\nArquivo não foi salvo no repositório')

Run().run(year=2023)    
Run().run(year=2024)