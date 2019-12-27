import requests
import json
import re
import time
import os

tgtoken = str(os.environ.get('TGTOKEN'))
    
def send_mesg_post():
    method = 'https://api.telegram.org/bot' + tgtoken + '/sendMessage'

    mesg_post = requests.post(method, data={
         'chat_id': '@rtttew',
         'text': 'Я бот и работаю на хероку.'
         })

    if mesg_post.status_code != 200:
        raise Exception('send_mesg_post')

while True:
    send_mesg_post()
    time.sleep(5)
