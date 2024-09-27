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
       'Hi there!', 'I am good, how about you?', 'Goodbye!', 'You are welcome!',
        'To apply for admission, visit our website and fill out the online application form.', 
        'Admission requirements include a high school diploma and proof of English proficiency.', 
        'Yes, financial aid is available for eligible students through various programs.', 
        'The campus is vibrant, with modern facilities and a supportive community.',
        'Yes, you can transfer credits. Please consult our admissions team for details.', 
        'The deadline for applications is typically May 31 for the upcoming academic year.',
        'Yes, we offer scholarships based on merit and need. Check our website for details.',
        'You can contact the admissions office at admissions@kepler.edu or call +123456789.',
        'We provide various support services, including academic advising, counseling, and career services.',
        'Kepler College offers undergraduate degrees in business, communications, and healthcare management, with international recognition.',
        'Yes, Kepler College partners with Southern New Hampshire University (SNHU) to offer U.S.-accredited degrees, recognized worldwide.',
        'Kepler College uses a competency-based learning model combining online coursework with in-person coaching.', 
        'Admission is competitive, focusing on academic performance, leadership potential, and motivation to succeed.', 
        'Applicants need a high school diploma, English proficiency, and must pass the entrance exam or selection process.', 
        'Yes, Kepler College offers merit-based scholarships and financial aid for students.', 
        'Kepler College fosters a collaborative learning environment with access to technology, study areas, and extracurricular activities.',
        'Yes, Kepler College provides on-campus accommodation.', 
        'Kepler College offers career coaching, academic advising, and mental health services.', 
        'Kepler College graduates enjoy strong employment rates.', 
        'Yes, Kepler College emphasizes hands-on learning through internships.', 
        'Kepler College’s competency-based education, career coaching, and partnerships equip students with job market skills.',
        'Kepler College is committed to affordability, with various scholarships and financial aid.', 
        'Yes, Kepler College offers flexible payment plans.', 
        'Scholarships are awarded based on merit and financial need.', 
        'Kepler College provides leadership programs, student clubs, and social activities.', 
        'Yes, students are encouraged to participate in community service and volunteer projects.', 
        'Kepler College attracts students from across Rwanda and neighboring countries.', 
        'Kepler College integrates technology in online platforms and virtual classrooms.', 
        'Yes, Kepler College is part of a global network through partnerships with SNHU.', 
        'Kepler College graduates secure jobs in top local and international companies.', 
        'Kepler College supports entrepreneurship through mentorship and startup incubators.', 
        'Yes, international students are welcome to apply to Kepler College.', 
        'English is the primary language of instruction.', 
        'Kepler College includes real-world projects, case studies, and internships.', 
        'Kepler College maintains a strong alumni network.', 
        'Yes, Kepler College collaborates with local businesses.', 
        'Faculty at Kepler College are selected for their commitment to student success.', 
        'Kepler College promotes diversity and inclusion.', 
        'Kepler College stands out due to its competency-based education and strong career services.', 
        'You can apply to Kepler College by visiting their website.', 
        'Business administration, healthcare management, and communications are the most popular majors.', 
        'Kepler College provides coaching, assessments, and support to ensure academic success.', 
        'Yes, Kepler College offers exchange programs and study abroad opportunities.', 
        'Kepler College is a secular institution.', 
        'Kepler College provides students with access to modern technology.', 
        'Kepler College offers counseling, wellness programs, and a flexible learning model.', 
        'Kepler College’s mission is to provide accessible, high-quality education.', 
        'Most undergraduate programs take 3 to 4 years to complete.', 
        'Kepler College graduates often pursue careers in business and healthcare.', 
        'Kepler College assesses students based on demonstrated skills.', 
        'Kepler College integrates leadership training into its curriculum.', 
        'Kepler College emphasizes social impact through community service projects.', 
        'Yes, Kepler College offers a blended learning model.', 
        'Students can engage in various clubs, sports, and cultural activities.', 
        'Kepler College is an innovative institution focused on practical learning.', 
        'There are two main intakes in January and September each year.', 
        'The January intake begins classes in mid-January.', 
        'Kepler College maintains a 15:1 student-to-faculty ratio.', 
        'Yes, scholarships and financial aid are available for eligible students.', 
        'Kepler College values integrity, collaboration, and excellence in education.', 
        'Kepler College supports personal development through workshops and mentoring.', 
        'Academic support includes tutoring, workshops, and personalized coaching.', 
        'Yes, there is a career center offering job placement and internship assistance.', 
        'Kepler College uses technology in classrooms and online platforms to facilitate learning.', 
        'Students typically live in campus housing or nearby apartments.', 
        'Yes, Kepler has partnerships with various universities and organizations.', 
        'Transferring credits is possible; please consult the admissions office for details.', 
        'Kepler College promotes sustainability through eco-friendly practices and community engagement.', 
        'Kepler College prepares students for the global job market with international partnerships and training.', 
        'Yes, Kepler offers postgraduate programs in business and education.', 
        'Students can participate in clubs, sports, and leadership opportunities.', 
        'Kepler College fosters innovation through creative projects and entrepreneurship programs.', 
        'Challenges include adapting to the learning model and time management; the college offers support for these.', 
        'Kepler contributes to the education landscape by offering relevant, quality programs.', 
        'Kepler provides internships through partnerships with businesses and organizations.', 
        'Kepler continuously updates its programs based on market research and industry feedback.', 
        'Kepler College facilitates connections between students and alumni through networking events.', 
        'Research opportunities are available in collaboration with faculty and industry partners.', 
        'Kepler has campuses in Kiziba and Kigali.'
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
