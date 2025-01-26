import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Neura Loop",
    page_icon=":brain:",
    layout="wide",  # Adjusted to display wide content
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Add custom 3D styling
st.markdown(
    """
    <style>
        /* Apply 3D styling to the main page */
        body {
            background: linear-gradient(145deg, #e6e6e6, #ffffff);
            font-family: 'Arial', sans-serif;
        }

        /* Style the sidebar */
        .css-1d391kg { /* Sidebar */
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            box-shadow: 4px 4px 8px #bfbfbf, -4px -4px 8px #ffffff;
            border-radius: 15px;
        }

        /* 3D button styling */
        button {
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            border: none;
            border-radius: 15px;
            box-shadow: 4px 4px 8px #bfbfbf, -4px -4px 8px #ffffff;
            color: #000;
            font-size: 16px;
            padding: 10px 20px;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-3px);
        }

        /* 3D container styling */
        .st-container {
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            box-shadow: 4px 4px 8px #bfbfbf, -4px -4px 8px #ffffff;
            border-radius: 15px;
            padding: 20px;
        }

        /* 3D chat bubbles */
        .st-chat-message {
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            border-radius: 15px;
            box-shadow: 4px 4px 8px #bfbfbf, -4px -4px 8px #ffffff;
            padding: 10px;
            margin-bottom: 10px;
        }

        /* Style titles */
        h1, h2, h3, h4, h5 {
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Mode:", ["Chatbot", "HTML Page"])

# Option to display HTML page
if app_mode == "HTML Page":
    # Read your `index.html` file
    def load_html_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    # Load and render the HTML
    html_content = load_html_file("index.html")
    st.components.v1.html(html_content, height=800, scrolling=True)

# Chatbot functionality
else:
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("Ask NeuraLoop Anything...!")

    # Display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message("assistant" if message.role == "model" else "user"):
            st.markdown(message.parts[0].text)

    # User input and AI response
    user_prompt = st.chat_input("Ask NeuraLoop")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
