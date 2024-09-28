import streamlit as st
import pandas as pd
import random

# Existing dataset ensuring all messages, senders, and receivers are aligned
data = {
    'Message': [
        "Arko I told him something he will remember for sometime",
        "I knew",
        "Let's go discuss it in the back (Kinyarwanda)",
        "Untitled (3).png (document omitted)",
        "Well, you are doing great work.",
        "It's good to hear how decisions are being made",
        "Let's say a student is in year 1, attends classes, gets marks, and pays fees. If they pass, they get promoted to year 2. What happens if they fail?",
        "I'm just asking",
        "Sure… I should show that on the diagram",
        "That's what I was thinking (Kinyarwanda)",
        "Keep talking (Kinyarwanda)",
        "I focused only on how data should flow but if a student doesn't complete the required credits, they have to repeat the year.",
        "Don't I understand? Let me ask, graduation isn't the data flow of the 3rd year? If all the conditions are fulfilled, someone should graduate, right? Unless there's more information you're getting from the database.",
        "You got me (Kinyarwanda)",
        "I don't know, I'm just trying to understand your data flow diagram ‍♀️",
        "Yes",
        "How do I look with my makeup (link to Instagram reel)",
        "(link to another Instagram reel)",
        ", you look like an angry bird to me",
        "Have a good day",
        "Have a better one too",
        "Hi",
        "umeze neza Kabatesi (How are you, Kabatesi?)",
        "Just to check on uu (Just to check on you)",
        "I am so busy",
        "but fine",
        "leaving the office shortly",
        "oooh! sorry",
        "okae",
        "(link to Instagram reel)",
        "Can we do this ?!!",
        "So confident…😁😁😁, by the way how did he know?? 🤔",
        "Aww… very touching",
        "Night night",
        "Yeap",
        "Man uziko dutekereza kimwe 😅 uziko nari narakoze article ijya kumpera nkiyi uzashyireho tube 2 and we will be telling our kids how twarabahaga turi 2 😅😅😅😅 anyway This article is great rwose, but the magazine will be a better tool to market EAUR sibyo. I think you should not focus about higher learning in general, instead focus on MIS at EAUR. Higher learning in general can be addressed in the introduction…. You should concentrate more on how MIS at EAUR has changed the way of learning by analyzing student data in real time and how we are going to integrate it with AI.",
        "We have some good points you can emphasize on like… automatic attendance, marks analysis, payment analysis and progress analysis…",
        "Niko mbitekereza",
        "Sibyo !!?",
        "Message of the day, thank you",
        "Night night babe",
        "Pleasure",
        "Night night",
        "😘",
        "😘",
        "Good morning",
        "Morning",
        "How wz ur night",
        "I was okay, managed to sleep",
        "Glad",
        "Thanks",
        "At work already?",
        "‎image omitted",
        "Okay",
        "Urazi??",
        "Tell me",
        "Tsanze PD yatagiye nijye winjiyemo nyuma",
        "You got at work late",
        "Yeap",
        "Hiii",
        "https://www.instagram.com/reel/DAMsmooCQV8/?igsh=MWJwNzRuMnNpd3I2dg==",
        "Meaning please?",
        "Hey",
        "Just nakunze the caption on it",
        "Are you not able to interpret it ??",
        "Umeze neza ??",
        "Yeah, it looks like someone cheated. So advice says gentlemen should choose mother to their kids not for themselves????",
        "At least",
        "Yeap! U got it",
        "Glad",
        "Don’t let beauty overshadow character…",
        "You should take the advice seriously 😁😁😁",
        "Abana beza ukabareka",
        "Busy today?",
        "Pfite bagahe se",
        "Not much",
        "Mvuye munama",
        "One I guess",
        "Okay",
        "orientation week assessment report f.pdf • ‎5 pages ‎document omitted",
        "ko ushize mubwishi se",
        "Hoya",
        "It’s fine",
        "😳😳",
        "What ??",
        "No need to say sorry",
        "Nabibonye ko ari Joke",
        "Okay",
        "How busy is your week?",
        "It depends on the day, but I’m always available whenever you need me or if there’s something I can do for you…",
        "Thank you",
        "Will you find an evening and see me?",
        "When would you like me to come?",
        "I don’t know that’s why asked first the your least busy day",
        "How about Tomorrow or Wednesday?",
        "Choose a day that you are least busy when you can leave at work a little bit earlier. I don’t want you to get stuck in traffic",
        "Or we can meet on Saturday I’ll be back to my feet I’m sure",
        "Babe, he is better than you who? He doesn’t miss any of Rambo’s moves",
        "I miss you",
        "He is so good 😁😃😃",
        "And why do think I asked you to come see me?",
        "Ever watched Rambo’s movies?",
        "Cz I miss you 😀",
        "All Rambo",
        "From 1 to 4",
        "😁😁😁 whatever",
        "Same, I’m glad you know how perfect he is..",
        "Have you watched last blood",
        "It was long time ago I don’t remember which is which",
        "Ninziza sanaaa",
        "Urazii",
        "Listening…",
        "‎audio omitted",
        "thanks for being there for your friend.",
        "Reporting them will not return your money, just be tough on them",
        "Thxx babe",
        "Uzi ahantu twagiye",
        "Hehe?",
        "Namubwiye go araska iki",
        "Avuga burger",
        "Twagiye hahandi",
        "Ehhh",
        "At least that’s what he wanted",
        "Sha mureke azashake umugore",
        "Igooo",
        "Azamushaka nakira",
        "Friday I had terrible & sharp pain and I felt like Jordan",
        "The developers have you cancelled?"
    ],
    'Sender': [
        "K Aline ☺️", "M Prince", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "M Prince",
        "M Prince", "M Prince", "M Prince", "M Prince", "K Aline ☺️", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", 
        "M Prince", "K Aline ☺️", "M Prince", "M Prince", "M Prince", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", 
        "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince", "M Prince", 
        "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", 
        "M Prince", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "K Aline ☺️", 
        "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", 
        "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", 
        "M Prince", "K Aline ☺️", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince"
    ],
    'Receiver': [
        "M Prince", "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince",
        "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince", 
        "K Aline ☺️", "M Prince", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "M Prince", "K Aline ☺️", 
        "M Prince", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince", "M Prince", "K Aline ☺️", 
        "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", 
        "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince", "K Aline ☺️", "K Aline ☺️", 
        "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince", 
        "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "M Prince", "M Prince", "M Prince", "K Aline ☺️", "K Aline ☺️", 
        "M Prince", "K Aline ☺️", "K Aline ☺️", "K Aline ☺️", "M Prince", "K Aline ☺️", "M Prince"
    ]
}

# To ensure all arrays are the same length
max_length = max(len(data['Message']), len(data['Sender']), len(data['Receiver']))

# Extend Sender and Receiver lists if they are shorter than the longest list
data['Sender'] += ["Unknown"] * (max_length - len(data['Sender']))
data['Receiver'] += ["Unknown"] * (max_length - len(data['Receiver']))

# Create DataFrame from the data
chat_data = pd.DataFrame(data)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get a response based on M Prince's input and return K Aline's replies
def get_chatbot_response(user_message):
    # Simple AI response logic, looking for responses from K Aline
    possible_responses = chat_data[(chat_data['Message'].str.contains(user_message, case=False, na=False)) & 
                                    (chat_data['Sender'] == "K Aline ☺️")]
    
    # If there are matching responses in the dataset
    if not possible_responses.empty:
        # Randomly select a K Aline's response
        response_row = possible_responses.sample(n=1).iloc[0]
        return f"{response_row['Sender']}: {response_row['Message']}"
    
    # Default response if no match is found
    return "I'm not sure how to respond to that. Can you elaborate?"

# Streamlit UI
st.title("Chatbot - M Prince & K Aline Conversation")

# User input
user_input = st.text_input("You:", "")

# Respond to user input
if st.button("Send"):
    if user_input:
        # Add user message to the chat
        st.session_state.messages.append({"sender": "You", "message": user_input})
        
        # Get AI response as K Aline
        ai_response = get_chatbot_response(user_input)
        
        # Add AI response to the chat
        st.session_state.messages.append({"sender": "K Aline ☺️", "message": ai_response})

# Display messages
for msg in st.session_state.messages:
    st.write(f"**{msg['sender']}:** {msg['message']}")
