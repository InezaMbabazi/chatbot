import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
import openai
import streamlit as st

# Set the path for NLTK data
nltk.data.path.append('./nltk_data')

# Load the dataset
data_path = 'Chatbot.csv'
df = pd.read_csv(data_path)

# Preprocessing function
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize text
    return tokens

# Process the questions in the dataset
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Set up the OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to generate responses
def generate_response(user_input):
    # Check if user input matches a question in the dataset
    for index, row in df.iterrows():
        if user_input.lower() in row['Processed_Questions']:
            return row['Answers']
    # If not found in dataset, use ChatGPT to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit UI
st.title("Chatbot")
user_input = st.text_input("Ask a question:")
if st.button("Send"):
    if user_input:
        response = generate_response(user_input)
        st.write(response)
    else:
        st.write("Please enter a question.")
