import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Append NLTK data path (ensure correct path)
nltk_data_path = os.path.join(os.getcwd(), '.nltk_data')
nltk.data.path.append(nltk_data_path)

# Ensure necessary NLTK resources are downloaded or available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_path)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_path)

# Load the dataset (ensure the CSV is in the same folder as the script)
df = pd.read_csv('Chatbot.csv')

# Define a text preprocessing function
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)

# Preprocess the Questions column
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Streamlit app setup
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
