import requests
import json

class FirebaseAPI:
    
    def __init__(self, endpoint : str):
        self.endpoint = endpoint
    
    def get_data(self, page=''):
        if page != '':
            request = requests.get(f'{self.endpoint}/{page}/.json')
        
        else:
            request = requests.get(f'{self.endpoint}/.json')
        
        return request.json()

    def post_data(self, page='', info=''):
        if page != '' and info != '':
            request = requests.post(f'{self.endpoint}/{page}/.json', data=json.dumps(info))
        elif info != '':
            request = requests.post(f'{self.endpoint}/.json', data=json.dumps(info))

    def patch_data(self, page='', info=''):
        if page != '' and info != '':
            request = requests.patch(f'{self.endpoint}/{page}/.json', data=json.dumps(info))
        elif info != '':
            request = requests.patch(f'{self.endpoint}/.json', data=json.dumps(info))


if __name__ == "__main__":
    db = FirebaseAPI('https://x-bot-borges-default-rtdb.firebaseio.com/')
    print(db.patch_data('actual_index', {'actual_index':2}))
    print(db.get_data('actual_index')['actual_index'])
        

            