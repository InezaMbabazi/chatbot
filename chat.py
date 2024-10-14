import streamlit as st
import openai

# Load OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Streamlit UI
st.title("Kepler College Chatbot")

# Input for user message
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        try:
            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Specify the model
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            # Extract the answer from the response
            answer = response.choices[0].message['content']
            st.text_area("Bot:", answer, height=300)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a message.")
