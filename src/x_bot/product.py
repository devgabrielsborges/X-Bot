from datetime import datetime
import pytz 


class Product:
    """ Class for storage and manipulate the product data"""
    @staticmethod   # function to get the current datetime
    def _current_datetime() -> str:
        return str(datetime.now(pytz.timezone("Brazil/East")))

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