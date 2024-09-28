import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Sample data
data = {
    'Date': ['20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022'],
    'Time': ['09:09:06', '09:09:06', '09:09:43', '09:10:34', '09:27:41'],
    'Sender': ['K Aline', 'M Prince', 'M Prince', 'M Prince', 'K Aline'],
    'Receiver': ['M Prince', 'K Aline', 'K Aline', 'K Aline', 'M Prince'],
    'Message': [
        "Messages and calls are end-to-end encrypted.",
        "Good morning campus director!! Hope you’re doing pretty fine!",
        "Request to release Experts in Hospitality and tourism_0001_0001.pdf.",
        "You deleted this message.",
        "Good morning J.P, I’m doing well, I hope you’re doing good too."
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Prepare data for modeling
X = df['Message']  # Features
y = df['Sender']  # Target labels
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X, y)

# Streamlit app
st.title("Chatbot Interface")

# Chat input
user_input = st.text_input("You: ", "")

if user_input:
    # Predict the sender based on the user input
    prediction = model.predict([user_input])
    st.write(f"Chatbot: {prediction[0]}")

# Add previous messages if needed
