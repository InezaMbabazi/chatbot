import streamlit as st
import openai
import nltk
import os
import pandas as pd
from nltk.tokenize import word_tokenize

# Set the NLTK data path to the current directory (where your script is)
nltk.data.path.append(os.path.join(os.getcwd(), 'corpora'))
nltk.data.path.append(os.path.join(os.getcwd(), 'tokenizers'))

# Initialize OpenAI API key
openai.api_key = "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"  # Replace with your OpenAI API key

# Load your dataset
df = pd.read_csv("your_dataset.csv")  # Replace with your dataset path

# Preprocess the text data
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize text
    return ' '.join(tokens)

# Apply preprocessing
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Function to get a response from OpenAI's model
def get_chatgpt_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

# Streamlit app layout
st.title("Chatbot with Dataset and OpenAI")
user_question = st.text_input("Ask a question:")

if st.button("Get Answer"):
    if user_question:
        # Check if the question is in the dataset
        processed_question = preprocess_text(user_question)  # Preprocess user question
        if processed_question in df['Processed_Questions'].values:
            answer = df[df['Processed_Questions'] == processed_question]['Answers'].values[0]
        else:
            # If not found, use OpenAI's model
            answer = get_chatgpt_response(user_question)
        
        st.write("Answer:", answer)
    else:
        st.warning("Please enter a question.")

# Additional Streamlit functionalities can go here
