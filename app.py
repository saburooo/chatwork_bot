from flask import Flask
import requests

import os
from pprint import pprint
import json

app = Flask(__name__)

class ChatWork:
    def __init__(self):
        self.api_key = self.get_keys()["api_key"]
        self.room_id = self.get_keys()["room_id"]
        self.message_url = 'https://api.chatwork.com/v2/rooms/{}/messages'.format(self.room_id)

    def chat_post(self, message):
        params = {
            "body":message
        }
        req = requests.post(self.message_url, headers=self.api_key, params=params)
    
    def chat_get(self):
        """
        json_fileで取得したのを頼りにテキストを解析し、それにあったものをpostしたい。
        """
        req = requests.get(self.message_url, headers=self.api_key)
        json_file = req.json()
        pprint(json_file[-1])
    
    def get_keys(self):
        """
        いっそメソッドでローカルにあるjsonもしくは環境変数から必要なものを取ってく
        辞書で返します。
        """
        key_and_id : dict = {}
        try:
            with open('local_key.json') as key:
                key_and_id = json.load(key)
                # print(key_and_id)
        except:
            key_and_id["api_key"] = os.environ["API_KEY"]
            key_and_id["room_id"] = os.environ["ROOM_ID"]
            print("ローカルでは取得できなかった")
        return key_and_id

@app.route('/', methods=['GET', 'POST'])
def index():
    pass

if __name__ == "__main__":
    chat = ChatWork()
    chat.chat_get()
    chat.chat_post("ピッコロ大魔王")
    #app.debug=True
    #app.run()