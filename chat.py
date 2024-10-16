import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import openai
import random

# Load your dataset
data_path = 'Chatbot.csv'  # Use the relative path to your CSV file
df = pd.read_csv(data_path)

# Ensure you have downloaded the required NLTK data files
# nltk.download('punkt')
# nltk.download('wordnet')

# Initialize OpenAI API key
openai.api_key = "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"  # Replace with your OpenAI API key

# Process text function
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize text
    return tokens

# Preprocess the questions
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Function to get a response from ChatGPT
def get_chatgpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or another model if preferred
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

# Function to find the best match
def find_best_match(user_input):
    user_tokens = preprocess_text(user_input)
    for index, row in df.iterrows():
        question_tokens = row['Processed_Questions']
        # Simple matching logic (you can improve this)
        if any(token in question_tokens for token in user_tokens):
            return row['Answers']  # Return the corresponding answer
    return None  # If no match found

# Streamlit interface
import streamlit as st

st.title("Chatbot")
st.write("Ask me anything!")

user_input = st.text_input("Your question:")

if st.button("Submit"):
    if user_input:
        # Try to find an answer in the dataset
        answer = find_best_match(user_input)
        if answer:
            st.write(f"Bot: {answer}")
        else:
            # If no answer found, fallback to ChatGPT
            st.write("Bot: I don't have an answer for that. Let me check with ChatGPT.")
            chatgpt_answer = get_chatgpt_response(user_input)
            st.write(f"ChatGPT: {chatgpt_answer}")
    else:
        st.write("Please enter a question.")

