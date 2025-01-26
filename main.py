import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="NeuraLoop",
    page_icon=":brain:",
    layout="wide",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Apply custom CSS from index.html
def apply_custom_css():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f4f9;
            color: #333;
        }

        .container {
            max-width: 900px;
            margin: auto;
            padding: 20px;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .chat-bubble {
            padding: 15px;
            margin: 10px 0;
            border-radius: 15px;
            display: inline-block;
        }

        .user-bubble {
            background: #007bff;
            color: #fff;
            text-align: right;
            float: right;
        }

        .bot-bubble {
            background: #e9ecef;
            color: #333;
            text-align: left;
            float: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Mode:", ["Index Page", "NeuraLoop"])

# Option to display HTML page
if app_mode == "Index Page":
    st.title("Welcome to NeuraLoop!")
    st.subheader("HTML Page View")
    
    def load_html_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    html_content = load_html_file("index.html")
    st.components.v1.html(html_content, height=800, scrolling=True)

# Chatbot functionality
elif app_mode == "NeuraLoop":
    apply_custom_css()  # Apply custom CSS

    st.title("Ask NeuraLoop Anything...!")
    st.markdown("<div class='container'>", unsafe_allow_html=True)

    # Initialize the chat session
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Display chat history with styled bubbles
    for message in st.session_state.chat_session.history:
        if message.role == "model":
            st.markdown(
                f"<div class='chat-bubble bot-bubble'>{message.parts[0].text}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-bubble user-bubble'>{message.parts[0].text}</div>",
                unsafe_allow_html=True,
            )

    # User input and AI response
    user_prompt = st.chat_input("Ask NeuraLoop")
    if user_prompt:
        st.markdown(
            f"<div class='chat-bubble user-bubble'>{user_prompt}</div>",
            unsafe_allow_html=True,
        )
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        st.markdown(
            f"<div class='chat-bubble bot-bubble'>{gemini_response.text}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
