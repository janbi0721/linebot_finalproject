from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
def mygo_talking(massage):
    image_folder = "Mygo"
    image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    client = genai.Client(
        api_key=os.getenv('GEMINI_API_KEY')
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=f"""
            這是你回答的句子列表{image_files} 
            這是我的回答:{massage}
            請幫我選擇一句合理的句子回答 
            只需要一句 回答應該要長得像以下 不要.jpg
        """
    )
    return response.text


def talking(massage):
    client = genai.Client(
        api_key=os.getenv('GEMINI_API_KEY')
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=f"""
            你是一位心理諮詢師，
            一位朋友向你咨詢聊天
            這是他的:{massage}
            我希望你直接回答他的問題 不用重點
        """
    )
    return response.text

# client = genai.Client(
#     api_key=os.getenv('GEMINI_API_KEY')
# )
# response = client.models.generate_content(
#     model='gemini-2.0-flash-exp', contents=f"""
#         你是一位心理諮詢師，
#         一位朋友向你咨詢聊天
#         這是他說的話:
#         我希望你直接回答他的問題 不用重點
#     """
# )
# print(response.text)