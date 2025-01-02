#關鍵字回應功能(chatgpt建議)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip().lower()

    # 關鍵字回應
    if user_message in ["你好", "hello"]:
        reply_message = "你好！有什麼我可以幫助的嗎？"
    elif user_message in ["幫助", "help"]:
        reply_message = "您可以輸入以下指令：\n1. 聊天\n2. 紀錄\n3. 紀錄睡眠時間\n4. 產生分析圖表"
    else:
        reply_message = f"你說的是：{user_message}"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
