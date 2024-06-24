"""
Runs the automation. First, retrieve the current index for the post,
using this index to search for the product in the spreadsheet.
Then, based on the product information, establish a chat in
Groq Cloud with the chosen specifications From there, the model
generates a message for the tweet to be posted, and the tweet is then
posted Finally, the bot prepares to send an SMS to the phone number you have
registered with Twilio, containing a customizable message
"""

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
if None not in wb.get_info():
    if wb.info[2] >= wb.info[1]:
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
            consumer_key=os.getenv('X_APIKEY'),
            consumer_secret=os.getenv('X_APISECRET'),
            access_token=os.getenv('X_TOKEN'),
            access_token_secret=os.getenv('X_TOKENSECRET'),
            bearer_token=os.getenv('X_BEARERTOKEN')
        )

        xbot.create_tweet(text=tweet_body)

        wb.post_info(['Postado', tweet_body])

        new_sms = TwilioAPI(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        sms_body = (
            f"Acabei de postar!\nProduto: "
            f"{wb.info[0]}\nValor: {wb.info[1]}\n Link {wb.info[3]}"
        )

        db.patch_data(info={'actual_index': index + 1})
        new_sms.send_sms(os.getenv('NUMBER_FROM'), os.getenv('NUMBER_TO'), sms_body)
else:
    try:
        print(
            f"None not in product info? -> {None not in wb.get_info()}",
            f"Last price <= Actual price? -> {wb.info[2] >= wb.info[1]}"
        )
    except Exception as error:
        raise error
