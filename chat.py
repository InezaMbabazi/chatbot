import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Data preparation
data = {
    'Message': [
        "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.",
        "Good morning campus director!! Hope you’re doing pretty fine! I would like to ask you a favor and a guidance...",
        "Good morning J.P, I’m doing well, I hope you’re doing good too. It’s fine I’ll have your mission order ready and send it to your email.",
        "Hello.",
        "Yes, JP how are you?",
        "Pretty fine Director… if possible you help me to get that mission order by Morning… to comply with RTB request.",
        "Confirm the information below: Purpose of the Travel: curriculum review Length of stay: 13 days Mission fees to be covered by RTB.",
        "Purpose of the travel: workshop to develop industry based training trainees manuals.",
        "Good afternoon director umeze neza ?? Nageze imusanze neza We’re also trying to clean our data...",
        "Good morning.",
        "Good morning.",
        "Can we boost this on social networks with only 200$ we can make noises around…. It’s a great content.",
        "Good morning, kindly give me 30 minutes.",
        "JP Amakuru ??",
        "Good evening Director."
    ],
    'Sender': ['M Prince'] * 15,
    'Receiver': ['K Aline'] * 15
}

# Creating the DataFrame
df = pd.DataFrame(data)

# Model training
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(df['Message'], df['Message'])  # Using Message as both features and labels for simplicity

# Streamlit app
st.title("Chatbot")
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        prediction = model.predict([user_input])[0]
        st.write(f"K Aline: {prediction}")
    else:
        st.write("Please enter a message.")
