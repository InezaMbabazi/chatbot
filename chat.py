import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Data with messages, sender, and receiver
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
        "Good morning, kindly give me 30 minutes.",
        "Arko I told him something he will remember for sometime.",
        "I knew.",
        "Let's go discuss it in the back (Kinyarwanda).",
        "You deleted this message.",
        "Untitled (3).png (document omitted)",
        "Well, you are doing great work.",
        "It's good to hear how decisions are being made.",
        "Let's say a student is in year 1, attends classes, gets marks, and pays fees. If they pass, they get promoted to year 2. What happens if they fail?",
        "I'm just asking.",
        "Sure… I should show that on the diagram.",
        "That's what I was thinking (Kinyarwanda).",
        "Keep talking (Kinyarwanda).",
        "I focused only on how data should flow but if a student doesn't complete the required credits, they have to repeat the year.",
        "Don't I understand? Let me ask, graduation isn't the data flow of the 3rd year? If all the conditions are fulfilled, someone should graduate, right? Unless there's more information you're getting from the database.",
        "You got me (Kinyarwanda).",
        "I don't know, I'm just trying to understand your data flow diagram ‍♀️.",
        "Yes.",
        "How do I look with my makeup (link to Instagram reel).",
        "(link to another Instagram reel).",
        "You look like an angry bird to me.",
        "Have a good day.",
        "Have a better one too.",
        "Hi.",
        "Umeze neza Kabatesi (How are you, Kabatesi?).",
        "Juss to check on uu (Just to check on you).",
        "I am so busy.",
        "But fine.",
        "Leaving the office shortly.",
        "Oooh! Sorry.",
        "Okae.",
        "(link to Instagram reel).",
        "Can we do this ?!!",
        "So confident…😁😁😁, by the way how did he know?? 🤔",
        "Aww… very touching.",
        "Night night.",
        "Article & Message.docx ‎document omitted.",
        "Yeap.",
        "Man uziko dutekereza kimwe 😅 uziko nari narakoze article ijya kumpera nkiyi uzashyireho tube 2 and we will be telling our kids how twarabahaga turi 2 😅😅😅😅 anyway This article is great rwose, but the magazine will be a better tool to market EAUR sibyo. I think you should not focus about higher learning in general, instead focus on MIS at EAUR. Higher learning in general can be addressed in the introduction…. You should concentrate more on how MIS at EAUR has changed the way of learning by analyzing student data in real time and how we are going to integrate it with AI…..",
        "We have some good points you can emphasize on like… automatic attendance, marks analysis, payment analysis and progress analysis….",
        "Niko mbitekereza.",
        "Sibyo !!?"
    ],
    'Sender': [
        'M Prince', 'K Aline ☺️', 'M Prince', 'M Prince', 'M Prince',
        'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️', 'M Prince',
        'M Prince', 'M Prince', 'M Prince', 'M Prince', 'M Prince',
        'M Prince', 'M Prince', 'M Prince', 'M Prince', 'M Prince',
        'M Prince', 'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️',
        'M Prince', 'K Aline ☺️', 'M Prince', 'M Prince', 'K Aline ☺️',
        'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️', 'M Prince', 'M Prince',
        'K Aline ☺️', 'K Aline ☺️', 'M Prince', 'M Prince', 'M Prince',
        'M Prince', 'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️',
        'M Prince', 'M Prince', 'M Prince', 'M Prince', 'M Prince',
        'M Prince', 'M Prince', 'K Aline ☺️', 'K Aline ☺️', 'M Prince',
        'M Prince', 'K Aline ☺️', 'K Aline ☺️', 'K Aline ☺️', 'M Prince',
        'M Prince'
    ],
    'Receiver': [
        'K Aline' for _ in range(70)  # Adjusted to match the number of messages
    ]
}

# Remove the message that says "‎This message was deleted."
remove_message = "‎This message was deleted."
filtered_data = [(msg, sender) for msg, sender in zip(data['Message'], data['Sender']) if msg != remove_message]

# Unzip the filtered data
filtered_messages, filtered_senders = zip(*filtered_data)

# Update data
data['Message'] = list(filtered_messages)
data['Sender'] = list(filtered_senders)
data['Receiver'] = ['K Aline' for _ in range(len(data['Message']))]  # Update Receiver based on the remaining messages

# Check that lengths are consistent
assert len(data['Message']) == len(data['Sender']) == len(data['Receiver']), \
    "Length mismatch between Message, Sender, and Receiver."

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
