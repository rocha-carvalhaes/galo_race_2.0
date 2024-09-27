import os

class GetPath:
    
    def __init__(self) -> None:
        pass
    
    def get_pdf_path(self, year):
        
        # Obtaining script path
        abs_path = os.path.dirname(os.path.abspath(__file__))

        # Getting to the root path of the project
        root_path = abs_path.rsplit('\\', 1)[0]

        # Getting to the "01_data\\01_raw" folder, where pdf's are stored
        year = str(year)
        pdf_path = os.path.join(root_path, 'data', 'raw', year)
        
        return pdf_path
