import google.generativeai as genai
import os
#from keys import gemini_key

genai.configure(api_key='')
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("give us a hackathon project prompt.")
print(response.text)