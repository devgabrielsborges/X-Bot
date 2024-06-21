import os
import tweepy
from dotenv import load_dotenv
from classes import SheetXlsx, FirebaseAPI, TwilioAPI, GroqCloud

db = FirebaseAPI('https://x-bot-borges-default-rtdb.firebaseio.com/')
PAGE = 'actual_index'
index = int(db.get_data(PAGE))   # armazena índice atual
print(f'Index: {index}\n')

wb = SheetXlsx(r"Projeto-X-Bot", r"Projeto-X-Bot.xlsx", index)
wb.get_info()   # busca informações da linha a partir do índice
db.post_data('/Postagens/Horarios', {f'{index}': str(wb.date)})
print(wb.date)

load_dotenv()

prompt_msg = (
    f"Você é um estrategista em posts de tweets sobre promoções imperdíveis."
    f"Faça um texto curto e eficaz para vender {wb.produto}. Custa {wb.valor}."
    f"O texto deve ser próprio para tweets e deve trazer a ideia de urgência"
    f"para que os usuários se interessem pelo produto."
    f"Lembrando que vendemos produtos de terceiros, não são produtos nossos."
    f"Texto em português do Brasil. Até 280 caracteres"
)

groq_chat = GroqCloud(
    "You're especialist at sales and marketing and post sales promotions",
    criativity=1.15,
    model="llama3-70b-8192"
)

tweet_body = f"{groq_chat.request(prompt_msg)}\n{wb.link}"
print(tweet_body)

xbot = tweepy.Client(
    consumer_key=os.getenv('x_apikey'),
    consumer_secret=os.getenv('x_apisecret'),
    access_token=os.getenv('x_token'),
    access_token_secret=os.getenv('x_tokensecret'),
    bearer_token=os.getenv('x_bearertoken')
)

xbot.create_tweet(text=tweet_body)

wb.post_info(['Postado', tweet_body])

new_sms = TwilioAPI(os.getenv('twilio_sid'), os.getenv('twilio_token'))
sms_body = (
    f"Acabei de postar!\nProduto: "
    f"{wb.info[0]}\nValor: {wb.info[1]}\n Link {wb.info[2]}"
)

db.patch_data(info={'actual_index': index + 1})
new_sms.send_sms(os.getenv('number_from'), os.getenv('number_to'),  sms_body)
