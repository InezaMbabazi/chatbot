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

# Load CSV dataset (Chatbot.csv)
def load_chatbot_csv():
    try:
        # Load the CSV file from the same directory as chatbot.py
        chatbot_data = pd.read_csv(os.path.join(os.getcwd(), 'Chatbot.csv'))  # Load CSV from the current working directory
        if 'Questions' in chatbot_data.columns and 'Answers' in chatbot_data.columns:
            return chatbot_data
        else:
            st.error("Chatbot.csv must contain 'Questions' and 'Answers' columns.")
            return None
    except FileNotFoundError:
        st.error("Chatbot.csv file not found in the current directory. Please upload the file.")
        return None

# Load chatbot CSV data
chatbot_data = load_chatbot_csv()

# Function to preprocess text
def preprocess_text(text):
    try:
        # Use only the standard punkt tokenizer
        tokens = word_tokenize(text.lower())
        return tokens
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        return []

# Function to fetch and parse content from a website
def fetch_website_content(url):
    try:
        # Send a request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text from the website
        # You can customize this part to extract specific content such as paragraphs, headings, etc.
        paragraphs = soup.find_all('p')
        website_text = " ".join([para.get_text() for para in paragraphs])

        return website_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return ""

# Load website content (you can replace this URL with your website's URL)
website_url = "https://keplercollege.ac.rw/"  # Replace with your website URL
website_content = fetch_website_content(website_url)

# Function to get a response from OpenAI API
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

# Function to get the most relevant answer from the CSV data
def get_answer_from_csv(user_question):
    if chatbot_data is not None:
        # Preprocess the user question
        user_question_tokens = preprocess_text(user_question)
        
        # Find the best matching question in the CSV based on token overlap
        best_match = None
        highest_overlap = 0
        
        for index, row in chatbot_data.iterrows():
            question_tokens = preprocess_text(row['Questions'])
            overlap = len(set(user_question_tokens).intersection(set(question_tokens)))
            if overlap > highest_overlap:
                highest_overlap = overlap
                best_match = row['Answers']
        
        # Return the answer if a match is found
        if best_match:
            return best_match
        else:
            return "Sorry, I couldn't find an answer to your question in the database."
    return "Error loading chatbot data."

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
        # Get response from the chatbot CSV data
        chatbot_response = get_answer_from_csv(user_input)
        
        # If no answer found in the CSV, use OpenAI to generate a response based on website content
        if chatbot_response == "Sorry, I couldn't find an answer to your question in the database.":
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
