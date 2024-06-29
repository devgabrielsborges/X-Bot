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
import firebase_admin
from firebase_admin import db, credentials
from classes import Product, TwilioAPI, GroqCloud

# auth to firebase

cred = credentials.Certificate('fire_credentials.json')
firebase_admin.initialize_app(
    cred,
    {'databaseURL': 'https://x-bot-borges-default-rtdb.firebaseio.com'}
)
index = db.reference('/actual_index').get()
print(f'Index: {index}\n')

item = Product(
    db.reference(f'/itens/{index}/Produto').get(),
    db.reference(f'/itens/{index}/Valor').get(),
    db.reference(f'/itens/{index}/Ultimo_valor').get(),
    db.reference(f'/itens/{index}/Link').get()
)

if None not in item.set_info():
    if item.info[2] >= item.info[1]:
        db.reference(f'/itens/{index}').update({'Data': item.date})
    print(item.date)

    load_dotenv()

    with open('prompt.txt', 'r', encoding='UTF8') as prompt:
        prompt_msg = prompt.read().format(item.produto, item.valor)

    groq_chat = GroqCloud(
        "You're especialist at sales and marketing and post sales promotions",
        criativity=1.15,
        model="llama3-70b-8192"
        )

    tweet_body = f"{groq_chat.request(prompt_msg)}\n{item.link}"
    print(tweet_body)

    xbot = tweepy.Client(
        consumer_key=os.getenv('X_APIKEY'),
        consumer_secret=os.getenv('X_APISECRET'),
        access_token=os.getenv('X_TOKEN'),
        access_token_secret=os.getenv('X_TOKENSECRET'),
        bearer_token=os.getenv('X_BEARERTOKEN')

        )

    xbot.create_tweet(text=tweet_body)
    db.reference(f'/itens/{index}').update({'Mensagem': tweet_body})

    new_sms = TwilioAPI(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
    sms_body = (
        f"Acabei de postar!\nProduto: "
        f"{item.info[0]}\nValor: {item.info[1]}\n Link {item.info[3]}"
        )
    db.reference(f'/itens/{index}').update({'Postado': True})
    db.reference('/').update({'actual_index': index + 1})
    new_sms.send_sms(os.getenv('NUMBER_FROM'), os.getenv('NUMBER_TO'), sms_body)
else:
    try:
        print(
            f"None in product info? -> {None in item.info}\n",
            f"Info: {item.info}"
        )
    except Exception as error:
        raise error
