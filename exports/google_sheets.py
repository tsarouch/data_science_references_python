
import pandas as pd
import numpy as np
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

class GoogleSheetExporter(object):

    def __init__(self):
        pass

    def get_credentials(self, credentials_json):
        json_key = json.load(open(credentials_json))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(
            json_key['client_email'],
            json_key['private_key'].encode(),
            scope)
        return gspread.authorize(credentials)

    def get_worksheet_by_url(self, gc, url, sheet_idx):
        sh = gc.open_by_url(url)
        return sh.get_worksheet(sheet_idx)

    def export_dataframe(self, worksheet, df):
        self._create_columns(worksheet, df)
        self._create_rows(worksheet, df)


    def _numberToLetters(self, q):
        q = q - 1
        result = ''
        while q >= 0:
            remain = q % 26
            result = chr(remain+65) + result;
            q = q//26 - 1
        return result

    def _create_columns(self, worksheet, df):
        # columns names
        columns = df.columns.values.tolist()
        # selection of the range that will be updated
        cell_list = worksheet.range('A1:' + self._numberToLetters(len(columns))+'1')
        # modifying the values in the range
        for cell in cell_list:
            val = columns[cell.col-1]
            if type(val) is str:
                val = val.decode('utf-8')
            cell.value = val
        # update in batch
        worksheet.update_cells(cell_list)


    def _create_rows(self, worksheet, df):
        # number of lines and columns
        num_lines, num_columns = df.shape
        worksheet.resize(num_lines + 1, num_columns)

        # selection of the range that will be updated
        cell_list = worksheet.range('A2:' + self._numberToLetters(num_columns)+str(num_lines+1))
        # modifying the values in the range
        for cell in cell_list:
            val = df.iloc[cell.row-2,cell.col-1]
            if type(val) is str:
                val = val.decode('utf-8')
            elif isinstance(val, (int, long, float, complex)):
                # note that we round all numbers
                val = int(round(val))
            cell.value = val
        # update in batch
        worksheet.update_cells(cell_list)
