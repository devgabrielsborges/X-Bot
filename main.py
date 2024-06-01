from bot import XBot, Message
from firebase import FirebaseAPI

db = FirebaseAPI('https://x-bot-borges-default-rtdb.firebaseio.com/')
page = 'actual_index'
index = db.get_data(page)[page]   # armazena índice atual

msg = Message(index)
msg.get_info()   # busca informações da linha a partir do índice
msg.post_info([str(msg.date)])
db.post_data('/Postagens/Horarios', {f'{index}':str(msg.date)})
print(msg.date)

