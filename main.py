import os
from dotenv import load_dotenv
from classes import Message, FirebaseAPI, TwilioAPI, Xbot

db = FirebaseAPI('https://x-bot-borges-default-rtdb.firebaseio.com/')
page = 'actual_index'
index = int(db.get_data(page))   # armazena índice atual

msg = Message(index)
msg.get_info()   # busca informações da linha a partir do índice
msg.post_info([str(msg.date)])
db.post_data('/Postagens/Horarios', {f'{index}':str(msg.date)})
print(msg.date)

load_dotenv()
new_sms = TwilioAPI(os.getenv('sid'), os.getenv('token'))
sms_body = f"Acabei de postar!\nProduto: {msg.info[0]}\nValor: {msg.info[1]}\n Link{msg.info[2]}"

db.patch_data(info={'actual_index':index + 1})
new_sms.send_sms(os.getenv('from'), os.getenv('to'),  sms_body)


