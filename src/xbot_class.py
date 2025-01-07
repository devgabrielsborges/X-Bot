import os
import tweepy
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db, credentials
from aux_classes import Product, TwilioAPI, GroqCloud


class Xbot:

    @staticmethod
    def set_credentials() -> credentials.Certificate:
        """
        Set the credentials for the firebase connection.
        """
        cred = credentials.Certificate('credentials.json')
        return cred

    @staticmethod
    def get_item(index) -> Product:
        """
        Set the item to be posted.
        """
        item = Product(
            str(db.reference(f'/itens/{index}/Produto').get()),
            float(db.reference(f'/itens/{index}/Valor').get()),
            float(db.reference(f'/itens/{index}/Ultimo_valor').get()),
            str(db.reference(f'/itens/{index}/Link').get())
        )
        return item

    def __init__(self, index: int = None):
        load_dotenv()
        self.credentials = self.set_credentials()

        # Initialize Firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                self.credentials,
                {'databaseURL': os.getenv('FIREBASE_URL')}
            )

        if index is None:
            self.index = db.reference('/actual_index').get()
        else:
            self.index = index
        self.item = self.get_item(self.index)
        self.tweet_body = None

    def set_tweet_body(self, criativity: int = 1.15, model_setting: str = "llama3-70b-8192") -> str:
        """
        Get the tweet body.
        """
        if None not in self.item.list_info():
            if self.item.info[2] >= self.item.info[1]:
                db.reference(f'/itens/{self.index}').update({'Data': self.item.date})
            print(self.item.date)

            with open('prompt.txt', 'r', encoding='UTF8') as prompt:
                prompt_msg = prompt.read().format(self.item.produto, self.item.valor)

            groq_chat = GroqCloud(
                "You're especialist at sales and marketing and post sales promotions",
                criativity=criativity,
                model=model_setting
            )

            tweet_body = f"{groq_chat.request(prompt_msg)}\n{self.item.link}"

            return tweet_body

    def post_tweet(self, manual_post: bool = False):
        """
        Post the tweet.
        """
        twitter_client = tweepy.Client(
            consumer_key=os.getenv('X_APIKEY'),
            consumer_secret=os.getenv('X_APISECRET'),
            access_token=os.getenv('X_TOKEN'),
            access_token_secret=os.getenv('X_TOKENSECRET'),
            bearer_token=os.getenv('X_BEARERTOKEN')
        )

        self.tweet_body = self.set_tweet_body()
        twitter_client.create_tweet(text=self.tweet_body)

        db.reference(f'/itens/{self.index}').update({'Mensagem': self.tweet_body})
        db.reference(f'/itens/{self.index}').update({'Postado': True})

        if not manual_post:
            db.reference('/').update({'actual_index': self.index + 1})

    def send_sms(self):
        """send_sms Send an SMS message to a number
        """
        new_sms = TwilioAPI(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        sms_body = (
            f"Acabei de postar!\nProduto: "
            f"{self.item.produto}\nValor: {self.item.valor}\n{self.item.link}"
        )

        new_sms.send_sms(
            os.getenv('NUMBER_FROM'),
            os.getenv('NUMBER_TO'),
            sms_body
        )