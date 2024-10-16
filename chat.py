import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Ensure NLTK data path includes your local .nltk_data folder
nltk.data.path.append('.nltk_data')

# Download stopwords if not already downloaded
nltk.download('stopwords', download_dir='.nltk_data')

# Load the dataset
df = pd.read_csv('Chatbot.csv')

# Define a preprocessing function
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())  
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)

# Preprocess the Questions column
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Streamlit application setup
st.title("Chatbot with NLTK and OpenAI")

# Get user input
user_input = st.text_input("Ask me anything:")

# If the user asks a question
if user_input:
    # Show the user input on the screen
    st.write("You asked:", user_input)
    
    # Preprocess user input
    processed_input = preprocess_text(user_input)
    
    # Generate a response using OpenAI
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"The user asked: {processed_input}\nGenerate a response:",
      max_tokens=150
    )
    
    # Display the response
    st.write("Chatbot's response:", response.choices[0].text.strip())
