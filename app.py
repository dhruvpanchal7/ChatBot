from dotenv import load_dotenv 
load_dotenv() 
import streamlit as st 
import os 
from PIL import Image 
import google.generativeai as genai  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])  

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(layout="wide") 
st.header("Gemini Chatbot")   

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Enter your question here:", key="input")
submit_button = st.button("Submit")  

if submit_button and input_text:
    response = get_gemini_response(input_text)
    
    # Combine the text from all chunks into a single string
    gemini_response_text = ' '.join([chunk.text for chunk in response])
    
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is:")
    
    # Display the entire Gemini response as a single text
    st.write(gemini_response_text)
    
    st.session_state['chat_history'].append(("Gemini", gemini_response_text))

st.subheader("The Chat History is:")  

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
