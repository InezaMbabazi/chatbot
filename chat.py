import openai
import pandas as pd
import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize

# Set NLTK data path to the local .nltk_data directory
nltk.data.path.append('./.nltk_data')

# Function to check if NLTK resources are available
def check_nltk_resources():
    try:
        # Check for the standard punkt tokenizer
        nltk.data.find('tokenizers/punkt')
        st.success("NLTK 'punkt' tokenizer is available.")
    except LookupError:
        st.error("NLTK 'punkt' tokenizer not found. Please ensure it's available in the .nltk_data directory.")

# Call the function to check resources
check_nltk_resources()

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Function to preprocess text
def preprocess_text(text):
    try:
        # Tokenize using NLTK (for simple NLP tasks)
        tokens = word_tokenize(text.lower())
        return tokens
    except Exception as e:
        st.error(f"Error processing text: {str(e)}")
        return []

# Function to fetch and parse content from a website
def fetch_website_content(url):
    try:
        # Send a request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text from the website (we can refine this based on the structure)
        paragraphs = soup.find_all('p')
        website_text = " ".join([para.get_text() for para in paragraphs])

        # Optionally, include headers or other sections that might provide important context
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        website_text += " ".join([header.get_text() for header in headers])

        return website_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return ""

# Load website content (replace this URL with your actual website URL)
website_url = "https://keplercollege.ac.rw/"  # Replace with your website URL
website_content = fetch_website_content(website_url)

# Function to get a response from OpenAI API using the website content
def get_openai_response(question, context):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"{question}\n\nContext: {context}"}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to get specific information based on curriculum details from the website
def get_course_info_by_year(year, content):
    # Example pattern to extract Year 1 curriculum from website content
    if 'Year 1' in content:
        year_1_data = """
        Year 1:
        In their first year in the program, students delve into the fundamental principles of project management. Topics include project scope and design, project management information systems, principles of management, and the fundamentals of project management. Emphasis is placed on building a strong theoretical foundation that serves as the cornerstone for more advanced concepts in subsequent years, and on technology, critical thinking, and problem-solving skills.

        Courses:
        Trimester 1:
        - ENG6101 | English Communication Skills 1: Fundamentals of Grammar and Reading | 20 Credits
        - ETH6101 | Critical Thinking and Ethical Problem Solving | 10 Credits
        - TEC6101 | Computer Applications 1: Microsoft Word and Google Suite | 10 Credits
        - PCO6101 | Professional Foundations | 10 Credits

        Trimester 2:
        - ENG6202 | English Communication Skills 2: Academic Writing | 10 Credits
        - MTH6201 | Business Mathematics | 10 Credits
        - TEC6202 | Computer Applications 2: Microsoft Excel and Powerpoint | 10 Credits
        - MGT6201 | Principles of Management | 10 Credits
        - PRM6201 | Fundamentals of Project Management | 15 Credits
        """
        return year_1_data
    else:
        return "Sorry, I could not find detailed information for that year."

# Example chatbot database (replace with your actual data)
chatbot_data = {
    'question': ['What is Kepler College?', 'How do I apply?', 'What programs are offered?', 'What do we learn in Year 1 of Project Management?'],
    'answer': [
        "Kepler College is a dynamic institution providing quality education in various fields.",
        "To apply, visit our website and fill out the online application form.",
        "Kepler College offers programs in various disciplines, including Business, IT, and Education.",
        get_course_info_by_year(1, website_content)  # Year 1 Project Management curriculum
    ]
}

# Convert the example database into a pandas DataFrame
chatbot_df = pd.DataFrame(chatbot_data)

# Streamlit UI with header image and instructions
header_image_path = "header.png"  # Ensure this image exists in your working directory
if os.path.exists(header_image_path):
    st.image(header_image_path, use_column_width=True)
else:
    st.warning("Header image not found. Please upload 'header_image.png'.")

# Add chatbot title and instructions
st.title("Kepler College Chatbot")

st.markdown("""
    <div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #2E86C1;">Welcome to Kepler College's AI-Powered Chatbot</h3>
        <p>To interact with this AI assistant, you can:</p>
        <ul style="list-style-type: square;">
            <li>Type a question or message in the input field below and press Enter to submit.</li>
            <li>The chatbot will respond based on the website's content and knowledge base.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Initialize a session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialize a session state for user input clearing
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""  # Default to empty string

# Function to handle user input after pressing Enter
def handle_user_input():
    user_input = st.session_state.input_text.strip()  # Get the input text

    if user_input != "":
        # First, try to get a response from the chatbot database
        chatbot_response = get_database_info(user_input, chatbot_df)

        # If no useful answer from the database, fallback to the website content
        if "Sorry" in chatbot_response:
            chatbot_response = get_openai_response(user_input, website_content)

        # Add the conversation to session state
        st.session_state.conversation.append({"user": user_input, "chatbot": chatbot_response})

        # Clear the input field by resetting the session state correctly
        st.session_state.input_text = ""  # This clears the input field after sending the message

# User input field with the updated functionality for Enter key
user_input = st.text_input("You:", value=st.session_state.input_text, key="input_text", on_change=handle_user_input)

# Display the last 3 conversations with new messages on top
if st.session_state.conversation:
    st.markdown("<h4>Conversation History:</h4>", unsafe_allow_html=True)
    for chat in reversed(st.session_state.conversation[-3:]):
        st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>"
                    f"<strong>You:</strong> {chat['user']}<br>"
                    f"<strong>Chatbot:</strong> {chat['chatbot']}</div>", unsafe_allow_html=True)
