import streamlit as st
import random

# Sample messages for M Prince and K Aline
messages = [
    {"sender": "M Prince", "message": "Hey, how have you been?"},
    {"sender": "K Aline", "message": "I'm good, just busy with work."},
    {"sender": "M Prince", "message": "Have you managed to fix your internet issues?"},
    {"sender": "K Aline", "message": "Yes, finally! It’s been a relief."},
    {"sender": "M Prince", "message": "That's great to hear! What else is new?"},
    {"sender": "K Aline", "message": "I’ve been thinking about taking a trip soon."},
    {"sender": "M Prince", "message": "That sounds fun! Where do you want to go?"},
    {"sender": "K Aline", "message": "Maybe somewhere by the lake."},
    # Add more messages as needed
]

st.title("Chatbot Simulation")

# Display chat history
for message in messages:
    if message['sender'] == "M Prince":
        st.markdown(f"**{message['sender']}**: {message['message']}")
    else:
        st.markdown(f"**{message['sender']}**: {message['message']}")

# Add a simple input for M Prince to send a new message
user_input = st.text_input("M Prince's Message:")

if st.button("Send"):
    if user_input:
        st.markdown(f"**M Prince**: {user_input}")
        # Respond as K Aline based on historical messages
        response = random.choice([msg['message'] for msg in messages if msg['sender'] == "K Aline"])
        st.markdown(f"**K Aline**: {response}")
    else:
        st.warning("Please enter a message.")
