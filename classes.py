"""Classes & methods for main script"""

import json
from datetime import datetime
import pytz
import requests

from openpyxl import load_workbook
from twilio.rest import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class SheetXlsx:
    """ Class for operation with Excel xlsx worksheets
    """

    @staticmethod   # função para obter horário
    def _data_hora() -> str:
        return str(datetime.now(pytz.timezone("Brazil/East")))

    def __init__(self, sheetname: str, sheetpath: str, actual_place: int):
        """__init__ _summary_

        Args:
            sheetname (str): Name of sheet for future operations and saving
            sheetpath (str): Path of the archive
            actual_place (int): Index for operations with the cells
        """
        self.sheetname = sheetname
        self.sheet = load_workbook(sheetpath)
        self.worksheet = self.sheet.active
        self.actual_place = actual_place
        self.date = self._data_hora()
        self.values_add = None
        self.produto = None
        self.valor = None
        self.link = None
        self.info = None

    def get_info(self) -> list:
        """get_info -> Get information from cells

        Returns:
            list: List with information about the product
        """
        self.produto = self.worksheet[f"A{self.actual_place}"].value
        self.valor = self.worksheet[f"B{self.actual_place}"].value
        self.link = self.worksheet[f"C{self.actual_place}"].value
        self.info = [self.produto, self.valor, self.link]
        return self.info

    def post_info(self, value_add: list):
        """post_info -> Add informations to the cells

        Args:
            value_add (list): [status_message, product_message]
        """
        if len(value_add) == 2:
            self.worksheet[f"D{self.actual_place}"] = value_add[0]
            self.worksheet[f"E{self.actual_place}"] = value_add[1]
            self.worksheet[f"F{self.actual_place}"] = self._data_hora()

            self.sheet.save(f"{self.sheetname}.xlsx")
            print("Worksheet has been saved")


class FirebaseAPI:
    """ Class for operations with Firebase
    """

    def __init__(self, endpoint: str):
        """__init__ Set up the URL of Firebase Realtime Database

        Args:
            endpoint (str): URL of Realtime Database
        """
        self.endpoint = endpoint

    def get_data(self, *page: str) -> dict:
        """get_data getter method for data in Realtime Database

        Args:
            page (str, optional): URL of an especific page to get the data.
            Defaults to '' if you want get data from the main page

        Returns:
            _type_: dict
        """
        if page != '':
            request = requests.get(
                f'{self.endpoint}/{page}/.json',
                timeout=10
            )

        else:
            request = requests.get(
                f'{self.endpoint}/.json',
                timeout=10
            )

        return request.json()

    def post_data(self, page='', info=''):
        """post_data setter method for data in Realtime Database

        Args:
            page (str, optional): URL of an especific page to get the data.
            Defaults to '' if you want get data from the main page

            info (str, optional): data to post. Defaults to ''.
        """
        if page != '' and info != '':
            requests.post(
                f'{self.endpoint}/{page}/.json',
                data=json.dumps(info),
                timeout=10
            )

        elif info != '':
            requests.post(
                f'{self.endpoint}/.json',
                data=json.dumps(info),
                timeout=10
            )

    def patch_data(self, page='', info=''):
        """patch_data Patch data in Realtime Database

        Args:
            page (str, optional): URL of an especific page to get the data.
            Defaults to '' if you want get data from the main page

            info (str, optional): data to post. Defaults to ''.
        """
        if page != '' and info != '':
            requests.patch(
                f'{self.endpoint}/{page}/.json',
                data=json.dumps(info),
                timeout=10
            )
        elif info != '':
            requests.patch(
                f'{self.endpoint}/.json',
                data=json.dumps(info),
                timeout=10
            )


class TwilioAPI:
    """ class for operations with Twilio SMS API
    """
    def __init__(self, account_sid: str, auth_token: str):
        """__init__ Set the account sid and authenticantion token

        Args:
            account_sid (str): account sid
            auth_token (str): authentication token
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = None
        self.sid = None

    def send_sms(self, from_number: str, to_number: str, msg: str):
        """send_sms _summary_

        Args:
            from_number (str): Number from Twilio
            to_number (str): Number you want to send the message.
            msg (str): Message
        """
        self.client = Client(self.account_sid, self.auth_token)
        message = self.client.messages.create(
            to=to_number,
            from_=from_number,
            body=msg
        )
        self.sid = message.sid
        print(message.sid)


class GroqCloud:
    """ class for operations with Groq Cloud
    """
    def __init__(self, job: str, criativity=0, model="llama3-8b-8192"):
        """__init__ Defines initial information to run the requests

        Args:
            job (_type_): Context for the model
            criativity (int, optional): Temperature parameter. Defaults to 0.
            model (str, optional): Model. Defaults to "llama3-8b-8192".
        """
        self.job = job    # informações prévias para o modelo
        self.criativity = criativity   # temperature
        self.model = model   # tipo de modelo
        self.prompt = ChatPromptTemplate.from_messages(
            [("system", f"{self.job}"), ("human", "{text}")]
        )
        self.chat = ChatGroq(
            temperature=self.criativity,
            model_name=f"{self.model}"
        )
        self.response = None
        self.chain = None

    def request(self, msg: str) -> str:
        """request Send a prompt to Groq Cloud

        Args:
            msg (_type_): Prompt for the chat

        Returns:
            str: Response of the prompt
        """
        # getting conexion
        self.chain = self.prompt | self.chat

        # sending request
        self.response = self.chain.invoke({"text": f"{msg}"})

        return self.response.content
