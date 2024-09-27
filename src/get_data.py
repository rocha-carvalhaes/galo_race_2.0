import os
import pandas as pd
import re
import pdfplumber
import fitz # type: ignore

class GetData:
    
    def __init__(self) -> None:
        self.columns = ['pos','num','athlete','gender','age','group','ag','c','team','time']
    
    def parse_text_to_table(self, text):
        # Implement parsing logic to convert text into a structured table
        # This could involve splitting lines, using regex to find patterns, etc.
        parsed_data = []

        # Example (placeholder) parsing logic:
        lines = text.split('\n')
        for line in lines:
            # Split line into data fields, assuming space-separated values
            fields = line.split()
            if len(fields) == 10:  # assuming there are 10 columns
                parsed_data.append(fields)

        return parsed_data

    def extract_page_from_pdf(self, file_path: str, page_num: int):

        # Open the PDF file with fitz
        document = fitz.open(file_path)

        # Gettin text from page 'p'
        page = document.load_page(page_num)
        text = page.get_text("text")
        text = text.replace('\n', ' ')

        # String to identify splitting position
        character_to_insert = "##"

        # Splitting rows properly
        pattern = r'(\d{2}:\d{2}:\d{2})'
        text_to_split = re.sub(pattern, r'\1' + character_to_insert, text)
        splitted_text = text_to_split.split(character_to_insert)
        splitted_lists = [splitted_text[i:i + 1] for i in range(0, len(splitted_text), 1)]

        # Method to split each row into columns
        def split_rows(row_text):

            # pattern 0: headers
            pattern = r"\bTempo\b"
            row_text_0 = re.sub(pattern, lambda match: match.group(0) + character_to_insert, row_text)
            row_texts = row_text_0.split(character_to_insert)
            row_text_0 = [text.strip() for text in row_texts]
        
            # pattern 1: time
            pattern = r"\b\d{2}:\d{2}:\d{2}\b"
            row_text_1 = re.sub(pattern, lambda match: character_to_insert + match.group(0), row_text_0[-1])
            row_texts = row_text_1.split(character_to_insert)
            row_text_1 = [text.strip() for text in row_texts]

            # pattern 2: faixa
            pattern = r'(F\d{1,4}|M\d{1,4})\b'
            row_text_2 = re.sub(pattern, character_to_insert+r'\1'+character_to_insert, row_text_1[0])
            row_text_2 = row_text_2.split(character_to_insert)
            row_text_2 = [text.strip() for text in row_text_2]

            # pattern 3: f.e.
            pattern = r'(\b\d{1,4}\b|-)'
            row_text_3 = re.sub(pattern, r'\1'+character_to_insert, row_text_2[2])
            row_text_3 = row_text_3.split(character_to_insert)
            row_text_3 = [text.strip() for text in row_text_3]

            # pattern 4: age
            pattern = r'(?<=\s)(\d{1,2})\b(?!.*\d)'
            row_text_4 = re.sub(pattern, character_to_insert+r'\1', row_text_2[0])
            row_text_4 = row_text_4.split(character_to_insert)
            row_text_4 = [text.strip() for text in row_text_4]

            # pattern 5: sexo
            pattern = r'(?<=\b)(F|M)(?=\s*$)'
            row_text_5 = re.sub(pattern, fr'{character_to_insert}\1',  row_text_4[0])
            row_text_5 = row_text_5.split(character_to_insert)
            row_text_5 = [text.strip() for text in row_text_5]

            # pattern 6: athlete num
            pattern = r'(\b\d{1,5}\b)'
            row_text_6 = re.sub(pattern, lambda match: character_to_insert + match.group(0) + character_to_insert, row_text_5[0])
            row_text_6 = row_text_6.split(character_to_insert)
            row_text_6 = [text.strip() for text in row_text_6]

            # Aranging columns and returning row data
            row_texts = [row_text_6[1], row_text_6[3], row_text_6[4], row_text_5[1], row_text_4[1], row_text_2[1], row_text_3[0], '', row_text_3[1], row_text_1[1]]
            return row_texts

        page_data = []
        for sublist in splitted_lists:

            # Removing page headers and footers from dataset
            mask = (
                ('CORRIDA DO GALO 2024' not in sublist[0]) &
                ('25/08/2024' not in sublist[0]) &
                ('CORRIDA DO GALO 2023' not in sublist[0]) &
                ('27/08/2023' not in sublist[0])
            )

            if mask:
                row = split_rows(sublist[0])
                page_data.append(row)

        return page_data


    def extract_table_from_pdf(self, file_path, extract_via: str):
        
        if extract_via == 'pdfplumber':
            # Using pdfplumber to read pdf content
            with pdfplumber.open(file_path) as pdf:

                data = []

                # Iterate through the pages
                for i, page in enumerate(pdf.pages):

                    # Try to xtract table
                    try:
                        if page.find_table():
                            page_data = page.extract_tables()
                            data.extend(page_data[0])

                    # Use custom fitz for exceptions
                    except:
                        page_data = self.extract_page_from_pdf(file_path=file_path, page_num=i)
                        data.extend(page_data)

                dataframe = pd.DataFrame(data, columns=self.columns)

        elif extract_via == 'custom_fitz':
            # Using custom fitz method to read pdf content
            document = fitz.open(file_path)
            # Get the number of pages
            n_pages = document.page_count

            data = []

            # Iterate through the pages and extract data
            for i in range(0, n_pages):
                page_data = self.extract_page_from_pdf(file_path=file_path, page_num=i)
                if len(page_data) > 0:
                    data.extend(page_data)

            dataframe = pd.DataFrame(data, columns=self.columns)

        """
        # Needs java jdk as depedency. This block will be commentted until jdk becomes available
        elif extract_via == 'tabula':
            # Using tabula module to read pdf content
            data = tabula.read_pdf(
                file_path, 
                pages='all', # read all pages at once
                encoding='latin-1', 
                multiple_tables=False,
                lattice=True # informing tables are separeted by lines
            )
        """

        return dataframe

    def get_data(self, pdf_path, extract_via):
        
        # List files in the data folder
        list_files = os.listdir(pdf_path)
        
        # Aranging files to display important info
        df_files = pd.DataFrame(list_files)
        df_files = df_files[0].str.split('.', expand=True)
        df_files = df_files.loc[df_files[1] == 'pdf']
        df_files = df_files[0].str.split('-', expand=True, n=2)
        df_files.columns = ['distance', 'gender', 'n']
        
        # Creating DataFrame to store extracted data
        data = pd.DataFrame()
        
        # Extracting data
        for file_num in df_files.index:
            print(df_files['distance'][file_num], df_files['gender'][file_num])
            
            file_path = os.path.join(pdf_path, list_files[file_num])
            
            table = self.extract_table_from_pdf(file_path=file_path, extract_via=extract_via)
            
            # Adding a column with the race distance        
            table['distance'] = df_files['distance'][file_num]
            
            # Minimum treatments to store structured data
            df = table # temporary dataframe
            # first_line = pd.DataFrame(table.columns).T # missandertood value placed in headers
            # df.columns = columns # renaming columns to standarize concatenation
            # first_line.columns = columns
            data = pd.concat([data, table], ignore_index=True)
            
            # Replacing line breakers so csv does not get messed up
            data.team = data.team.str.replace('\r', ' ')
            data.athlete = data.athlete.str.replace('\r', ' ')   
        
        data = data.loc[data.pos != 'Pos']
        
        return data
