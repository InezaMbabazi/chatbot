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
def scrape_website_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Customize the following to extract relevant content
            content = soup.get_text()
            return content
        else:
            st.error(f"Failed to fetch website data: Status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error scraping website: {str(e)}")
        return None

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

# Streamlit UI
st.title("Kepler College Chatbot")

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    # Try scraping website content
    website_content = scrape_website_content("https://keplercollege.ac.rw/")
    response_from_website = None
    if website_content and user_input.lower() in website_content.lower():
        response_from_website = "Found relevant information on the website. Please visit for detailed information."

    # Try to get a response from the DataFrame
    response_from_dataframe = get_response_from_dataframe(user_input)

    # Use OpenAI API if no match in website or DataFrame
    if response_from_website:
        chatbot_response = response_from_website
    elif response_from_dataframe:
        chatbot_response = response_from_dataframe
    else:
        context = df.to_string(index=False)  # Create a context from the entire DataFrame
        chatbot_response = get_openai_response(user_input, context)

    # Add the conversation to session state
    st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})

# Display conversation history
if st.session_state.conversation:
    for chat in reversed(st.session_state.conversation):
        st.markdown(f"**You:** {chat['user']}  \n**Chatbot:** {chat['chatbot']}")
