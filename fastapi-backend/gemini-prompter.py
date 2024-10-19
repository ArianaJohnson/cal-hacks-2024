import google.generativeai as genai
import os
from keys import gemini_key

genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)