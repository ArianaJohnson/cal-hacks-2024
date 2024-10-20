import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from pydantic import BaseModel, UUID4
from typing import List, Optional
from keys import GEMINI_KEY
from models import *
from deepgram_prompter import text_to_speech
from playsound import playsound

# Configure the Google Gemini model
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

router = APIRouter()

# Input Pydantic model for request body
class base_inputs:
    name: str = 'John'
    phone: str = '416-234-5837'
    medical_conditions: List[str] = ['asthma']
    allergies: Optional[List[str]] = ['peanuts']
    medications: Optional[List[str]] = ['inhaler']
    id: UUID = None
    age: int = 30
    gender: str = 'Male'
    emergency_contact: str = 'Jane'
    emergency_phone: str = '123-456-7890'
    medical_info: MedicalInfo = None
    patient_id: UUID = None
    emergency_type: List[str] = None
    location: str = None
    additional_info: Optional[str] = None

inputs = base_inputs()

chat = None

# Route for beginning a conversation
@router.post("/begin_conversation/")
async def begin_conversation():
    try:
        audiofile = 'sample_1.mp3'
        # Save the audio file to a temporary directory
        audiofile_name = f"temp_mp3/{audiofile}"
        # Upload the file to Google Gemini and start a conversation
        myfile = genai.upload_file(audiofile_name)
        prompt_test_data = f"""Imagine you are {inputs.name}'s level-headed AI assistant whose purpose is to carry through a conversation 
        with a 911 dispatcher on behalf of {inputs.name}. We are going to play a game where I am the dispatcher for 911. 
        For each prompt I will prompt you with updates on the current situation, and then in a voice audio file, I will pretend to be the dispatcher. You
        will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

        This is the first prompt, and instead of updating the situation I will give as much context as available to the current
        situation. then, in the audio file will be what the dispatcher says. 

        BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
        ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR!

        For context, {inputs.name} is a {inputs.age} year old {inputs.gender}. Their medical conditions
        include {inputs.medical_conditions}. He is allergic to {inputs.allergies} and for 
        medication he is on {inputs.medications}. We are in need of {inputs.emergency_type}.
        There are gunshots detected in the vacinity. {inputs.name} has a heart rate of 120 bpm and a blood pressure of 130/80. The ADDRESS is
        {inputs.location}. {inputs.name}'s emergency contacts are {inputs.emergency_contact}, {inputs.emergency_phone}.

        

        Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER, ON BEHALF OF {inputs.name}, and 
        whatever is in the AUDIO FILE is what the dispatcher has told you.
        YOU ARE NOT {inputs.name}! YOU ARE HIS AI ASSISTANT!
        
        Respond in Plain, unformatted text.
        """

        chat = model.start_chat(
            history=[{"role": "user", "parts": prompt_test_data}]
        )
        next_prompt_data = f"""The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
        ON BEHALF OF {inputs.name}, and the dispatcher has told you what is in the AUDIO FILE. 
        BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
        ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text."""
        response = chat.send_message([myfile, next_prompt_data])
        text_to_speech(response.text)
        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route for continuing a conversation
@router.post("/continue_conversation/")
async def continue_conversation(audiofile: str):
    try:
        # Save the new audio file to a temporary directory
        audiofile_name = f"temp_mp3/{audiofile}"

        # Retrieve the chat session and continue the conversation
        myfile = genai.upload_file(audiofile_name)  # Assuming you have this method to retrieve a chat
        next_prompt_data = f"""The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
        ON BEHALF OF the user! And the dispatcher has told you what is in the AUDIO FILE. 
        BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
        ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text."""
        response = chat.send_message([myfile, next_prompt_data])
        audio_file_path = text_to_speech(response.text)

        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
