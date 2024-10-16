import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Ensure this path is included

# Set your OpenAI API key securely
openai.api_key = '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'

# Function to ensure the required NLTK resources are downloaded
def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.write("Downloading 'punkt' tokenizer...")
        nltk.download('punkt', quiet=True)  # Download quietly
        st.success("Downloaded 'punkt' tokenizer.")

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
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Chatbot.csv')
        if 'Questions' not in df.columns or 'Answers' not in df.columns:
            st.error("The 'Questions' or 'Answers' column is missing in the dataset.")
            return None
        return df
    except FileNotFoundError:
        st.error("Chatbot.csv file not found. Please upload the file.")
        return None
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None

df = load_data()

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

if user_input and df is not None:
    # Preprocess user input
    processed_input = preprocess_text(user_input)

    # Check for predefined responses in the DataFrame
    response = df[df['Questions'].str.lower() == user_input.lower()]['Answers'].values

    if len(response) > 0:
        response = response[0]  # Get the first matching answer
    else:
        # If no predefined answer is found, call OpenAI API
        response = get_openai_response(user_input)

    st.write(f"Chatbot: {response}")
