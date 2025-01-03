from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
image_folder = "Mygo圖包"
image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

client = genai.Client(
    api_key=os.getenv('GEMINI_API_KEY')
)
response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents=f"""
        這是我回答的句子列表{image_files} 
        這是我的回答:你是gay嗎
        請幫我選擇一句比較合理的句子 
        只需要一句 回答應該要長得像以下 不要.jpg
    """
)
print(response.text)

