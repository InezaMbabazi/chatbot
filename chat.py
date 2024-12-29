import openai
import pandas as pd
import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path to the local .nltk_data directory
nltk.data.path.append('./.nltk_data')

# Function to check if NLTK resources are available
def check_nltk_resources():
    try:
        # Check for the standard punkt tokenizer
        nltk.data.find('tokenizers/punkt')
        st.success("NLTK 'punkt' tokenizer is available.")
    except LookupError:
        st.error("NLTK 'punkt' tokenizer not found. Please ensure it's available in the .nltk_data directory.")

# Call the function to check resources
check_nltk_resources()

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Function to preprocess and tokenize text using nltk
def preprocess_text(text):
    try:
        # Tokenize the text using nltk.tokenize
        tokens = word_tokenize(text.lower())  # Convert to lowercase for better matching
        return tokens
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        return []

# Load Chatbot CSV data
def load_chatbot_data():
    try:
        chatbot_df = pd.read_csv("Chatbot.csv")
        if "Questions" not in chatbot_df.columns or "Answers" not in chatbot_df.columns:
            raise ValueError("CSV must contain 'Questions' and 'Answers' columns.")
        return chatbot_df
    except Exception as e:
        st.error(f"Error loading Chatbot CSV data: {str(e)}")
        return pd.DataFrame()

# Load website content (you can replace this URL with your website's URL)
def fetch_website_content(url):
    try:
        # Send a request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text from the website (you can customize this part)
        paragraphs = soup.find_all('p')
        website_text = " ".join([para.get_text() for para in paragraphs])

        return website_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return ""

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

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Function to handle user input after pressing Enter
def handle_user_input():
    user_input = st.session_state.input_text.strip()  # Get the input text

    if user_input != "":
        # Tokenize the user input
        user_tokens = preprocess_text(user_input)

        # Load the chatbot data
        chatbot_data = load_chatbot_data()

        # Check if the tokens match any questions in the database
        matched_answer = ""
        for _, row in chatbot_data.iterrows():
            question_tokens = preprocess_text(row['Questions'])
            if any(token in question_tokens for token in user_tokens):  # Simple token matching
                matched_answer = row['Answers']
                break

        if matched_answer:
            chatbot_response = matched_answer
        else:
            # If no match found in the database, check the website content
            website_content = fetch_website_content("https://keplercollege.ac.rw/")  # Use your website URL here
            chatbot_response = get_openai_response(user_input, website_content)

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
