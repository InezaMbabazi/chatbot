import re
import streamlit as st
from difflib import SequenceMatcher

# Load and clean chat data
def load_chat(file_object):
    message_pattern = re.compile(r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)$')
    messages = []

    for line in file_object:
        line = line.decode('utf-8') if isinstance(line, bytes) else line
        match = message_pattern.match(line)
        if match:
            _, _, sender, message = match.groups()
            messages.append({"sender": sender.strip(), "message": message.strip()})
    return messages

# Build contextual pairs: look at last 2-3 messages before Aline replies
def build_contextual_pairs(messages, you='M.Prince', her='K Aline'):
    pairs = []
    i = 0
    while i < len(messages) - 1:
        if messages[i]['sender'] == you:
            context = messages[i]['message']
            j = i + 1
            while j < len(messages) and messages[j]['sender'] == you:
                context += " " + messages[j]['message']
                j += 1
            if j < len(messages) and messages[j]['sender'] == her:
                pairs.append((context.strip(), messages[j]['message']))
            i = j
        else:
            i += 1
    return pairs

# Compare similarity
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Find best match
def get_reply(user_input, pairs, threshold=0.4):  # Lower threshold
    # Check for common greetings
    common_greetings = {
        "hi": "Hey JP",
        "hello": "Hey JP",
        "hey": "Hey JP"
    }
    user_input_lower = user_input.lower()
    
    if user_input_lower in common_greetings:
        return common_greetings[user_input_lower]
    
    best_score = 0
    best_reply = None
    for q, a in pairs:
        score = similarity(user_input, q)
        if score > best_score:
            best_score = score
            best_reply = a
    if best_score >= threshold:
        return best_reply
    return "I'm not sure how to respond 😅"

# Streamlit app interface
st.title("💬 Chat with Aline (AI version)")

# Upload chat file
chat_file = st.file_uploader("Upload your WhatsApp chat (.txt)", type=["txt"])

if chat_file:
    messages = load_chat(chat_file)
    pairs = build_contextual_pairs(messages)

    # Text input for user query
    user_input = st.text_input("You (M.Prince):", "")

    if user_input:
        # Get a reply based on the best matching message
        reply = get_reply(user_input, pairs)
        st.text_area("Aline:", value=reply, height=100)

    # Clear the input field after response
    if st.button("Clear Input"):
        st.text_input("You (M.Prince):", "")
