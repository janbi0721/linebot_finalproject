from flask import Flask, request, abort, send_from_directory    
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, StickerSendMessage
import os
import requests
from openai import AzureOpenAI
from PIL import Image
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
#ngrk_url
ngrok_url = os.getenv('NGROK_URL')


# 你的 LINE Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 Line 平台
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("無效的簽名。請檢查 CHANNEL_SECRET 是否正確")
        abort(400)
    except Exception as e:
        app.logger.error(f"處理訊息時發生錯誤: {e}")
        abort(500)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應收到的訊息
    text_message = TextSendMessage(text=event.message.text)
    
    # 建立訊息列表
    訊息變數 = []
    for i in range(1):
        訊息變數.append(text_message)

    # 傳送訊息
    line_bot_api.reply_message(event.reply_token, 訊息變數)

if __name__ == "__main__":
    app.run(port=5000)