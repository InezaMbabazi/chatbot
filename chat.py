import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
import streamlit as st

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Ensure this path is correct

# Function to ensure the required NLTK resources are downloaded
def ensure_nltk_resources():
    resources = ['punkt', 'punkt_tab']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            st.write(f"Downloading '{resource}' tokenizer...")
            nltk.download(resource)

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

# Set the title of the app
st.title("Chatbot Questions Processing")

# Load your DataFrame
try:
    df = pd.read_csv('Chatbot.csv')
except FileNotFoundError:
    st.write("Error: 'Chatbot.csv' file not found.")
    st.stop()

# Check if 'Questions' column exists
if 'Questions' in df.columns:
    # Process the 'Questions' column
    df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

    # Display the original and processed questions with a section header
    st.subheader("Original and Processed Questions:")
    st.dataframe(df[['Questions', 'Processed_Questions']].head())
else:
    st.write("The 'Questions' column is not found in the DataFrame.")
