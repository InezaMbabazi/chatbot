import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Data preparation with 30 equal-length messages
data = {
    'Message': [
        "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.",
        "Good morning campus director!! Hope you’re doing pretty fine! I would like to ask you a favor and a guidance, RTB have requested me to go for curriculum review and they have sent an email to the Vc, I was supposed to go in this week but with this activity we’re having now I told them I’ll come in this upcoming Sunday until 4th November, but they have requested me to send my mission order which will start on 23 to 4th November for the preparation of accommodation and etc… and the problem I’ll come back to Kigali tomorrow evening when your office and the office of Vc will be closed … I was asking my self if I can get a support from you or an advise how I can get that mission order. Thank you",
        "Request to release Experts in Hospitality and tourism_0001_0001.pdf • ‎4 pages ‎document omitted",
        "You deleted this message.",
        "Good morning J.P, I’m doing well, I hope you’re doing good too. It’s fine I’ll have your mission order ready and send it to your email.",
        "I think that will work for you.",
        "I’m doing pretty fine.",
        "Sure and thank you.",
        "Hello.",
        "Yes, JP how are you?",
        "Pretty fine Director… if possible you help me to get that mission order by Morning… to comply with RTB request.",
        "Sure, I was actually working since I thought you want it by tomorrow I kept it on hold.",
        "What’s the District?",
        "Ooooh! I understand.",
        "Musanze.",
        "Ok.",
        "Confirm the information below: Purpose of the Travel: curriculum review Length of stay: 13 days Mission fees to be covered by RTB.",
        "Purpose of the travel: workshop to develop industry based training trainees manuals.",
        "Ibindi ni byo.",
        "Noted, I’ll send it your email tomorrow in the morning.",
        "And means of transport: ??",
        "All will be covered by RTB.",
        "I mean is it public or private??",
        "Public.",
        "Good afternoon director umeze neza ?? Nageze imusanze neza We’re also trying to clean our data ubu tugeze kuri 21.48% Bari muri registration and finance, dusigaranye 67.72% bari muri finance batari muri registration and 10.81% bari muri registration batari muri fiance after this exercise we will at least make sure ko tuzi abanyeshuri bacu aho bari.",
        "Good afternoon JP.",
        "Yego meze neza, glad to arrived safe. Noted and thanks for the update.",
        "Purpose: workshop to develop industry based training trainees manuel.",
        "Give me few.",
        "Is 7 days?",
        "‎image omitted.",
        "Can we boost this on social networks with only 200$ we can make noises around…. It’s a great content.",
        "Good morning.",
        "Good morning.",
        "That’s great idea, let’s meet tomorrow with marketing coordinator to discuss on marketing strategy. Tomorrow at 9:00 AM.",
        "Sure.",
        "Thank you.",
        "Good morning, kindly give me 30 minutes.",
        "Good morning.",
        "Sure.",
        "JP Amakuru ??",
        "‎image omitted.",
        "Good evening Director."
    ],
    'Sender': ['M Prince'] * 30,
    'Receiver': ['K Aline'] * 30
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
