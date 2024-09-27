import streamlit as st
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Title of the chatbot app
st.title("Kepler College Project Management Chatbot")

# Knowledge base from the orientation document
knowledge_base = {
    "program overview": (
        "Kepler College offers affordable, scalable, and competence-based higher education programs. "
        "The Bachelor of Arts in Project Management focuses on equipping students with 21st-century transferable skills."
    ),
    "duration": (
        "The Bachelor of Arts in Project Management program takes 3 years to complete for students with good academic progression."
    ),
    "learning modalities": (
        "Learning modalities include in-person classes, online learning through Canvas, and independent learning."
    ),
    "foundation program": (
        "The foundation program focuses on key skills such as English language, technology, critical thinking, and professional competencies, "
        "lasting for 6 months (two trimesters of Year 1)."
    ),
    "assessment structure": (
        "Kepler College uses a competence-based assessment model, including formative assessments that do not contribute to the final grade, "
        "and summative assessments that do."
    ),
    "grading process": (
        "Students are evaluated using a rubric, and to pass, a student must achieve at least a 4 on each assessed rubric."
    ),
    "career support": (
        "The Careers Department helps students prepare for their careers, offering job readiness support and facilitating internships and employment."
    ),
    "attendance expectations": (
        "Students must arrive at least 5 minutes before class, and lateness without valid communication may be reported as a violation of the code of conduct."
    ),
    "dress code": (
        "The dress code at Kepler College is business casual."
    ),
    "academic integrity": (
        "Plagiarism and academic dishonesty are not tolerated and may result in disciplinary measures."
    ),
}

# Prepare the knowledge base for NLP processing
questions = list(knowledge_base.keys())
answers = list(knowledge_base.values())

# Vectorize the questions using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(questions)

# User input from Streamlit text input
user_input = st.text_input("Ask a question about the Project Management program:")

if user_input:
    # Preprocess user input
    user_input_vector = vectorizer.transform([user_input])

    # Calculate similarity scores between user input and knowledge base
    cosine_similarities = linear_kernel(user_input_vector, tfidf_matrix).flatten()

    # Find the index of the best matching question
    best_match_index = np.argmax(cosine_similarities)
    best_match_score = cosine_similarities[best_match_index]

    # Set a threshold for response
    threshold = 0.1  # You can adjust this value

    if best_match_score > threshold:
        st.write(answers[best_match_index])
    else:
        st.write("I'm sorry, I couldn't find an answer to your question. Please ask something else.")
