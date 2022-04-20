import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('Client_Secret.json', scope)
client = gspread.authorize(credentials)

def addToSheet(csv_path):
  spreadsheet = client.open('JPNS_CSV_to_Sheets')
  with open(csv_path, encoding='latin-1', mode='r') as file_obj:
      content = file_obj.read()
      client.import_csv(spreadsheet.id, data=content)