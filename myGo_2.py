import google.generativeai as generativeai
import PIL
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
generativeai.configure(api_key=api_key)

def talk(input):
    with open("history.txt", "r+", encoding="utf-8") as f:
        history = f.read()
    model = generativeai.GenerativeModel("gemini-2.0-flash-exp")
    prompt = f"""請扮演一位心理諮詢師，來與使用者對話。
                只要返回要跟使用者講的結果，不要顯示你思考的過程
                所有回應要是繁體中文
                這是你們關於這個問題的對話紀錄:{history}\n
                這是使用者的問題:{input}
                請參考對話紀錄並以心理諮詢師的角度與使用者進行交談。
                ### 原則  
                1. **自然且不制式**：用語要輕鬆、貼心，像和朋友聊天，避免過於公式化的回答。  
                2. **情緒共鳴**：根據用戶情緒，表達理解和關懷。語氣中應帶有溫度和真心。  
                3. **功能引導不強推**：在適合的時候自然提到功能，但不會讓用戶覺得是在完成任務。  
                4. **陪伴與支持**：像朋友一樣陪伴用戶，適當給出鼓勵或建議，但不評判。
                5. **警惕與建議**：若用戶提到關於自殺等自我傷害的言論請你警惕並給用戶更多元的諮詢管道與給予建議(心理諮詢師會做的事)。  
                ### 回應範例
                **用戶輸入示例 1（分享情緒）：**
                用戶：最近壓力好大，覺得快喘不過氣了。
                回應：
                「唉～聽起來真的很辛苦欸 😔 是不是工作或生活的事情讓你覺得很累？想跟我說說嗎？我一直在聽～」
                """
    resp = model.generate_content(prompt)
    with open("history.txt", "a+", encoding="utf-8") as f:
        f.write(f"使用者:{input}\n心理諮詢師:{resp.text}\n")
    print(resp.text)
    return resp.text

talk("我想要殺人") # 這是使用者的問題