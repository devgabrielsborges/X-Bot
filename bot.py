import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class XBot:
    pass
    
    
class Message:
    
    @staticmethod
    def _sheets(method):
        def wrapper(self):
            
            # If modifying these scopes, delete the file token.json.
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

            # The ID and range of a sample spreadsheet.
            SAMPLE_SPREADSHEET_ID = "1Fam3Tf54V0E_IzmEg_OsT9wnqqUlpz-cHl-ShPds2JE"   # ID da planilha
            SAMPLE_RANGE_NAME = "Produtos!A1:D1"

            """Shows basic usage of the Sheets API.
            Prints values from a sample spreadsheet.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                    )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            method(self)

    @_sheets        
    def _getMsgInfo():

        try:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
                .execute()
            )
            valores = result['values']
            print(valores)
            return valores.json()
            
        except HttpError as err:
            print(err)

    @_sheets
    def _postMsg():
        pass
                

    def __init__(self):

        self.produto = self._getMsgInfo()[0]
        self.valor = self._getMsgInfo()[1]
        self.link = self._getMsgInfo()[2]
        self.body = self._getMsgInfo()[3]

if __name__ == '__main__':
    msg = Message()
    
