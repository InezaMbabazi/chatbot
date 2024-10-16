import openai
import pandas as pd
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Ensure this path is included

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

# Function to get user feedback
def collect_feedback(response):
    feedback = st.radio("Was this answer helpful?", ("Yes", "No"))
    if feedback == "Yes":
        st.success("Thank you for your feedback!")
    else:
        st.error("Sorry to hear that. We'll strive to improve!")

# Streamlit chatbot interface
st.title("Interactive Chatbot")
user_input = st.text_input("You:", "")

if user_input:
    # Preprocess user input
    processed_input = preprocess_text(user_input)

    # Try to get a response from the DataFrame
    response = get_response_from_dataframe(user_input)

    if response:
        # If a match is found in the DataFrame, use the corresponding answer
        st.write(f"Chatbot: {response}")
        
        # Ask if the user would like to know more about the topic
        follow_up = st.radio("Would you like to know more about this topic?", ("Yes", "No"))
        if follow_up == "Yes":
            st.write("Please specify what else you would like to know!")
    
        # Collect feedback
        collect_feedback(response)
    else:
        # If no predefined answer is found, call OpenAI API for broader information
        # Additionally, provide context from the DataFrame
        context = df.to_string(index=False)  # Create a context from the entire DataFrame
        response = get_openai_response(user_input, context)
        st.write(f"Chatbot: {response}")
        
        # Ask if the user would like to know more about the topic
        follow_up = st.radio("Would you like to ask something else?", ("Yes", "No"))
        if follow_up == "Yes":
            st.write("Please ask your question!")
    
        # Collect feedback
        collect_feedback(response)
