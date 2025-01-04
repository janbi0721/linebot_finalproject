# 注意 如果要用RICH MENU 要去另一個終端打 curl -X POST http://localhost:5000/create_richmenu
from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, MessagingApiBlob
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction,
    FlexSendMessage, RichMenu, RichMenuBounds, RichMenuArea, URIAction
)
from linebot.v3.webhook import WebhookHandler
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

# 設置日誌記錄 - 新增 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')
messaging_api = MessagingApi(channel_access_token)
messaging_api_blob = MessagingApiBlob(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 LINE 平台
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
    # 原本的回應邏輯
    user_message = event.message.text.strip()
    reply_message = f"你說的是：{user_message}"
    messaging_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

@app.route("/create_richmenu", methods=['POST'])
def create_richmenu():
    """建立 Rich Menu"""
    try:
        # 刪除現有的 Rich Menu
        rich_menu_list = messaging_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            messaging_api.delete_rich_menu(rich_menu.rich_menu_id)

        # 定義 Rich Menu 的結構
        rich_menu = RichMenu(
            size={"width": 2500, "height": 1686},  # Rich Menu 的尺寸
            selected=True,
            name="Rich Menu 1",
            chat_bar_text="主選單",  # 聊天室底部顯示的按鈕文字
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
                    action=MessageAction(label="紀錄今日心情", text="紀錄今日心情")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
                    action=MessageAction(label="紀錄今日日記", text="紀錄今日日記")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=843, width=1250, height=843),
                    action=MessageAction(label="紀錄睡眠情況", text="紀錄睡眠情況")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=843, width=1250, height=843),
                    action=MessageAction(label="分析圖表", text="分析圖表")
                ),
            ]
        )

        # 建立 Rich Menu
        rich_menu_response = messaging_api.create_rich_menu(rich_menu)
        rich_menu_id = rich_menu_response.rich_menu_id

        # 上傳新的 Rich Menu 圖片
        with open(r"D:\程式設計3\linebot_finalproject\new_richmenu_resized.png", "rb") as f:  # 確保 new_richmenu_resized.png 是你的新圖片檔
            messaging_api_blob.set_rich_menu_image(rich_menu_id, "image/png", f)

        # 啟用新的 Rich Menu
        messaging_api.set_default_rich_menu(rich_menu_id)

        logger.info("Rich Menu 更新成功！")  # 新增: 日誌記錄

        return "Rich Menu 更新成功！", 200

    except Exception as e:
        logger.error(f"更新 Rich Menu 時發生錯誤: {str(e)}")  # 新增: 日誌記錄
        return f"更新 Rich Menu 時發生錯誤: {str(e)}", 500

if __name__ == "__main__":
    app.run(port=5000)
