from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


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
