import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Complete chat data (trimmed to 38 entries for consistency)
data = {
    'Date': [
        '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022',
        '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022',
        '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022',
        '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022',
        '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022', '20/10/2022',
        '24/10/2022', '24/10/2022', '24/10/2022', '09/11/2022', '09/11/2022',
        '09/11/2022', '16/11/2022', '16/11/2022', '16/11/2022', '16/11/2022',
        '16/11/2022', '16/11/2022', '17/11/2022', '17/11/2022', '17/11/2022',
        '17/11/2022', '17/11/2022'
    ][:38],  # Keeping only the first 38 entries
    'Time': [
        '09:09:06', '09:09:06', '09:09:43', '09:10:34', '09:27:41',
        '09:28:17', '09:28:32', '09:28:42', '17:30:50', '17:30:52',
        '17:40:02', '19:01:26', '19:04:10', '19:05:37', '19:06:12',
        '19:06:15', '19:07:01', '19:09:54', '19:14:21', '19:14:30',
        '19:15:32', '19:22:06', '19:31:13', '19:31:59', '20:57:40',
        '12:09:18', '12:17:21', '12:19:12', '17:18:05', '17:45:32',
        '17:50:55', '09:17:40', '09:18:33', '09:18:38', '10:22:41',
        '10:53:32', '21:36:42', '21:36:50', '09:05:50', '09:07:40',
        '09:07:45', '19:16:09', '19:17:00', '19:56:16'
    ][:38],  # Keeping only the first 38 entries
    'Sender': [
        'K Aline', 'M Prince', 'M Prince', 'M Prince', 'K Aline',
        'K Aline', 'M Prince', 'M Prince', 'M Prince', 'M Prince',
        'K Aline', 'M Prince', 'K Aline', 'K Aline', 'M Prince',
        'M Prince', 'K Aline', 'K Aline', 'M Prince', 'M Prince',
        'K Aline', 'M Prince', 'K Aline', 'M Prince', 'M Prince',
        'M Prince', 'K Aline', 'K Aline', 'M Prince', 'K Aline',
        'M Prince', 'K Aline', 'M Prince', 'K Aline', 'M Prince',
        'K Aline', 'M Prince', 'M Prince', 'K Aline', 'M Prince',
        'M Prince', 'K Aline', 'K Aline', 'M Prince', 'K Aline'
    ][:38],  # Keeping only the first 38 entries
    'Receiver': [
        'M Prince', 'K Aline', 'K Aline', 'K Aline', 'M Prince',
        'M Prince', 'K Aline', 'K Aline', 'K Aline', 'K Aline',
        'M Prince', 'K Aline', 'M Prince', 'M Prince', 'K Aline',
        'K Aline', 'M Prince', 'M Prince', 'M Prince', 'M Prince',
        'M Prince', 'K Aline', 'K Aline', 'M Prince', 'M Prince',
        'M Prince', 'K Aline', 'K Aline', 'K Aline', 'K Aline',
        'K Aline', 'K Aline', 'K Aline', 'K Aline', 'K Aline',
        'K Aline', 'M Prince', 'M Prince', 'M Prince', 'M Prince',
        'M Prince', 'M Prince', 'K Aline', 'M Prince', 'K Aline'
    ][:38],  # Keeping only the first 38 entries
    'Message': [
        "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.",
        "Good morning campus director!! Hope you’re doing pretty fine! I would like to ask you a favor and a guidance, RTB have requested me to go for curriculum review and they have sent an email to the Vc, I was supposed to go in this week but with this activity we’re having now I told them I’ll come in this upcoming Sunday until 4th November, but they have requested me to send my mission order which will start on 23 to 4th November for the preparation of accommodation and etc… and the problem I’ll come back to Kigali tomorrow evening when your office and the office of Vc will be closed … I was asking my self if I can get a support from you or an advise how I can get that mission order. Thank you.",
        "Request to release Experts in Hospitality and tourism_0001_0001.pdf • ‎4 pages ‎document omitted",
        "You deleted this message.",
        "Good morning J.P, I’m doing well, I hope you’re doing good too. It’s fine I’ll have your mission order ready and send it to your email.",
        "I think that will work for you.",
        "I’m doing pretty fine.",
        "Sure and thank you.",
        "Hello.",
        "director.",
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
    ][:38]  # Keeping only the first 38 entries
}

# Create DataFrame
df = pd.DataFrame(data)

# Prepare the data for the model
X = df['Message']
y = df['Sender']  # Assuming the goal is to predict the Sender

# Build and train the model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X, y)

# Streamlit app
st.title('Chat Message Sender Prediction')

# Input for user message
user_message = st.text_area("Enter a message:")

if st.button("Predict Sender"):
    prediction = model.predict([user_message])
    st.write(f"The predicted sender is: **{prediction[0]}**")
