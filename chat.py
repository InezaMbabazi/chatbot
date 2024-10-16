import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Ensure this path is included

# Directly set the OpenAI API key (use with caution)
openai.api_key = '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'

# Function to ensure the required NLTK resources are downloaded
def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.write("Downloading 'punkt' tokenizer...")
        nltk.download('punkt', quiet=True)  # Download quietly
        st.success("Downloaded 'punkt' tokenizer.")
    
    # Check for punkt_tab specifically
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        st.write("Downloading 'punkt_tab' tokenizer...")
        nltk.download('punkt_tab', quiet=True)  # Download quietly
        st.success("Downloaded 'punkt_tab' tokenizer.")

# Download required resources
ensure_nltk_resources()

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
    if 'Questions' not in df.columns:
        st.error("The 'Questions' column is missing in the dataset.")
    else:
        # Process the 'Questions' column
        df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
except FileNotFoundError:
    st.error("Chatbot.csv file not found. Please upload the file.")
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")

# Function to get response from OpenAI
def get_openai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": question}]
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
