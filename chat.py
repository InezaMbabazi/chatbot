import streamlit as st
import openai
import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources (only needed the first time you run the app)
nltk.download('punkt')
nltk.download('wordnet')

# Set up OpenAI API Key
openai.api_key = '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'  # Replace with your actual OpenAI API key

# Load the dataset from GitHub
data_url = 'https://github.com/InezaMbabazi/chatbot/blob/main/Chatbot.csv'  # Replace with your actual GitHub URL
df = pd.read_csv(data_url, on_bad_lines='warn', encoding='utf-8')


# Preprocess text
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized)

# Apply preprocessing to questions
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Function to get response from OpenAI (ChatGPT)
def get_chatgpt_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can also use other engines like "gpt-3.5-turbo"
            prompt=user_input,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error with ChatGPT: {e}"

# Fallback function for similarity-based matching
def get_fallback_response(user_input):
    user_input_processed = preprocess_text(user_input)
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform(df['Processed_Questions'].tolist() + [user_input_processed])
    vectors = vectorizer.toarray()

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1]).flatten()
    
    # Get the index of the most similar question
    index = np.argmax(cosine_similarities)
    
    # Return the corresponding answer
    return df['Answers'][index]

# Main chatbot function combining ChatGPT and fallback
def chatbot(user_input):
    response = get_chatgpt_response(user_input)
    
    # If ChatGPT response fails or is unsatisfactory, use fallback method
    if response == "" or "Error" in response:
        response = get_fallback_response(user_input)
    
    return response

# Streamlit UI
st.title("Kepler College Chatbot")

# User input text box
user_input = st.text_input("Ask me anything about Kepler College:")

# Display response when the user submits a query
if user_input:
    response = chatbot(user_input)
    st.write(f"Chatbot: {response}")
