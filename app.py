from flask import Flask
import requests

import os
from pprint import pprint
import json
import re

app = Flask(__name__)


class MessageAnalize:
    def __init__(self, json_file):
        """
        このままクラスが増えすぎるのもまずいと思った。
        このクラスでメッセージとその他諸々を解析する。
        """
        self.message_id : str = json_file["message_id"]
        self.body : str = json_file["body"]
        self.name : str = json_file["account"]["name"]
        self.account : str = json_file["account"]["account_id"]
        self.q_and_a = re.compile('質問|在宅(で|も|は).*?|これは')

    def greet(self) -> dict:
        return re.search("おはよう|こん(にち|ばん)[はわ]", self.body)
    
    def parrot(self):
        """
        オウム返し
        """
        return self.body

    def ngword(self):
        """
        NGワードが入っているかどうか確認する。
        """
        return re.search("アホ|バカ|馬鹿|阿保", self.body)

    def inword(self, words):
        return re.search(words, self.body)

    def messagegenerate(self):
        """
        メッセージを受け取った情報を基に生成する。
        """
        if self.ngword():
            return "禁止ワードを入れるとかwww" + self.name + "君ちぃーっすwww"
        if self.greet():
            return '[rp aid=' + self.account + ' to=' + self.message_id + ']' + self.name + "さん、こんにちは今日もご機嫌ですね",
        if self.inword('(なん|何)だ(きみ|君)は(.*?!)'):
            return "なんだチミ(君)はってか!? え!? なんだチミはってか！そうです、私が変なおじさんです"


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
        req = requests.put(self.message_url + 'read', headers=self.api_key)
    
    def chat_get(self) -> list:
        """
        json_fileで取得したのを頼りにテキストを解析し、それにあったものをpostしたい。
        """
        req = requests.get(self.message_url, headers=self.api_key)
        try:
            json_file_list = req.json()
        except:
            json_file_list = {}
        if json_file_list != {}:
            pprint(json_file_list[-1])
        else:
            print("ゲットできず")
        return json_file_list
    
    def get_keys(self) -> dict:
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
    chat = ChatWork()
    for c in chat.chat_get():
        m = MessageAnalize(c)
    
    return chat.chat_post()


if __name__ == "__main__":
    chat = ChatWork()
    for c in chat.chat_get():
        m = MessageAnalize(c)
        chat.chat_post(m.messagegenerate())
    #app.debug=True
    #app.run()
