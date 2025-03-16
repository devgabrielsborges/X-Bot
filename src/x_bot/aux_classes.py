"""Classes & methods for main script"""

from datetime import datetime
from pytz import timezone
from twilio.rest import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class Product:
    """ Class for storage and manipulate the product data"""
    @staticmethod   # function to get the current datetime
    def _current_datetime() -> str:
        return str(datetime.now(timezone("Brazil/East")))

    def __init__(self, produto: str, valor: float, ultimo_valor: float, link: str):
        """__init__ Inicial information

        Args:
            produto (str): Product name
            valor (float): Price
            ultimo_valor (float): Last price
            link (str): Link
        """
        self.produto = produto
        self.valor = valor
        self.ultimo_valor = ultimo_valor
        self.link = link
        self.date = self._current_datetime()
        self.info = None

    def list_info(self) -> dict:
        """set_info for future operations

        Returns:
            dict: [str, float, float, link]
        """
        self.info = [self.produto, self.valor, self.ultimo_valor, self.link]
        return self.info


class TwilioAPI:
    """ class for operations with Twilio SMS API"""
    def __init__(self, account_sid: str, auth_token: str):
        """__init__ Set the account sid and authenticantion token

        Args:
            account_sid (str): account sid
            auth_token (str): authentication token
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client: Client | None = None
        self.sid: str = ''

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
        self.sid: str = message.sid


class GroqCloud:
    """ class for operations with Groq Cloud"""
    def __init__(self, job: str, criativity: float = 0.0, model: str = "llama3-8b-8192"):
        """__init__ Defines initial information to run the requests

        Args:
            job (_type_): Context for the model
            criativity (int, optional): Temperature parameter. Defaults to 0.
            model (str, optional): Model. Defaults to "llama3-8b-8192".
        """
        self.job = job    # previous information for the model
        self.criativity = criativity   # temperature
        self.model = model   # model type
        self.prompt = ChatPromptTemplate.from_messages(
            [("system", f"{self.job}"), ("human", "{text}")]
        )
        self.chat = ChatGroq(
            temperature=self.criativity,
            model_name=f"{self.model}"
        )
        self.response: str | None = None
        self.chain: self.chain | self.prompt | None = None

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
