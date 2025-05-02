import re
import streamlit as st

# Load and clean chat data
def load_chat(file_object):
    message_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}) - ([^:]+): (.+)$')
    messages = []

    for line in file_object:
        line = line.decode('utf-8') if isinstance(line, bytes) else line
        match = message_pattern.match(line)
        if match:
            _, _, sender, message = match.groups()
            messages.append({"sender": sender.strip(), "message": message.strip()})
    return messages

# Build message-response pairs
def build_pairs(messages, you='M.Prince', her='K Aline'):
    pairs = []
    for i in range(len(messages) - 1):
        if messages[i]['sender'] == you and messages[i+1]['sender'] == her:
            pairs.append((messages[i]['message'], messages[i+1]['message']))
    return pairs

# Simple reply logic based on exact or partial match
def get_reply(user_input, pairs):
    user_input_lower = user_input.lower()
    for q, a in pairs:
        if q.lower() in user_input_lower or user_input_lower in q.lower():
            return a
    return "I'm not sure what to say 😅"

# Streamlit app interface
st.title("💬 Chat with Aline (AI version)")

# Upload WhatsApp chat file
chat_file = st.file_uploader("Upload WhatsApp chat (.txt)", type=["txt"])

if chat_file:
    messages = load_chat(chat_file)
    pairs = build_pairs(messages)

    user_input = st.text_input("You:", "")

    if user_input:
        reply = get_reply(user_input, pairs)
        st.text_area("Aline:", value=reply, height=100)
