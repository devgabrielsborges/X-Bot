import pytz
import os.path
import requests
import json
import tweepy

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twilio.rest import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from dotenv import load_dotenv
class Message:

    @staticmethod   # função para obter horário
    def _data_hora():
        fuso_BR = pytz.timezone("Brazil/East")
        horario_BR = datetime.now(fuso_BR)
        return horario_BR
    

    def __init__(self, actual_place):
        self.actual_place = actual_place
        self.date = self._data_hora()
        self.values_add = None
    
    def base_struct(method):
        def wrapper(self, *args, **kwargs):
            # If modifying these scopes, delete the file token.json.
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

            # The ID and range of a sample spreadsheet.
            SAMPLE_SPREADSHEET_ID = "1Fam3Tf54V0E_IzmEg_OsT9wnqqUlpz-cHl-ShPds2JE"   # ID da planilha
            SAMPLE_RANGE_NAME = f"Produtos!A{self.actual_place}:D{self.actual_place}"

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
            self.creds = creds
            self.SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_ID
            self.SAMPLE_RANGE_NAME = SAMPLE_RANGE_NAME

            method(self, *args, **kwargs)
        return wrapper

    @base_struct
    def get_info(self):
        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=self.SAMPLE_RANGE_NAME)
                .execute()
            )
            print(result)
            valores = result['values'][0]
            print(valores)
            self.produto = valores[0]
            self.valor = valores[1]
            self.link = valores[2]
            
        except HttpError as err:
            print(err)
    
    @base_struct
    def post_info(self, values_add : list, column='E'):
        try:
            service = build("sheets", "v4", credentials=self.creds)
            # Call the Sheets API
            sheet = service.spreadsheets()
            # Add or edit some info

            values_add = [values_add]
            result = (
                sheet.values()
                .update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=f'{column}{self.actual_place}', valueInputOption="USER_ENTERED", body={'values': values_add})
                .execute()
            )
            print(result)
                
            # Método update + valueInputOption
        except HttpError as err:
            print(err)
    
    @property
    def info(self):
        return [self.produto, self.valor, self.link]


class FirebaseAPI:
    
    def __init__(self, endpoint : str):
        self.endpoint = endpoint
    
    def get_data(self, page=''):
        if page != '':
            request = requests.get(f'{self.endpoint}/{page}/.json')
        
        else:
            request = requests.get(f'{self.endpoint}/.json')
        
        return request.json()

    def post_data(self, page='', info=''):
        if page != '' and info != '':
            request = requests.post(f'{self.endpoint}/{page}/.json', data=json.dumps(info))
        elif info != '':
            request = requests.post(f'{self.endpoint}/.json', data=json.dumps(info))

    def patch_data(self, page='', info=''):
        if page != '' and info != '':
            request = requests.patch(f'{self.endpoint}/{page}/.json', data=json.dumps(info))
        elif info != '':
            request = requests.patch(f'{self.endpoint}/.json', data=json.dumps(info))


class TwilioAPI:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
    
    def send_sms(self, from_number : str, to_number : str, msg : str):
        self.client = Client(self.account_sid, self.auth_token)
        message = self.client.messages.create(
            to=to_number,
            from_=from_number,
            body=msg
        )
        self.sid = message.sid
        print(message.sid)

class GroqCloud:
    def __init__(self, job, criativity=0, model="llama3-8b-8192"):
        self.job = job    # informações prévias para o modelo
        self.criativity = criativity   # temperature
        self.model = model   # tipo de modelo
        self.prompt = ChatPromptTemplate.from_messages(
            [("system", f"{self.job}"), ("human", "{text}")]
        )
        self.chat = ChatGroq(temperature=self.criativity, model_name=f"{self.model}")
    
    def request(self, msg):
        self.chain = self.prompt | self.chat   # conexão
        self.response = self.chain.invoke({"text": f"{msg}"})   # enviando requisicao
        
        return self.response.content
