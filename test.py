from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(
    api_key=os.getenv('GEMINI_API_KEY')
)
response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents='你可以對圖片進行辨識嗎'
)
print(response.text)