import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Neura Loop",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",    # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Optionally render the index.html file
def render_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.markdown(html_content, unsafe_allow_html=True)

# Sidebar for switching between the chatbot and index.html
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Mode:", ["Chatbot", "HTML Page"])

if app_mode == "HTML Page":
    # Render the index.html content
    render_html_file("index.html")
else:
    # Chatbot functionality
    st.title("Ask NeuraLoop Anything...!")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask NeuraLoop")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

