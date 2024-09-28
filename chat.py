import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Data preparation with 30 equal-length messages
data = {
    'Message': [
        "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.",
        "Good morning campus director!! Hope you’re doing pretty fine! I would like to ask you a favor and a guidance, RTB have requested me to go for curriculum review and they have sent an email to the Vc.",
        "Request to release Experts in Hospitality and tourism_0001_0001.pdf • ‎4 pages ‎document omitted",
        "You deleted this message.",
        "Good morning J.P, I’m doing well, I hope you’re doing good too.",
        "I think that will work for you.",
        "I’m doing pretty fine.",
        "Sure and thank you.",
        "Hello.",
        "Yes, JP how are you?",
        "Pretty fine Director… if possible you help me to get that mission order by Morning…",
        "Sure, I was actually working since I thought you want it by tomorrow I kept it on hold.",
        "What’s the District?",
        "Musanze.",
        "Ok.",
        "Confirm the information below: Purpose of the Travel: curriculum review Length of stay: 13 days.",
        "Purpose of the travel: workshop to develop industry based training trainees manuals.",
        "Noted, I’ll send it your email tomorrow in the morning.",
        "And means of transport: ??",
        "All will be covered by RTB.",
        "I mean is it public or private??",
        "Public.",
        "Good afternoon director umeze neza ?? Nageze imusanze neza We’re also trying to clean our data.",
        "Good afternoon JP.",
        "Yego meze neza, glad to arrived safe.",
        "Purpose: workshop to develop industry based training trainees manuel.",
        "Give me few.",
        "Is 7 days?",
        "Can we boost this on social networks with only 200$?",
        "Good morning, kindly give me 30 minutes."
    ],
    'Sender': ['M Prince'] * 30,  # Ensure all 30 messages are from M Prince
    'Receiver': ['K Aline'] * 30  # Ensure all 30 messages are to K Aline
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
