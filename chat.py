import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = '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'

# Function to get response from ChatGPT
def get_chatgpt_response(user_message):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": user_message}]
    )
    return response['choices'][0]['message']['content']

# Streamlit app layout
st.title("Kepler College Chatbot")

# User input
user_input = st.text_input("Ask a question:")

if st.button("Send"):
    if user_input:
        answer = get_chatgpt_response(user_input)
        st.text_area("ChatGPT's response:", value=answer, height=300)
    else:
        st.error("Please enter a question.")

# Optional: Display static FAQ (if desired)
st.subheader("Frequently Asked Questions")
faqs = {
    "What kind of degrees does Kepler offer?": "Kepler College offers bachelor's programs in Project Management and Business Analytics, focusing on practical, industry-relevant education.",
    "Is Kepler College accredited by HEC?": "Yes, Kepler College is accredited by the Higher Education Council (HEC) of Rwanda.",
    # Add more FAQs as needed
}

for question, answer in faqs.items():
    st.write(f"**Q:** {question}")
    st.write(f"**A:** {answer}")
