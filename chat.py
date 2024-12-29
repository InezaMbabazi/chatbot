import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
import os
import requests
from requests.exceptions import RequestException, Timeout
from bs4 import BeautifulSoup

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

# Function to preprocess text
def preprocess_text(text):
    try:
        # Use only the standard punkt tokenizer
        tokens = word_tokenize(text.lower())
        return tokens
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        return []

# Load your DataFrame
try:
    df = pd.read_csv('Chatbot.csv')
    if 'Questions' not in df.columns or 'Answers' not in df.columns:
        st.error("The 'Questions' or 'Answers' column is missing in the dataset.")
    else:
        df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
except FileNotFoundError:
    st.error("Chatbot.csv file not found. Please upload the file.")
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")

# Function to fetch and parse content from a website
def fetch_website_content(url):
    try:
        # Set a timeout for the request (e.g., 5 seconds)
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check if the request was successful (200 OK)
        
        # Parse the website content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all text from the website
        paragraphs = soup.find_all('p')  # Get all paragraph tags
        website_text = " ".join([para.get_text() for para in paragraphs])

        return website_text
    except Timeout:
        st.error(f"The request to {url} timed out. Please check the server status.")
        return ""
    except RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return ""

# Use the updated URL
website_url = "https://keplercollege.ac.rw/"

# Function to get a response from the OpenAI API
def get_openai_response(question, context):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{question}\n\nContext: {context}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to check if the user's question matches any in the DataFrame
def get_response_from_dataframe(user_input):
    for index, row in df.iterrows():
        if row['Questions'].lower() in user_input.lower():
            return row['Answers']
    return None

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
            <li>Type a question or message in the input field below and press Enter.</li>
            <li>If your question matches one in the database, you'll receive the predefined answer.</li>
            <li>If the question is not found, the assistant will fetch relevant information from the website.</li>
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

# Initialize a session state for user input
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""  # Default to empty string

# User input with a unique key for session state
user_input = st.text_input("You:", value=st.session_state.input_text, key="input_text")

# Handle input submission by detecting the user pressing Enter (value change)
if user_input.strip() != "":
    # Try to get a response from the DataFrame
    response = get_response_from_dataframe(user_input)

    if response:
        chatbot_response = response
    else:
        # Fetch website content if no match in the database
        website_content = fetch_website_content(website_url)
        if website_content:
            chatbot_response = get_openai_response(user_input, website_content)
        else:
            chatbot_response = "I couldn't find an answer from the website, please try again later."

    # Add the conversation to session state
    st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})

    # Clear input field after response has been added
    st.session_state.input_text = ""  # Clear input field after response

# Display the last 3 conversations with new messages on top
if st.session_state.conversation:
    st.markdown("<h4>Conversation History:</h4>", unsafe_allow_html=True)
    for chat in reversed(st.session_state.conversation[-3:]):
        st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>"
                    f"<strong>You:</strong> {chat['user']}<br>"
                    f"<strong>Chatbot:</strong> {chat['chatbot']}</div>", unsafe_allow_html=True)
