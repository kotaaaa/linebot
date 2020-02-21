#!/home/kk1110/.local/share/virtualenvs/linebot-nxOg-56M/bin/python3.8
import sys
print(sys.path)
import flask

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
print('a')

app = Flask(__name__)

line_bot_api = LineBotApi('HmZrbJbUT+ZnBiwX5uLG8cuKg1Qo3d99+EjRPPjPCVHk1/HgDwMNR45vdJvCaIgxWmOMDnQT9z+AA9eGoKR+/vkZxGqJdZyeExDoVlreubQ73bbUfZeUpEz/AbHJqbZY/bEsXhwVMCAeiiCy15ylSgdB04t89/1O/w1cDnyilFU=')#YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('549900161624cd875236a62d28e567a6')#YOUR_CHANNEL_SECRET

@app.route("/")
def hello_world():
    return "hello world!"

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
