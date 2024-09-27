import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load or define your bot data (replace this with your actual dataset)
# Make sure you have a CSV file with 'User_Input' and 'Bot_Response' columns
bot_data = pd.DataFrame({
    'User_Input': ['hello', 'how are you', 'bye', 'thanks','How do I apply for admission?'
,'What are the admission requirements?'
],
    'Bot_Response': ['Hi there!', 'I am good, how about you?', 'Goodbye!', 'You are welcome!','To apply for admission, visit our website and fill out the online application form.','Admission requirements include a high school diploma and proof of English proficiency.'

]
})

# Vectorizing the user inputs
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(bot_data['User_Input'])

def chatbot_response(user_input):
    # Transform the user input into a vector
    user_vector = vectorizer.transform([user_input.lower()])
    
    # Compute cosine similarity between the user input and stored inputs
    similarities = cosine_similarity(user_vector, vectors)

    # Find the index of the best match
    best_match_idx = similarities.argmax()

    # Return the bot's response that corresponds to the best match
    return bot_data['Bot_Response'][best_match_idx]

# Streamlit interface
st.title("Chatbot Assistant")

# Initial message
st.write("Hello! I am your assistant. Feel free to chat with me!")

# Create a text input for the user
user_input = st.text_input("You:", "")

# Check if user input is not empty
if user_input:
    if user_input.lower() == "exit":
        st.write("Bot: Goodbye! Have a great day!")
    else:
        # Get the bot's response
        response = chatbot_response(user_input)
        st.write(f"Bot: {response}")

# Footer
st.write("Type 'exit' to end the conversation.")
