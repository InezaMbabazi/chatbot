import openai
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
import streamlit as st
import os  # Import the os module to access environment variables

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Adjust this path if necessary

# Set your OpenAI API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Access the secret

# Function to ensure the required NLTK resources are downloaded
def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.write("Downloading 'punkt' tokenizer...")
        nltk.download('punkt')

# Download required resources
ensure_nltk_resources()

# Function to preprocess text
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    return tokens

# Load your DataFrame
df = pd.read_csv('Chatbot.csv')

# Check if 'Questions' column exists
if 'Questions' in df.columns:
    # Process the 'Questions' column
    df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Function to get response from OpenAI
def get_openai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # or whichever model you want to use
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit chatbot interface
st.title("Chatbot")
user_input = st.text_input("You:", "")

if user_input:
    # Preprocess user input
    processed_input = preprocess_text(user_input)

    # Check for predefined responses
    response = df[df['Processed_Questions'].apply(lambda x: x == processed_input)]['Answers'].values
    if len(response) > 0:
        response = response[0]
    else:
        # If no predefined answer is found, call OpenAI API
        response = get_openai_response(user_input)

    st.write(f"Chatbot: {response}")
