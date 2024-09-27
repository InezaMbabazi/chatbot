import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Title of the chatbot app
st.title("Kepler College Chatbot")

# Load or define the bot data
bot_data = {
    'User_Input': [
        # (Your User_Input data here)
    ],
    'Bot_Response': [
        # (Your Bot_Response data here)
    ]
}

bot_df = pd.DataFrame(bot_data)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(bot_df['User_Input'])

# Function to generate a response
def get_response(user_input):
    user_input_tfidf = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_input_tfidf, tfidf_matrix)
    most_similar_index = similarities.argmax()
    return bot_df['Bot_Response'].iloc[most_similar_index]

# User input from Streamlit text input
user_input = st.text_input("Ask a question:")

if user_input:
    response = get_response(user_input)
    st.write("**Bot:**", response)
    st.session_state.chat_history.append(f"You: {user_input}")
    st.session_state.chat_history.append(f"Bot: {response}")

# Display chat history
if 'chat_history' in st.session_state:
    for chat in st.session_state.chat_history:
        st.write(chat)
else:
    st.session_state.chat_history = []
