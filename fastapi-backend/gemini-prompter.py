import google.generativeai as genai
import os
from keys import gemini_key
from models import *

# class inputs():
#     emergency_contact: EmergencyContact
#     medical_info: MedicalInfo
#     patient: Patient
#     dispatch_request: DispatchRequest



if __name__ == "__main__":
    prompt_test_data = """
    Imagine you are a level-headed AI assistant whose purpose is to carry through a conversation 
    with a 911 dispatcher on behalf of James. We are going to play a game where I am the dispatcher for 911. 
    For each prompt I will prompt you with updates on the current situation, and then in square brackets I will pretend to be the dispatcher. You
    will respond as if you are in a conversation with this dispatcher and be helpful and answer their questions.

    This is the first prompt, and instead of updating the situation I will give as much context as available to the current
    situation. then, in square brackets will be what the dispatcher says. 

    For context, James is a 31 year old male. His medical conditions
    include diabetes. He is allergic to peanuts and for medication he is on insulin. We are in need of police and ambulance.
    There are gunshots detected in the vacinity. James has a heart rate of 120 bpm and a blood pressure of 130/80. 

    [911, what is your emergency?]
    """
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print(response.text)
    while true:
        response = model.generate_content(input())
        print(response.text)