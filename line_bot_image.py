#注意 如果要用RICH MENU 要去另一個終端打 curl -X POST http://localhost:5000/create_richmenu
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction,
    FlexSendMessage,RichMenu,RichMenuBounds,RichMenuArea,URIAction
)
import os
from dotenv import load_dotenv
import mygo_talking


load_dotenv()

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


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
    get_message = mygo_talking.talking(user_message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=get_message))


@app.route("/create_richmenu", methods=['POST'])
def create_richmenu():
    """建立 Rich Menu"""
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
                action=MessageAction(label="產生分析圖表", text="產生分析圖表")
            ),
        ]
    )

    # 建立 Rich Menu
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu)

    # 上傳 Rich Menu 圖片
    with open("richmenu.png", "rb") as f:  # 確保 richmenu.png 是你的圖片檔
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

    # 啟用 Rich Menu
    line_bot_api.set_default_rich_menu(rich_menu_id)

    return "Rich Menu 建立成功！", 200



if __name__ == "__main__":
    app.run(port=5000)