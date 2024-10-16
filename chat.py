import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
import streamlit as st

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Adjust this path if necessary

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
    try:
        # Tokenize the text into words
        tokens = word_tokenize(text.lower())
        return tokens
    except LookupError as e:
        st.write(f"Error in tokenizing text: {e}")
        return []

# Load your DataFrame
df = pd.read_csv('Chatbot.csv')

# Process the 'Questions' column
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Chatbot interface
st.title("Chatbot")
user_input = st.text_input("You:")

if user_input:
    # Preprocess user input
    processed_input = preprocess_text(user_input)
    
    # Find the best matching question
    matching_question = df[df['Processed_Questions'].apply(lambda x: set(x) == set(processed_input))]
    
    if not matching_question.empty:
        response = matching_question['Answers'].values[0]
        st.write(f"Chatbot: {response}")
    else:
        st.write("Chatbot: Sorry, I don't have an answer for that.")
