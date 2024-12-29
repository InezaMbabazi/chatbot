import openai
import pandas as pd
import streamlit as st
import os
import requests
from bs4 import BeautifulSoup

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Load the Chatbot CSV data with 'Questions' and 'Answers' columns
try:
    df = pd.read_csv('Chatbot.csv')

    # Check if the required columns exist
    if 'Questions' not in df.columns or 'Answers' not in df.columns:
        raise ValueError("CSV must contain 'Questions' and 'Answers' columns.")

    # Extract the questions and answers into a dictionary
    chatbot_data = dict(zip(df['Questions'], df['Answers']))
    st.success("Chatbot CSV data loaded successfully.")
except Exception as e:
    st.error(f"Error loading Chatbot CSV data: {str(e)}")
    chatbot_data = {}  # Empty dictionary if loading fails

# Function to fetch and parse content from a website
def fetch_website_content(url):
    try:
        # Send a request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text from the website (you can customize this part if needed)
        paragraphs = soup.find_all('p')
        website_text = " ".join([para.get_text() for para in paragraphs])

        return website_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return ""

# Load website content (replace with your website URL)
website_url = "https://keplercollege.ac.rw/"  # Replace with your website URL
website_content = fetch_website_content(website_url)

# Function to get a response from OpenAI API
def get_openai_response(question, context):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"{question}\n\nContext: {context}"}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to get chatbot response
def get_chatbot_response(user_input):
    # First, check if the question exists in the chatbot data (from CSV)
    if user_input in chatbot_data:
        return chatbot_data[user_input]
    
    # If the question is not found in the chatbot data, then use OpenAI to generate a response
    website_response = get_openai_response(user_input, website_content)
    return website_response

# Streamlit UI with header image and instructions
header_image_path = "header.png"  # Ensure this image exists in your working directory
if os.path.exists(header_image_path):
    st.image(header_image_path, use_column_width=True)
else:
    st.warning("Header image not found. Please upload 'header_image.png'.")

# Add chatbot title and instructions
st.title("Kepler College Chatbot")

st.markdown("""
    <div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #2E86C1;">Welcome to Kepler College's AI-Powered Chatbot</h3>
        <p>To interact with this AI assistant, you can:</p>
        <ul style="list-style-type: square;">
            <li>Type a question or message in the input field below and press Enter to submit.</li>
            <li>The chatbot will respond based on the website's content and knowledge base.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Apply custom CSS for layout styling
st.markdown("""
    <style>
    .chatbox {
        border: 2px solid #2196F3;
        padding: 10px;
        height: 200px;
        overflow-y: scroll;
        background-color: #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialize a session state for user input clearing
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""  # Default to empty string

# Function to handle user input after pressing Enter
def handle_user_input():
    user_input = st.session_state.input_text.strip()  # Get the input text

    if user_input != "":
        # Get response from the chatbot or website
        chatbot_response = get_chatbot_response(user_input)

        # Add the conversation to session state
        st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})

        # Clear the input field by resetting the session state correctly
        st.session_state.input_text = ""  # This clears the input field after sending the message

# User input field with the updated functionality for Enter key
user_input = st.text_input("You:", value=st.session_state.input_text, key="input_text", on_change=handle_user_input)

# Display the last 3 conversations with new messages on top
if st.session_state.conversation:
    st.markdown("<h4>Conversation History:</h4>", unsafe_allow_html=True)
    for chat in reversed(st.session_state.conversation[-3:]):
        st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>"
                    f"<strong>You:</strong> {chat['user']}<br>"
                    f"<strong>Chatbot:</strong> {chat['chatbot']}</div>", unsafe_allow_html=True)
