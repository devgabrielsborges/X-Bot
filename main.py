import os
import tweepy
from dotenv import load_dotenv
from classes import Message, FirebaseAPI, TwilioAPI, GroqCloud

db = FirebaseAPI('https://x-bot-borges-default-rtdb.firebaseio.com/')
page = 'actual_index'
index = int(db.get_data(page))   # armazena índice atual
print(f'Index: {index}\n')

msg = Message(index)
msg.get_info()   # busca informações da linha a partir do índice
db.post_data('/Postagens/Horarios', {f'{index}':str(msg.date)})
print(msg.date)

load_dotenv()

prompt_msg = f"Imagine que você é um estrategista em posts de tweets sobre promoções imperdíveis. Crie um texto curto e poderoso para vender um/uma {msg.produto} que custa {msg.valor}. O texto deve ser próprio para tweets e deve trazer a ideia de urgência para que os usuários se interessem pelo produto. Lembrando que vendemos produtos de terceiros, não são produtos nossos. Texto em português do Brasil. Até 280 caracteres"

groq_chat = GroqCloud("You are especialist at sales and marketing",criativity=1.21, model="llama3-70b-8192")
tweet_body = f"{groq_chat.request(prompt_msg)}\n{msg.link}" 
print(tweet_body)

xbot = tweepy.Client(
    consumer_key=os.getenv('x_apikey'),
    consumer_secret=os.getenv('x_apisecret'),
    access_token=os.getenv('x_token'),
    access_token_secret=os.getenv('x_tokensecret'),
    bearer_token=os.getenv('x_bearertoken')
)

xbot.create_tweet(text=tweet_body)

msg.post_info(['Postado'], column='D')
msg.post_info([tweet_body], column='E')
msg.post_info([str(msg.date)], column='F')

new_sms = TwilioAPI(os.getenv('twilio_sid'), os.getenv('twilio_token'))
sms_body = f"Acabei de postar!\nProduto: {msg.info[0]}\nValor: {msg.info[1]}\n Link {msg.info[2]}"

db.patch_data(info={'actual_index':index + 1})
new_sms.send_sms(os.getenv('number_from'), os.getenv('number_to'),  sms_body)


