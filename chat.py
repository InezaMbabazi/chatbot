import streamlit as st
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Set up the NLTK data directory
nltk.data.path.append('.nltk_data')

# Load the CSV file into a DataFrame
df = pd.read_csv('Chatbot.csv')

# Preprocess text
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize text
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]  # Lemmatize
    return ' '.join(lemmatized_tokens)

# Process the questions
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Define a function to get responses
def get_response(user_input):
    # Simple logic to find the closest matching question
    for index, row in df.iterrows():
        if user_input in row['Processed_Questions']:
            return row['Answers']
    return "I'm sorry, I don't understand that."

# Streamlit app
st.title("Chatbot")
user_input = st.text_input("You:")
if st.button("Send"):
    response = get_response(preprocess_text(user_input))
    st.write(f"Bot: {response}")
