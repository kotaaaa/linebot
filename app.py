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

import mysql.connector

app = Flask(__name__)
app.config.from_json('development.json', True)

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
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    tobuy_lists = event.message.text.split('\n')
    if len(tobuy_lists) == 1 & (tobuy_lists[0] == "clear" or tobuy_lists[0] == "クリア"):
        send_sql = u"DELETE from itemTable where user_id = '"+event.source.user_id+"'"
    else:    
        for tobuy_list in tobuy_lists:
            send_sql = u"INSERT INTO itemTable(user_id, item, todo_flg) VALUES('"+event.source.user_id+"','"+tobuy_list+"','1') ON DUPLICATE KEY UPDATE user_id = '"+event.source.user_id+"',item = '"+tobuy_list+"', todo_flg = IF(todo_flg = 1,0,1)"

    db_text_save(send_sql)

    select_sql = u"select item from itemTable where user_id = '"+event.source.user_id+"' and todo_flg = 1"

    latest_todos_lists = db_text_select(select_sql)
    latest_todos_lists = [str(i[0]) for i in latest_todos_lists]
    latest_todos = '\n'.join(latest_todos_lists)
    if latest_todos == "":
        latest_todos = "なにもなし😄"
    else:
        latest_todos = "あなたのTODOリストはこれだよ！:D\n===================\n" + latest_todos + "\n==================="
    line_bot_api.reply_message(
        event.reply_token,
        [
        TextSendMessage(text=latest_todos),
        ])

def getConnection():
    return mysql.connector.connect(
            app.config['DBHOST'],
            app.config['DBNAME'],
            app.config['DBUSER'],
            app.config['DBPASS'],
            app.config['DBCHARSET'],
            )

def db_text_save(sql):
    connector = getConnection()
    cursor = connector.cursor()
    cursor.execute(sql)
    connector.commit()
    cursor.close()
    connector.close()

def db_text_select(sql):
    connector = getConnection()
    cursor = connector.cursor()
    cursor.execute(sql)
    text = cursor.fetchall()
    cursor.close()
    connector.close()
    return text

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
