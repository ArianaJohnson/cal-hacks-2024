import google.generativeai as genai
import os
from keys import GEMINI_KEY
from models import *

key = GEMINI_KEY
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash")

class inputs:
    name: str = None
    phone: str = None
    medical_conditions: List[str] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    id: UUID = None
    name: str = None
    age: int = None
    gender: str = None
    emergency_contact: EmergencyContact = None
    medical_info: MedicalInfo = None
    patient_id: UUID = None
    emergency_type: List[str] = None
    location: str = None
    additional_info: Optional[str] = None

def beginConversation(inputs, audiofile_name):
    
    myfile = genai.upload_file(f"temp_mp3/{audiofile_name}")
    prompt_test_data = f"""
    Imagine you are {inputs.name}'s level-headed AI assistant whose purpose is to carry through a conversation 
    with a 911 dispatcher on behalf of {inputs.name}. We are going to play a game where I am the dispatcher for 911. 
    For each prompt I will prompt you with updates on the current situation, and then in a voice audio file, I will pretend to be the dispatcher. You
    will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

    This is the first prompt, and instead of updating the situation I will give as much context as available to the current
    situation. then, in the audio file will be what the dispatcher says. 

    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR!

    For context, {inputs.name} is a {inputs.age} year old {inputs.gender}. Their medical conditions
    include {inputs.medical_conditions}. He is allergic to {inputs.allergies} and for medication he is on {inputs.medications}. We are in need of {inputs.emergency_type}.
    There are gunshots detected in the vacinity. {inputs.name} has a heart rate of 120 bpm and a blood pressure of 130/80. The ADDRESS is
    {inputs.location}.

    Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER, ON BEHALF OF {inputs.name}, and 
    whatever is in the AUDIO FILE is what the dispatcher has told you.
    YOU ARE NOT {inputs.name}! YOU ARE HIS AI ASSISTANT!
    
    Respond in Plain, unformatted text.
    """

    next_prompt_data = f"""
    The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
    ON BEHALF OF {inputs.name}, and the dispatcher has told you what is in the AUDIO FILE. 
    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text.
    """
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": prompt_test_data},
        ]
        )
    
    response = chat.send_message([myfile, next_prompt_data])
    return response.text, chat

def continueConversation(chat, audiofile_name):
    next_prompt_data = f"""
    The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
    ON BEHALF OF the user! And the dispatcher has told you what is in the AUDIO FILE. 
    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text.
    """
    myfile = genai.upload_file(f"temp_mp3/{audiofile_name}")
    response = chat.send_message([myfile, next_prompt_data])
    return response.text





if __name__ == "__main__":
    test_input = inputs()
    test_input.name = "John"

    response, chat = beginConversation(test_input, "sample_1.mp3")
    print(response)
    print(continueConversation(chat, "sample_2.mp3"))
    print(continueConversation(chat, "sample_3.mp3"))

    # prompt_test_data = f"""
    # Imagine you are {test_input.name}'s level-headed AI assistant whose purpose is to carry through a conversation 
    # with a 911 dispatcher on behalf of {test_input.name}. We are going to play a game where I am the dispatcher for 911. 
    # For each prompt I will prompt you with updates on the current situation, and then in a voice audio file, I will pretend to be the dispatcher. You
    # will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

    # This is the first prompt, and instead of updating the situation I will give as much context as available to the current
    # situation. then, in the audio file will be what the dispatcher says. 

    # BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    # ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR!

    # For context, {test_input.name} is a 31 year old male. His medical conditions
    # include diabetes. He is allergic to peanuts and for medication he is on insulin. We are in need of police and ambulance.
    # There are gunshots detected in the vacinity. {test_input.name} has a heart rate of 120 bpm and a blood pressure of 130/80. The ADDRESS is
    # 63 1st St.

    # Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER, ON BEHALF OF {test_input.name}, and 
    # whatever is in the AUDIO FILE is what the dispatcher has told you.
    # YOU ARE NOT {test_input.name}! YOU ARE HIS AI ASSISTANT!
    
    # Respond in Plain, unformatted text.
    # """

    # next_prompt_data = f"""
    # The situation has updated. There are no changes in the situation. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
    # ON BEHALF OF {test_input.name}, and the dispatcher has told you what is in the AUDIO FILE. 
    # BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    # ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text.
    # """
    # # Configure all the stuff
    # genai.configure(api_key=key)
    # model = genai.GenerativeModel("gemini-1.5-flash")

    # #Requests
    # myfile = genai.upload_file("temp_mp3/sample.mp3")
    # #print(f"{myfile=}")

    # # result = model.generate_content([myfile, "Describe this audio clip"])
    # # print(f"{result.text=}")
    # chat = model.start_chat(
    # history=[
    #     {"role": "user", "parts": prompt_test_data},
    # ]
    # )
    # response = chat.send_message([myfile, next_prompt_data])
    # print(response.text)

    # while 1:
    #     response = chat.send_message([myfile, next_prompt_data])
    #     print(response.text)