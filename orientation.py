import streamlit as st

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
    # Add more intents and responses as needed
}

# User input from Streamlit text input
user_input = st.text_input("Ask a question about the Project Management program:")

if user_input:
    # Convert user input to lower case for matching
    user_input = user_input.lower()
    response_found = False

    # Check for matching intent in the knowledge base
    for key in knowledge_base:
        if key in user_input:
            st.write(knowledge_base[key])
            response_found = True
            break

    if not response_found:
        st.write("I'm sorry, I couldn't find an answer to your question. Please ask something else.")
