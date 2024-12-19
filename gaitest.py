import os
import google.generativeai as generativeai
from dotenv import load_dotenv  # add this line to the top of your file
load_dotenv()

generativeai.configure(api_key=os.getenv('KEY'))
response = generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content('你好')
print(response.text)