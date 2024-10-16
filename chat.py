import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')

# Directly set the OpenAI API key (use with caution)
openai.api_key = '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'

# Function to ensure the required NLTK resources are downloaded
def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.write("Downloading 'punkt' tokenizer...")
        nltk.download('punkt', quiet=True)  # Download quietly
        st.success("Downloaded 'punkt' tokenizer.")

# Download required resources
ensure_nltk_resources()

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
        # Process the 'Questions' column
        df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
except FileNotFoundError:
    st.error("Chatbot.csv file not found. Please upload the file.")
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")

# Function to get a response from the OpenAI API if needed
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
        # Check if any part of the question contains the keywords from the DataFrame
        if row['Questions'].lower() in user_input.lower():
            return row['Answers']
    return None

# Streamlit chatbot interface
st.title("Kepler Colleger Chatbot")

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    # Preprocess user input
    processed_input = preprocess_text(user_input)

    # Try to get a response from the DataFrame
    response = get_response_from_dataframe(user_input)

    if response:
        # If a match is found in the DataFrame, use the corresponding answer
        chatbot_response = response
    else:
        # If no predefined answer is found, call OpenAI API for broader information
        context = df.to_string(index=False)  # Create a context from the entire DataFrame
        chatbot_response = get_openai_response(user_input, context)

    # Add the conversation to session state
    st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})

    # Keep only the last 3 conversations
    st.session_state.conversation = st.session_state.conversation[-3:]

# Display the last 3 conversations with new messages on top
if st.session_state.conversation:
    for chat in reversed(st.session_state.conversation):  # Reverse the order for newest on top
        st.write(f"You: {chat['user']}")
        st.write(f"Chatbot: {chat['chatbot']}")
