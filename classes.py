import pytz
import requests
import json

from datetime import datetime
from openpyxl import load_workbook
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twilio.rest import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

class SheetXlsx:

    @staticmethod   # função para obter horário
    def _data_hora():
        fuso_BR = pytz.timezone("Brazil/East")
        horario_BR = datetime.now(fuso_BR)
        return horario_BR

    def __init__(self, sheetname : str, sheetpath : str, actual_place : int):
        self.sheetname = sheetname
        self.sheet = load_workbook(sheetpath)
        self.worksheet = self.sheet.active
        self.actual_place = actual_place
        self.date = self._data_hora()
        self.values_add = None

    def get_info(self):
        self.produto = self.worksheet[f"A{self.actual_place}"].value
        self.valor = self.worksheet[f"B{self.actual_place}"].value
        self.link = self.worksheet[f"C{self.actual_place}"].value
        self.info = [self.produto, self.valor, self.link]
        print(self.info)
        
        return self.info
        
    def post_info(self, value_add : list) -> list:

        '''   
        values_add = [status_message, product_message]
        '''

        if len(value_add) == 2:
            self.worksheet[f"D{self.actual_place}"] = value_add[0]
            self.worksheet[f"E{self.actual_place}"] = value_add[1]
            self.worksheet[f"F{self.actual_place}"] = str(self._data_hora())

            self.sheet.save(f"{self.sheetname}.xlsx")
            print("Worksheet has been saved")


        
    def info(self) -> list:
        if None not in [self.produto, self.valor, self.link]:
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
