import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# Configure Gemini API Key
genai.configure(api_key="IzaSyD1XJtiSMuln2ZdcJtVakXJUZNw0y_fkC4")

# Load the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Gemini Chatbot with PDF", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot with PDF Training")

# PDF upload
uploaded_pdf = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_pdf is not None:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pdf_text = ""
    for page in doc:
        pdf_text += page.get_text()

    st.write("First 1000 characters of the PDF:")
    st.write(pdf_text[:1000])
    st.session_state.pdf_text = pdf_text

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question related to the PDF...")

if user_input and "pdf_text" in st.session_state:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Use PDF context for response
    pdf_context = st.session_state.pdf_text[:2000]
    input_text = f"{pdf_context}\n\nUser query: {user_input}"

    try:
        response = st.session_state.chat.send_message(input_text)
        answer = response.text
    except Exception as e:
        answer = "⚠ Sorry, something went wrong. Please try again later."
        st.error(f"Technical details: {e}")

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content":answer})