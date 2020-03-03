#!/home/kk1110/.local/share/virtualenvs/linebot-nxOg-56M/bin/python3.8
# coding:utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ファイルハンドラ
fh = logging.FileHandler('advance_logging.log')
fh.setLevel(logging.DEBUG)

# フォーマット
formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.debug('logging.debug.')
logger.info('logging.info.')
logger.warning('logging.warning.')
logger.error('logging.error.')
logger.critical('logging.critical.')
#ログ出力関係ここまで

import json
import os
import mysql.connector

app = Flask(__name__)
app.config.from_json('development.json', True)

f= open("dev_log/log1", mode='a',encoding="utf-8")

line_bot_api = LineBotApi(app.config['LINECHANNELACCESSTOKEN'])#YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler(app.config['LINECHANNELSECRET'])#YOUR_CHANNEL_SECRET


@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/test", methods=['GET'])
def test():
        return 'Test OK!', 404

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    #ログをテキストファイルに保存
    body_ = json.loads(body)
    f.write(str(body_["events"][0]["message"]["text"])+'\n')#とりあえず，これで，printする形にする．
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    tobuy_lists = event.message.text.split('\n')
    for tobuy_list in tobuy_lists:
        f.write(str(tobuy_list)+'\n')
        f.write(str(event["source"]["userId"])+'\n')
        send_sql = u"insert into testTable values('"+"5"+"','"+event.["source"]["userId"]+"')"
        db_text_save(send_sql)
        line_bot_api.reply_message(
            event.reply_token,
            [
            TextSendMessage(text=tobuy_list),
            TextSendMessage(text=tobuy_list)
            ])

def getConnection():
    return mysql.connector.connect(
            host="mysql8078.xserver.jp",
            db="kk1110_linebot",
            user="kk1110_userlbot",
            passwd="Kota0108",
            charset="utf8"
            )

def db_text_save(sql):
    connector = getConnection()
    cursor = connector.cursor()
    # sql = u"insert into testTable values('2','java')"
    cursor.execute(sql)
    connector.commit()
    cursor.close()
    connector.close()
    # return "DB saved!"


@app.route('/db')
def db_save():
    connector = getConnection()
    cursor = connector.cursor()
    sql = u"insert into testTable values('2','java')"
    cursor.execute(sql)
    connector.commit()
    cursor.close()
    connector.close()

    return "DB saved!"

if __name__ == "__main__":
    app.run(debug = True)
