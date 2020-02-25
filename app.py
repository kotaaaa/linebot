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

app = Flask(__name__)

f= open("dev_log/log1", mode='a',encoding="utf-8")
#f.write(os.environ.get('LINECHANNELACCESSTOKEN'))

line_bot_api = LineBotApi('HmZrbJbUT+ZnBiwX5uLG8cuKg1Qo3d99+EjRPPjPCVHk1/HgDwMNR45vdJvCaIgxWmOMDnQT9z+AA9eGoKR+/vkZxGqJdZyeExDoVlreubQ73bbUfZeUpEz/AbHJqbZY/bEsXhwVMCAeiiCy15ylSgdB04t89/1O/w1cDnyilFU=')#YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('549900161624cd875236a62d28e567a6')#YOUR_CHANNEL_SECRET


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(debug = True)
