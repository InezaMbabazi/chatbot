import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = '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'  # Replace with your actual OpenAI API key

# List of predefined questions and answers
qa_pairs = {
    "What kind of degrees does Kepler offer?": "Kepler College offers bachelor's programs in Project Management and Business Analytics, focusing on practical, industry-relevant education.",
    "Is Kepler College accredited by HEC?": "Yes, Kepler College is accredited by the Higher Education Council (HEC) of Rwanda.",
    "What can I learn in the Project Management program at Kepler College?": "The Project Management program covers planning, execution, monitoring, and managing project teams, preparing students for leadership roles in various sectors.",
    "What is the focus of the Business Analytics program at Kepler College?": "The Business Analytics program emphasizes data analysis, decision-making tools, and business intelligence to help students make data-driven decisions in organizations.",
    # Add more question-answer pairs here
}

def get_chatgpt_response(user_input):
    """Fetches a response from the OpenAI ChatGPT model."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use gpt-4 if you have access
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    st.title("Kepler College Chatbot")

    user_input = st.text_input("You: ", "")

    if st.button("Send"):
        if user_input:
            # Check if the user input matches any predefined questions
            if user_input in qa_pairs:
                answer = qa_pairs[user_input]
            else:
                # Get response from ChatGPT if not found in predefined questions
                answer = get_chatgpt_response(user_input)

            st.text_area("ChatGPT:", value=answer, height=300)
        else:
            st.error("Please enter a message.")

if __name__ == "__main__":
    main()
