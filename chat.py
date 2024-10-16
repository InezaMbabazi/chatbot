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
    if 'Questions' not in df.columns or 'Answers' not in df.columns:
        st.error("The 'Questions' or 'Answers' column is missing in the dataset.")
    else:
        # Process the 'Questions' column
        df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
except FileNotFoundError:
    st.error("Chatbot.csv file not found. Please upload the file.")
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")

# Function to get a response from the OpenAI API if needed
def get_openai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": question}]
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

# Streamlit chatbot interface
st.title("Chatbot")
user_input = st.text_input("You:", "")

if user_input:
    # Preprocess user input
    processed_input = preprocess_text(user_input)

    # Try to get a response from the DataFrame
    response = get_response_from_dataframe(user_input)
    
    if response:
        # If a match is found in the DataFrame, use the corresponding answer
        st.write(f"Chatbot: {response}")
    else:
        # If no predefined answer is found, call OpenAI API for broader information
        response = get_openai_response(user_input)
        st.write(f"Chatbot: {response}")
