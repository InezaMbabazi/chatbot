import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path to include your local data
nltk.data.path.append('./.nltk_data')  # Ensure this matches your directory structure

# Function to check if 'punkt' is available locally
def check_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.error("NLTK punkt tokenizer not found locally. Please ensure it is included in your project.")

# Call the function to check resources
check_nltk_resources()

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Function to preprocess text
def preprocess_text(text):
    try:
        tokens = word_tokenize(text.lower())
        return tokens
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        return []

# Load your DataFrame
try:
    df = pd.read_csv('Chatbot.csv')
    if 'Questions' not in df.columns or 'Answers' not in df.columns:
        st.error("The 'Questions' or 'Answers' column is missing in the dataset.")
    else:
        df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
except FileNotFoundError:
    st.error("Chatbot.csv file not found. Please upload the file.")
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")

# Function to get a response from the OpenAI API
def get_openai_response(question, context):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{question}\n\nContext: {context}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to check if the user's question matches any in the DataFrame
def get_response_from_dataframe(user_input):
    for index, row in df.iterrows():
        if row['Questions'].lower() in user_input.lower():
            return row['Answers']
    return None

# Streamlit chatbot interface
st.title("Kepler College Chatbot")

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    processed_input = preprocess_text(user_input)

    # Try to get a response from the DataFrame
    response = get_response_from_dataframe(user_input)

    if response:
        chatbot_response = response
    else:
        context = df.to_string(index=False)  # Create a context from the entire DataFrame
        chatbot_response = get_openai_response(user_input, context)

    # Add the conversation to session state
    st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})

    # Keep only the last 3 conversations
    st.session_state.conversation = st.session_state.conversation[-3:]

# Display the last 3 conversations with new messages on top
if st.session_state.conversation:
    for chat in reversed(st.session_state.conversation):
        st.write(f"You: {chat['user']}")
        st.write(f"Chatbot: {chat['chatbot']}")
