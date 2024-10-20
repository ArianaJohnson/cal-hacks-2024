import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from pydantic import BaseModel, UUID4
from typing import List, Optional
from keys import GEMINI_KEY
from models import *

# Configure the Google Gemini model
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

router = APIRouter()

# Input Pydantic model for request body
class Inputs(BaseModel):
    dispatch_request: DispatchRequest = None
    patient: Patient = None

# Route for beginning a conversation
@router.post("/begin-conversation/")
async def begin_conversation(inputs: Inputs, audiofile: UploadFile = File(...)):
    try:
        # Save the audio file to a temporary directory
        audiofile_name = f"temp_mp3/{audiofile.filename}"
        with open(audiofile_name, "wb") as buffer:
            buffer.write(await audiofile.read())

        # Upload the file to Google Gemini and start a conversation
        myfile = genai.upload_file(audiofile_name)
        prompt_test_data = f"""Imagine you are {inputs.patient.name}'s level-headed AI assistant whose purpose is to carry through a conversation 
        with a 911 dispatcher on behalf of {inputs.patient.name}. We are going to play a game where I am the dispatcher for 911. 
        For each prompt I will prompt you with updates on the current situation, and then in a voice audio file, I will pretend to be the dispatcher. You
        will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

        This is the first prompt, and instead of updating the situation I will give as much context as available to the current
        situation. then, in the audio file will be what the dispatcher says. 

        BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
        ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR!

        For context, {inputs.patient.name} is a {inputs.patient.age} year old {inputs.patient.gender}. Their medical conditions
        include {inputs.patient.medical_info.medical_conditions}. He is allergic to {inputs.patient.medical_info.allergies} and for 
        medication he is on {inputs.patient.medical_info.medications}. We are in need of {inputs.dispatch_request.emergency_type}.
        There are gunshots detected in the vacinity. {inputs.patient.name} has a heart rate of 120 bpm and a blood pressure of 130/80. The ADDRESS is
        {inputs.dispatch_request.location}.

        Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER, ON BEHALF OF {inputs.patient.name}, and 
        whatever is in the AUDIO FILE is what the dispatcher has told you.
        YOU ARE NOT {inputs.patient.name}! YOU ARE HIS AI ASSISTANT!
        
        Respond in Plain, unformatted text.
        """

        chat = model.start_chat(
            history=[{"role": "user", "parts": prompt_test_data}]
        )
        next_prompt_data = f"""The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
        ON BEHALF OF {inputs.patient.name}, and the dispatcher has told you what is in the AUDIO FILE. 
        BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
        ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text."""
        response = chat.send_message([myfile, next_prompt_data])

        return {"response": response.text, "chat_id": id(chat)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route for continuing a conversation
@router.post("/continue-conversation/")
async def continue_conversation(chat_id: str, audiofile: UploadFile = File(...)):
    try:
        # Save the new audio file to a temporary directory
        audiofile_name = f"temp_mp3/{audiofile.filename}"
        with open(audiofile_name, "wb") as buffer:
            buffer.write(await audiofile.read())

        # Retrieve the chat session and continue the conversation
        chat = model.get_chat_by_id(chat_id)  # Assuming you have this method to retrieve a chat
        next_prompt_data = f"""The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
        ON BEHALF OF the user! And the dispatcher has told you what is in the AUDIO FILE. 
        BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
        ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text."""
        myfile = genai.upload_file(audiofile_name)
        response = chat.send_message([myfile, next_prompt_data])

        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
