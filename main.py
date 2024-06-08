import os
import tweepy
from dotenv import load_dotenv
from classes import Message, FirebaseAPI, TwilioAPI

db = FirebaseAPI('https://x-bot-borges-default-rtdb.firebaseio.com/')
page = 'actual_index'
index = int(db.get_data(page))   # armazena índice atual
print(f'Index: {index}\n')

msg = Message(index)
msg.get_info()   # busca informações da linha a partir do índice
db.post_data('/Postagens/Horarios', {f'{index}':str(msg.date)})
print(msg.date)

load_dotenv()
xbot = tweepy.Client(
    consumer_key=os.getenv('x_apikey'),
    consumer_secret=os.getenv('x_apisecret'),
    access_token=os.getenv('x_token'),
    access_token_secret=os.getenv('x_tokensecret'),
    bearer_token=os.getenv('x_bearertoken')
)

tweet_body = f'SUPER PROMOÇÃO!! {msg.produto} POR APENAS {msg.valor}\n{msg.link}'
xbot.create_tweet(text=tweet_body)

msg.post_info(['Postado'], column='D')
msg.post_info([tweet_body], column='E')
msg.post_info([str(msg.date)], column='F')

new_sms = TwilioAPI(os.getenv('twilio_sid'), os.getenv('twilio_token'))
sms_body = f"Acabei de postar!\nProduto: {msg.info[0]}\nValor: {msg.info[1]}\n Link {msg.info[2]}"

db.patch_data(info={'actual_index':index + 1})
new_sms.send_sms(os.getenv('number_from'), os.getenv('number_to'),  sms_body)


