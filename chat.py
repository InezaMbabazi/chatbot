import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st

# Ensure the punkt tokenizer is available
nltk.data.path.append('.nltk_data')

# Load your dataset
df = pd.read_csv('Chatbot.csv')

# Define a preprocessing function
def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text.lower())  
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)

# Preprocess the Questions column
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Streamlit application setup
st.title("Chatbot")
user_input = st.text_input("Ask me anything:")
if user_input:
    st.write("You asked:", user_input)
