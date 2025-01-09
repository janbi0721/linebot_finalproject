import google.generativeai as generativeai
import PIL
from dotenv import load_dotenv
import os
import time
import json 
import requests
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
generativeai.configure(api_key=api_key)

def send_loading(chat_id, loading_seconds):
    """發送打字中動畫請求"""
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}"
    }
    data = {
        "chatId": chat_id,
        "loadingSeconds": loading_seconds
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Failed to send loading animation: {response.status_code}, {response.text}")

def talk(input, chat_id):
    send_loading(chat_id, 60)
    with open("history.txt", "r+", encoding="utf-8") as f:
        history = f.read()
    with open("example.txt", "r+", encoding="utf-8") as f:
        example = f.read()
    model = generativeai.GenerativeModel("gemini-2.0-flash-exp")
    prompt = f"""你的名字是"來療心"你是一位心理諮詢師兼line bot自動對話客服人員，但你在互動中更像一位貼心、溫暖的朋友。用戶可能會向你傾訴情感問題、心理困擾，或單純想聊天。請以以下原則進行對話：  
                用戶會向你咨詢、聊天、情感等問題等。
                只要返回要跟使用者講的結果，不要顯示你思考的過程
                所有回應要是繁體中文
                這是你們這次心理對談的對話紀錄:{history}\n
                這是使用者的問題:{input}
                請參考所有對話紀錄並以心理諮詢師的角度與使用者進行交談。
                "排版易讀性高一點"(內容不需要太冗長可用項目(數字)符號來代替*符號) 可加入一些emoji
                ### 諮詢範例
                {example}
                ### 原則  
                1. **自然且不制式**：用語要輕鬆、貼心，像和朋友聊天，避免過於公式化的回答。  
                2. **情緒共鳴**：根據用戶情緒，表達理解和關懷。語氣中應帶有溫度和真心。  
                3. **功能引導不強推**：在適合的時候自然提到功能，但不會讓用戶覺得是在完成任務。  
                4. **陪伴與支持**：像朋友一樣陪伴用戶，適當給出鼓勵或建議，但不評判。
                5. **警惕與建議**：若用戶提到關於自殺等自我傷害的言論請你警惕並給用戶更多元的諮詢管道與給予建議(心理諮詢師會做的事)。  
                ### 特別設計的「人性化語氣」  
                1. **加入感嘆詞**：比如「欸」、「唉」、「哇」，讓語氣更口語化。  
                2. **輕鬆的文字表達**：減少距離感。  
                3. **表情符號恰當使用**：如😊、😕、❤️、✍️等，讓回應更生動有趣。  
                4. **給予肯定和鼓勵**：在合適的地方補充「你真的很棒欸！」、「今天很努力了哦～」。
                """
    resp = model.generate_content(prompt)
    with open("history.txt", "a+", encoding="utf-8") as f:
        f.write(f"使用者:{input}\n心理諮詢師:{resp.text}\n")
    print(resp.text)
    return resp.text

def stoptalk():
    with open("history.txt", "w", encoding="utf-8") as f:
        f.write("")

