from fastapi import HTTPException, APIRouter
import requests
import json
from playsound import playsound
from keys import *
import os
from pydub import AudioSegment
from pydub.playback import play
from deprecated_gemini_prompter import *





router = APIRouter()

# Deepgram API credentials
DEEPGRAM_API_KEY = deepgram_key
DEEPGRAM_API_URL = 'https://api.deepgram.com/v1/text-to-speech'

# List of key medical words to emphasize
KEY_MEDICAL_WORDS = ["emergency", "heart attack", "stroke", "bleeding", "respiratory", "pain"]

# In-memory conversation store
conversations = {}

# def emphasize_keywords(text):
#     for word in KEY_MEDICAL_WORDS:
#         text = re.sub(rf'\b{word}\b', f'<emphasis>{word}</emphasis>', text, flags=re.IGNORECASE)
#     return text





import requests
from playsound import playsound

# Your Deepgram API key
def play_audio(audio_file_path):
    playsound(audio_file_path)
def text_to_speech(text):
    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
    headers = {
        "Authorization": f"Token {deepgram_key}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        audio_file_path = "response_audio.mp3"
        with open(audio_file_path, "wb") as f:
            f.write(response.content)
        playsound(audio_file_path)
    else:
        print("Error:", response.status_code, response.text)
        return None




def main():
    # Example string to convert to audio
    prompt_text = "This is a test string that will be converted to audio."
    print("Generating audio for prompt:", prompt_text)

    # Generate audio from the string
    audio_file_path = text_to_speech(prompt_text)

    if audio_file_path:
        print(f"Playing audio from: {audio_file_path}")
        play_audio(audio_file_path)
    else:
        print("Failed to generate audio.")

if __name__ == "__main__":
    main()