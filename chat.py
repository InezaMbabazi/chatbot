import streamlit as st
import openai

# Load OpenAI API key from secrets
openai.api_key =  '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'
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
