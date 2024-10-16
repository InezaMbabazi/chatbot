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
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        st.write("Downloading 'punkt_tab' tokenizer...")
        nltk.download('punkt_tab')

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

# Check if 'Questions' column exists
if 'Questions' in df.columns:
    # Process the 'Questions' column
    df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

    # Chatbot interaction
    st.title("Chatbot")
    user_input = st.text_input("You:", "")
    
    if user_input:
        # Preprocess user input
        processed_input = preprocess_text(user_input)
        
        # Simple response logic (this can be enhanced)
        if processed_input in df['Processed_Questions'].tolist():
            response = df[df['Processed_Questions'].apply(lambda x: x == processed_input)]['Response'].values[0]
        else:
            response = "I'm sorry, I don't understand that."

        st.write("Chatbot:", response)
else:
    st.write("The 'Questions' column is not found in the DataFrame.")
