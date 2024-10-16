import openai
import pandas as pd
import streamlit as st
import os

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('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')  # Make sure to set this in your environment

# Load your DataFrame
df = pd.read_csv('Chatbot.csv')

# Function to get response from OpenAI
def get_openai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": question}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit chatbot interface
st.title("Chatbot")
user_input = st.text_input("You:", "")

if user_input:
    # Check for predefined responses in the DataFrame
    response = df[df['Questions'].str.contains(user_input, case=False, na=False)]['Answers'].values
    if len(response) > 0:
        response = response[0]
    else:
        # If no predefined answer is found, call OpenAI API
        response = get_openai_response(user_input)

    st.write(f"Chatbot: {response}")
