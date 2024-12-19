from dotenv import load_dotenv
load_dotenv()



import os
import google.generativeai as generativeai
generativeai.configure(api_key=os.getenv('KEY'))
repspone = generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content('你是誰?')
print(repspone.text)