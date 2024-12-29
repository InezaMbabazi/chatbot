import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import requests
import os

# Set the NLTK data path to the local .nltk_data directory
nltk.data.path.append('./.nltk_data')

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Function to preprocess text
def preprocess_text(text):
    try:
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

# Function to scrape website content
def fetch_website_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract and return the main text content of the website
            return soup.get_text()
        else:
            return f"Failed to fetch website content. HTTP Status Code: {response.status_code}"
    except Exception as e:
        return f"Error fetching website content: {str(e)}"

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

# Function to combine responses from multiple sources
def get_combined_response(user_input):
    # Try to find a response in the dataset
    response = get_response_from_dataframe(user_input)
    
    if response:
        return response
    else:
        # If no match, fetch website content
        website_url = "https://keplercollege.ac.rw/"
        website_content = fetch_website_content(website_url)
        
        # Use OpenAI to process user input with website context
        context = f"Website Content: {website_content[:2000]}"  # Limit context length to 2000 characters
        chatbot_response = get_openai_response(user_input, context)
        return chatbot_response

# Streamlit UI
st.title("Kepler College Chatbot")

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User input with a unique key for session state
user_input = st.text_input("You:", key="user_input")

if user_input:
    # Process user input and generate a response
    chatbot_response = get_combined_response(user_input)
    
    # Add the conversation to session state
    st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})
    
    # Clear the input field
    st.session_state.user_input = ""  # Reset the input field

# Display the last 3 conversations with a scrolling chatbox style
if st.session_state.conversation:
    st.markdown("<h4>Conversation History:</h4>", unsafe_allow_html=True)
    for chat in reversed(st.session_state.conversation[-3:]):
        st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>"
                    f"<strong>You:</strong> {chat['user']}<br>"
                    f"<strong>Chatbot:</strong> {chat['chatbot']}</div>", unsafe_allow_html=True)
