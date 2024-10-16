import streamlit as st
import openai
import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources (only needed the first time you run the app)
nltk.download('wordnet')

# Set up OpenAI API Key
openai.api_key = 'YOUR_API_KEY'  # Replace with your actual OpenAI API key

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

# Preprocess text
lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')  # Tokenizes based on word characters

def preprocess_text(text):
    tokens = tokenizer.tokenize(text.lower())  # Tokenize text
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
