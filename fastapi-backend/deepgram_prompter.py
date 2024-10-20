
from fastapi import HTTPException, APIRouter
import requests
import re
from keys import *
import os


router = APIRouter()

# Deepgram API credentials
DEEPGRAM_API_KEY = deepgram_key
DEEPGRAM_API_URL = 'https://api.deepgram.com/v1/text-to-speech'

# List of key medical words to emphasize
KEY_MEDICAL_WORDS = ["emergency", "heart attack", "stroke", "bleeding", "respiratory", "pain"]

# In-memory conversation store
conversations = {}

def emphasize_keywords(text):
    for word in KEY_MEDICAL_WORDS:
        text = re.sub(rf'\b{word}\b', f'<emphasis>{word}</emphasis>', text, flags=re.IGNORECASE)
    return text


def convert_text_to_speech(text: str) -> str:
    ssml_text = f"<speak>{text}</speak>"  # Wrap text in SSML
    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'text': ssml_text,
        'voice': 'en-US-Wavenet-D',
        'ssml': True
    }

    response = requests.post(DEEPGRAM_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        audio_file_path = 'output_audio.wav'
        with open(audio_file_path, 'wb') as file:
            file.write(response.content)
        return audio_file_path
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text

