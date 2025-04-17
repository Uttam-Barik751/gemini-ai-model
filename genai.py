import streamlit as st
import google.generativeai as genai

# Set your Gemini API Key
genai.configure(api_key="AIzaSyD1XJtiSMuln2ZdcJtVakXJUZNw0y_fkC4") 

# Load the model (Gemini 1.5 Flash or Pro)
model = genai.GenerativeModel('gemini-1.5-flash') # Or use 'gemini-pro'

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# UI Config
st.set_page_config(page_title="Gemini Chatbot", page_icon=":gem:", layout="centered") # Using :gem: emoji as icon
st.title("JAMES AI Chatbot")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask something...")
if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gemini response
    try:
        response = st.session_state.chat.send_message(user_input)
        answer = response.text
    except Exception as e:
        answer = f"^^ Error: {str(e)}"

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})