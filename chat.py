import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Title of the chatbot app
st.title("Kepler College Chatbot")

# Load or define the bot data
bot_data = {
    'User_Input': [
      'hello', 'how are you', 'bye', 'thanks',
        'How do I apply for admission?', 'What are the admission requirements?',
        'Is financial aid available?', 'What is the campus like?',
        'Can I transfer credits from another institution?', 'What is the deadline for applications?',
        'Are there any scholarships available?', 'How can I contact the admissions office?',
        'What support services are available for students?', 'What programs does Kepler College offer?',
        'Is the education at Kepler College recognized internationally?', 'What is Kepler College’s teaching approach?',
        'How competitive is admission to Kepler College?', 'What are the admission requirements?',
        'Does Kepler College offer scholarships?', 'What is life like on Kepler College\'s campus?',
        'Does Kepler College offer housing to students?', 'What support services are available for students?',
        'What are Kepler College graduates\' job prospects?', 'Does Kepler College offer internships or practical training?',
        'How does Kepler College prepare students for the job market?', 'How affordable is it to study at Kepler College?',
        'Are there flexible payment plans for tuition?', 'How do scholarships and financial aid work at Kepler College?',
        'What leadership or extracurricular opportunities does Kepler College offer?', 
        'Can I engage in volunteer work or community projects while at Kepler College?',
        'How diverse is Kepler College\'s student body?', 'How does Kepler College use technology in its learning environment?',
        'Is Kepler College connected to global networks?', 'What are the career outcomes for Kepler College graduates?',
        'How does Kepler College support student entrepreneurship?', 'Can international students apply to Kepler College?',
        'What languages are used for instruction at Kepler College?', 'How does Kepler College integrate real-world projects into its curriculum?',
        'What opportunities are there for alumni engagement at Kepler College?', 'Does Kepler College have partnerships with local businesses?',
        'How are faculty members selected at Kepler College?', 'How does Kepler College handle student diversity and inclusion?',
        'What makes Kepler College different from other universities in Rwanda?', 'How can I apply to Kepler College?',
        'What are the most popular majors at Kepler College?', 'How does Kepler College ensure students’ academic success?',
        'Are there any study abroad programs or exchange opportunities?', 'Does Kepler College have any religious affiliation?',
        'What are the technological resources available to students?', 'How does Kepler College help students balance academic and personal life?',
        'What is Kepler College’s mission?', 'How long does it take to complete a degree at Kepler College?',
        'What career paths do Kepler College graduates typically pursue?', 'How does Kepler College measure student performance?',
        'What is Kepler College\'s approach to leadership development?', 'How does Kepler College integrate social impact into its education?',
        'Does Kepler College have an online learning option?', 'What extracurricular activities are available to students at Kepler College?',
        'Tell me about Kepler College', 'How many intakes are there?', 'When is the January intake?',
        'What is the student-to-faculty ratio at Kepler?', 'Does Kepler provide scholarships or financial aid?', 
        'What are Kepler’s core values?', 'How does Kepler support students\' personal development?',
        'What kind of academic support is available for students struggling with their studies?',
        'Is there a career center at Kepler?', 'How does Kepler integrate technology in the learning process?',
        'What are the living arrangements for students at Kepler?', 'Are there any partnerships between Kepler and other universities?',
        'What is the process for transferring credits to Kepler from another institution?',
        'What is Kepler\'s approach to sustainability and community engagement?', 'How does Kepler prepare students for the global job market?',
        'Does Kepler offer postgraduate programs?', 'What extracurricular opportunities are available at Kepler?',
        'How does Kepler foster innovation among its students?', 'What are the key challenges Kepler students face, and how does the college address them?',
        'How does Kepler contribute to the education landscape in Rwanda?', 'What kind of internships are available to Kepler students?',
        'How does Kepler ensure its programs stay relevant to the job market?', 'How do Kepler students stay connected with alumni?',
        'What kind of research opportunities are available at Kepler?', 'What campuses does Kepler have?'
    ],
    'Bot_Response': [
        'hello', 'how are you', 'bye', 'thanks',
        'How do I apply for admission?', 'What are the admission requirements?',
        'Is financial aid available?', 'What is the campus like?',
        'Can I transfer credits from another institution?', 'What is the deadline for applications?',
        'Are there any scholarships available?', 'How can I contact the admissions office?',
        'What support services are available for students?', 'What programs does Kepler College offer?',
        'Is the education at Kepler College recognized internationally?', 'What is Kepler College’s teaching approach?',
        'How competitive is admission to Kepler College?', 'What are the admission requirements?',
        'Does Kepler College offer scholarships?', 'What is life like on Kepler College\'s campus?',
        'Does Kepler College offer housing to students?', 'What support services are available for students?',
        'What are Kepler College graduates\' job prospects?', 'Does Kepler College offer internships or practical training?',
        'How does Kepler College prepare students for the job market?', 'How affordable is it to study at Kepler College?',
        'Are there flexible payment plans for tuition?', 'How do scholarships and financial aid work at Kepler College?',
        'What leadership or extracurricular opportunities does Kepler College offer?', 
        'Can I engage in volunteer work or community projects while at Kepler College?',
        'How diverse is Kepler College\'s student body?', 'How does Kepler College use technology in its learning environment?',
        'Is Kepler College connected to global networks?', 'What are the career outcomes for Kepler College graduates?',
        'How does Kepler College support student entrepreneurship?', 'Can international students apply to Kepler College?',
        'What languages are used for instruction at Kepler College?', 'How does Kepler College integrate real-world projects into its curriculum?',
        'What opportunities are there for alumni engagement at Kepler College?', 'Does Kepler College have partnerships with local businesses?',
        'How are faculty members selected at Kepler College?', 'How does Kepler College handle student diversity and inclusion?',
        'What makes Kepler College different from other universities in Rwanda?', 'How can I apply to Kepler College?',
        'What are the most popular majors at Kepler College?', 'How does Kepler College ensure students’ academic success?',
        'Are there any study abroad programs or exchange opportunities?', 'Does Kepler College have any religious affiliation?',
        'What are the technological resources available to students?', 'How does Kepler College help students balance academic and personal life?',
        'What is Kepler College’s mission?', 'How long does it take to complete a degree at Kepler College?',
        'What career paths do Kepler College graduates typically pursue?', 'How does Kepler College measure student performance?',
        'What is Kepler College\'s approach to leadership development?', 'How does Kepler College integrate social impact into its education?',
        'Does Kepler College have an online learning option?', 'What extracurricular activities are available to students at Kepler College?',
        'Tell me about Kepler College', 'How many intakes are there?', 'When is the January intake?',
        'What is the student-to-faculty ratio at Kepler?', 'Does Kepler provide scholarships or financial aid?', 
        'What are Kepler’s core values?', 'How does Kepler support students\' personal development?',
        'What kind of academic support is available for students struggling with their studies?',
        'Is there a career center at Kepler?', 'How does Kepler integrate technology in the learning process?',
        'What are the living arrangements for students at Kepler?', 'Are there any partnerships between Kepler and other universities?',
        'What is the process for transferring credits to Kepler from another institution?',
        'What is Kepler\'s approach to sustainability and community engagement?', 'How does Kepler prepare students for the global job market?',
        'Does Kepler offer postgraduate programs?', 'What extracurricular opportunities are available at Kepler?',
        'How does Kepler foster innovation among its students?', 'What are the key challenges Kepler students face, and how does the college address them?',
        'How does Kepler contribute to the education landscape in Rwanda?', 'What kind of internships are available to Kepler students?',
        'How does Kepler ensure its programs stay relevant to the job market?', 'How do Kepler students stay connected with alumni?',
        'What kind of research opportunities are available at Kepler?', 'What campuses does Kepler have?'
    ]
}

bot_df = pd.DataFrame(bot_data)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(bot_df['User_Input'])

# Function to generate a response
def get_response(user_input):
    user_input_tfidf = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_input_tfidf, tfidf_matrix)
    most_similar_index = similarities.argmax()
    return bot_df['Bot_Response'].iloc[most_similar_index]

# User input from Streamlit text input
user_input = st.text_input("Ask a question:")

if user_input:
    response = get_response(user_input)
    st.write("**Bot:**", response)
    st.session_state.chat_history.append(f"You: {user_input}")
    st.session_state.chat_history.append(f"Bot: {response}")

# Display chat history
if 'chat_history' in st.session_state:
    for chat in st.session_state.chat_history:
        st.write(chat)
else:
    st.session_state.chat_history = []
