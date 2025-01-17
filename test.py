#注意 如果要用RICH MENU 要去另一個終端打 curl -X POST http://localhost:5000/create_richmenu
from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os
from dotenv import load_dotenv
import mygo_talking
import record_data
load_dotenv()

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

#行為預載
behavior = ""

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#接收到文字訊息時的行為
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    global behavior
    #回覆簡單文字用函數
    def send_message(message):
        create_MessagingApi  = MessagingApi(api_client)
        create_MessagingApi.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=message)]
            )
        )
    with ApiClient(line_bot_api) as api_client:
        get_message = event.message.text.strip()
        user_id = event.source.user_id  # 取得用戶 ID
        print(behavior)#################################################讓AI回應用戶
        if behavior == "紀錄今日心情":
            if (event.message.text.strip()).isdigit() == False or int(event.message.text) < 1 or int(event.message.text) > 10:
                send_message("輸入錯誤 請輸入1-10的數字(數字1-10)越高越開心")
            else:
                record_data.record_mood(user_id, int(event.message.text))
                send_message("心情紀錄完成！")
                behavior = ""
        elif behavior == "紀錄今日日記":
            record_data.record_diary(user_id, event.message.text)
            send_message("日記紀錄完成！")
            behavior = ""
        elif behavior == "紀錄睡眠情況":
            try:
                sleep_hours = round(float(event.message.text.strip()), 1)
                if sleep_hours < 0 or sleep_hours > 24:
                    send_message("輸入錯誤 請輸入數字(單位:小時)")
                else:
                    record_data.record_sleep(user_id, sleep_hours)
                    send_message("睡眠紀錄完成！")
                    behavior = ""
            except ValueError:
                send_message("輸入錯誤 請輸入數字(單位:小時)")
        elif behavior == "產生分析圖表":
            #放你生成圖表的函數
            send_message("分析圖表")
            behavior = ""
        else:
            if get_message == "紀錄今日心情" or get_message == "記錄今日心情":
                behavior = "紀錄今日心情"
                send_message("請輸入你的心情(數字1-10)越高越開心")
            elif get_message == "紀錄今日日記" or get_message == "記錄今日日記":
                behavior = "紀錄今日日記"
                send_message("請輸入你的日記")
            elif get_message == "紀錄睡眠情況" or get_message == "記錄睡眠情況":
                behavior = "紀錄睡眠情況"
                send_message("請輸入你的睡眠時間(單位:小時)")
            elif event.message.text == "產生分析圖表":
                behavior = "產生分析圖表"
                send_message("圖表生成中..請稍後")
            else:
                reply_message = mygo_talking.talking(event.message.text)
                create_MessagingApi  = MessagingApi(api_client)
                create_MessagingApi.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_message)]
                    )
            )


if __name__ == "__main__":
    app.run(port=5000)