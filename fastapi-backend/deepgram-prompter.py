import requests
from keys import deepgram_key
# Your Deepgram API key
DEEPGRAM_API_KEY = 'deepgram_key'
DEEPGRAM_API_URL = 'https://api.deepgram.com/v1/text-to-speech'

# Text you want to convert
text_data = "Your text from Gemini AI goes here."

# Set up the headers
headers = {
    'Authorization': f'Token {DEEPGRAM_API_KEY}',
    'Content-Type': 'application/json',
}

# Set up the payload
payload = {
    'text': text_data,
    'voice': 'en-US-Wavenet-D',  # You can choose different voices
    'speed': 1.0,
    'pitch': 0.0
}

# Make the request
response = requests.post(DEEPGRAM_API_URL, headers=headers, json=payload)

# Check for successful response
if response.status_code == 200:
    # Save the audio to a file
    with open('output_audio.wav', 'wb') as audio_file:
        audio_file.write(response.content)
    print("Audio saved as output_audio.wav")
else:
    print(f"Error: {response.status_code} - {response.text}")


with open('gemini_output.txt', 'r') as file:
    text_data = file.read()
