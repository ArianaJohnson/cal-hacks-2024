import google.generativeai as genai
import os
from keys import GEMINI_KEY
from models import *

key = GEMINI_KEY

class inputs:
    def __init__(self, ):
        emergency_contact: EmergencyContact
        medical_info: MedicalInfo
        patient: Patient
        dispatch_request: DispatchRequest

def beginConversation(inputs):
    prompt_test_data = """
    Imagine you are {inputs.patient.name}'s level-headed AI assistant whose purpose is to carry through a conversation 
    with a 911 dispatcher on behalf of {inputs.patient.name}. We are going to play a game where I am the dispatcher for 911. 
    For each prompt I will prompt you with updates on the current situation, and then in square brackets I will pretend to be the dispatcher. You
    will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

    This is the first prompt, and instead of updating the situation I will give as much context as available to the current
    situation. then, in square brackets will be what the dispatcher says. 

    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR!

    For context, {inputs.patient.name} is a 31 year old male. His medical conditions
    include diabetes. He is allergic to peanuts and for medication he is on insulin. We are in need of police and ambulance.
    There are gunshots detected in the vacinity. {inputs.patient.name} has a heart rate of 120 bpm and a blood pressure of 130/80. The ADDRESS is
    63 1st St.

    Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER, ON BEHALF OF {inputs.patient.name}, and the dispatcher has told 
    you what is in the SQUARE BRACKETS. YOU ARE NOT {inputs.patient.name}! YOU ARE HIS AI ASSISTANT!
    
    Respond in Plain, unformatted text.
    """

    next_prompt_data_1 = """
    The situation has updated. There are no changes in the situation. []
    """
    next_prompt_data_2 = """
    ]. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
    ON BEHALF OF {inputs.patient.name}, and the dispatcher has told you what is in the SQUARE BRACKETS. 
    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text.
    """


    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
    history=[
        {"role": "user", "parts": prompt_test_data},
    ]
)
    response = chat.send_message(next_prompt_data_1 + "[911, what is your emergency?]" + next_prompt_data_2)
    print(response.text)

    while 1:
        response = chat.send_message(next_prompt_data_1 + input() + next_prompt_data_2)
        print(response.text)







if __name__ == "__main__":
    test_input = inputs()
    test_input.patient.name = "Jack"
    prompt_test_data = """
    Imagine you are {test_input.patient.name}'s level-headed AI assistant whose purpose is to carry through a conversation 
    with a 911 dispatcher on behalf of {test_input.patient.name}. We are going to play a game where I am the dispatcher for 911. 
    For each prompt I will prompt you with updates on the current situation, and then in square brackets I will pretend to be the dispatcher. You
    will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

    This is the first prompt, and instead of updating the situation I will give as much context as available to the current
    situation. then, in square brackets will be what the dispatcher says. 

    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR!

    For context, {test_input.patient.name} is a 31 year old male. His medical conditions
    include diabetes. He is allergic to peanuts and for medication he is on insulin. We are in need of police and ambulance.
    There are gunshots detected in the vacinity. {test_input.patient.name} has a heart rate of 120 bpm and a blood pressure of 130/80. The ADDRESS is
    63 1st St.

    Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER, ON BEHALF OF {test_input.patient.name}, and the dispatcher has told 
    you what is in the SQUARE BRACKETS. YOU ARE NOT {test_input.patient.name}! YOU ARE HIS AI ASSISTANT!
    
    Respond in Plain, unformatted text.
    """

    next_prompt_data_1 = """
    The situation has updated. There are no changes in the situation. []
    """
    next_prompt_data_2 = """
    ]. Remember, respond AS IF YOU ARE an assistant having a CONVERSATION with the DISPATCHER,
    ON BEHALF OF {inputs.patient.name}, and the dispatcher has told you what is in the SQUARE BRACKETS. 
    BE PASSIVE! Do NOT overload with information the DISPATCHER DOES NOT REQUEST! Answer WHAT THE DISPATCHER
    ASKS FOR! DO NOT GIVE INFORMATION THAT THEY DON'T ASK FOR! Respond in Plain, unformatted text.
    """


    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
    history=[
        {"role": "user", "parts": prompt_test_data},
    ]
)
    response = chat.send_message(next_prompt_data_1 + "[911, what is your emergency?]" + next_prompt_data_2)
    print(response.text)

    while 1:
        response = chat.send_message(next_prompt_data_1 + input() + next_prompt_data_2)
        print(response.text)