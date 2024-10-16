import streamlit as st
import openai
import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')

# Set up OpenAI API Key
openai.api_key = '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'  # Replace with your actual OpenAI API key

# Sample dataset for fallback responses
data = {
    "Questions": [
        "What kind of degrees does Kepler offer?",
        "Is Kepler College accredited by HEC?",
        # (other questions as before)
    ],
    "Answers": [
        "Kepler College offers bachelor's programs in Project Management and Business Analytics, focusing on practical, industry-relevant education.",
        "Yes, Kepler College is accredited by the Higher Education Council (HEC) of Rwanda.",
        # (other answers as before)
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Preprocess text using lemmatization and tokenization
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize text
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]  # Lemmatize tokens
    return ' '.join(lemmatized)

# Apply preprocessing to questions
df['Processed_Questions'] = df['Questions'].apply(preprocess_text)

# Function to get response from OpenAI (ChatGPT)
def get_chatgpt_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can also use "gpt-3.5-turbo"
            prompt=user_input,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error with ChatGPT: {e}"

# Fallback function for similarity-based matching using cosine similarity
def get_fallback_response(user_input):
    user_input_processed = preprocess_text(user_input)  # Preprocess user input
    
    # Create TF-IDF vectors including the user input
    vectorizer = TfidfVectorizer().fit_transform(df['Processed_Questions'].tolist() + [user_input_processed])
    vectors = vectorizer.toarray()

    # Calculate cosine similarity between the user input and all questions
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1]).flatten()
    
    # Get the index of the most similar question
    index = np.argmax(cosine_similarities)
    
    # Return the corresponding answer
    return df['Answers'][index]

# Main chatbot function combining ChatGPT and fallback method
def chatbot(user_input):
    response = get_chatgpt_response(user_input)
    
    # If ChatGPT response fails or is unsatisfactory, use fallback method
    if response == "" or "Error" in response:
        response = get_fallback_response(user_input)
    
    return response

# Streamlit UI for the chatbot
st.title("Kepler College Chatbot")

# Input text box for user to ask a question
user_input = st.text_input("Ask me anything about Kepler College:")

# Display chatbot response when user submits a query
if user_input:
    response = chatbot(user_input)
    st.write(f"Chatbot: {response}")
