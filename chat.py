import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load or define your bot data (replace this with your actual dataset)
# Make sure you have a CSV file with 'User_Input' and 'Bot_Response' columns
bot_data = pd.DataFrame({
    'User_Input': ['hello', 'how are you', 'bye', 'thanks','How do I apply for admission?',
'What are the admission requirements?',
'Is financial aid available?',
'What is the campus like?',
'Can I transfer credits from another institution?',
'What is the deadline for applications?',
'Are there any scholarships available?',
'How can I contact the admissions office?',
'What support services are available for students?',
'What programs does Kepler college College offer?',
'Is the education at Kepler college College recognized internationally?',
'What is Kepler college’s teaching approach?',
'How competitive is admission to Kepler college College?',
'What are the admission requirements?',
'Does Kepler college College offer scholarships?',
'What is life like on Kepler college\'s campus?',
'Does Kepler college offer housing to students?',
'What support services are available for students?',
'What are Kepler college graduates\' job prospects?',
'Does Kepler college offer internships or practical training?',
'How does Kepler college prepare students for the job market?',
'How affordable is it to study at Kepler college College?',
'Are there flexible payment plans for tuition?',
'How do scholarships and financial aid work at Kepler college?',
'What leadership or extracurricular opportunities does Kepler college offer?',
'Can I engage in volunteer work or community projects while at Kepler college?',
'How diverse is Kepler college College\'s student body?',
'How does Kepler college use technology in its learning environment?',
'Is Kepler college College connected to global networks?',
'What are the career outcomes for Kepler college graduates?',
'How does Kepler college support student entrepreneurship?',
'Can international students apply to Kepler college College?',
'What languages are used for instruction at Kepler college?',
'How does Kepler college integrate real-world projects into its curriculum?',
'What opportunities are there for alumni engagement at Kepler college?',
'Does Kepler college College have partnerships with local businesses?',
'How are faculty members selected at Kepler college?',
'How does Kepler college handle student diversity and inclusion?',
'What makes Kepler college different from other universities in Rwanda?',
'How can I apply to Kepler college?',
'What are the most popular majors at Kepler college?',
'How does Kepler college ensure students’ academic success?',
'Are there any study abroad programs or exchange opportunities?',
'Does Kepler college have any religious affiliation?',
'What are the technological resources available to students?',
'How does Kepler college help students balance academic and personal life?',
'What is Kepler college’s mission?',
'How long does it take to complete a degree at Kepler college?',
'What career paths do Kepler college graduates typically pursue?',
'How does Kepler college measure student performance?',
'What is Kepler college\'s approach to leadership development?',
'How does Kepler college integrate social impact into its education?',
'Does Kepler college have an online learning option?',
'What extracurricular activities are available to students at Kepler college?',
'Tell me about Kepler college',
'How many intakes?',
'intake open',
'support phone number, admission number, registration number',
'What is the student-to-faculty ratio at Kepler?',
'Does Kepler provide scholarships or financial aid?',
'What are Kepler’s core values?',
'How does Kepler support students\' personal development?',
'What kind of academic support is available for students struggling with their studies?',
'Is there a career center at Kepler?',
'How does Kepler integrate technology in the learning process?',
'What are the living arrangements for students at Kepler?',
'Are there any partnerships between Kepler and other universities?',
'What is the process for transferring credits to Kepler from another institution?',
'What is Kepler\'s approach to sustainability and community engagement?',
'How does Kepler prepare students for the global job market?',
'Does Kepler offer postgraduate programs?',
'What extracurricular opportunities are available at Kepler?',
'How does Kepler foster innovation among its students?',
'What are the key challenges Kepler students face, and how does the college address them?',
'How does Kepler contribute to the education landscape in Rwanda?',
'What kind of internships are available to Kepler students?',
'How does Kepler ensure its programs stay relevant to the job market?',
'How do Kepler students stay connected with alumni?',
'What kind of research opportunities are available at Kepler?',
'campuses'

],
    'Bot_Response': ['Hi there!', 'I am good, how about you?', 'Goodbye!', 'You are welcome!','To apply for admission, visit our website and fill out the online application form.', 'Admission requirements include a high school diploma and proof of English proficiency.', 'Yes, financial aid is available for eligible students through various programs.', 'The campus is vibrant, with modern facilities and a supportive community.', 'Yes, you can transfer credits. Please consult our admissions team for details.', 'The deadline for applications is typically May 31 for the upcoming academic year.', 'Yes, we offer scholarships based on merit and need. Check our website for details.', 'You can contact the admissions office at admissions@Kepler college.edu or call +123456789.', 'We provide various support services, including academic advising, counseling, and career services.', 'Kepler college offers undergraduate degrees in business, communications, and healthcare management, with international recognition through partnerships with U.S.-based universities.', 'Yes, Kepler college partners with Southern New Hampshire University (SNHU) to offer U.S.-accredited degrees, recognized worldwide.', 'Kepler college uses a competency-based learning model combining online coursework with in-person coaching to ensure students gain practical skills.', 'Admission is competitive, focusing on academic performance, leadership potential, and motivation to succeed in a competency-based environment.', 'Applicants need a high school diploma, English proficiency, and must pass the entrance exam or selection process.', 'Yes, Kepler college offers merit-based scholarships and financial aid for students demonstrating academic excellence and financial need.', 'Kepler college fosters a collaborative learning environment with access to technology, study areas, and extracurricular activities. Students also engage in professional development.', 'Yes, Kepler college provides on-campus accommodation, though some students may opt for off-campus housing.', 'Kepler college offers career coaching, academic advising, mental health services, and professional networking to support student development.', 'Kepler college graduates enjoy strong employment rates, with many securing internships and jobs in sectors like international organizations, businesses, and government.', 'Yes, Kepler college emphasizes hands-on learning through internships and apprenticeships, helping students gain real-world experience.', 'Kepler college’s competency-based education, career coaching, and employer partnerships equip students with skills to thrive in the job market.', 'Kepler college is committed to affordability, with tuition fees varying by program. Scholarships and financial aid are available to reduce costs.', 'Yes, Kepler college offers flexible payment plans and installment options for students needing financial flexibility.', 'Scholarships are awarded based on merit and financial need, with aid packages tailored to each student’s situation.', 'Kepler college provides leadership programs, student clubs, and social activities, fostering leadership skills and networking opportunities.', 'Yes, students are encouraged to participate in community service, volunteer projects, and social impact initiatives.', 'Kepler college attracts students from across Rwanda and neighboring countries, creating a diverse community with varying backgrounds.', 'Kepler college integrates technology through online platforms, digital resources, and virtual classrooms to deliver modern, student-centered education.', 'Yes, Kepler college is part of a global network through partnerships with SNHU and other organizations, offering cross-cultural learning and global exposure.', 'Many Kepler college graduates find employment in top local and international companies, NGOs, and government agencies. Kepler college’s strong career services and alumni network play a key role in these outcomes.', 'Kepler college encourages entrepreneurship by offering mentorship programs, startup incubators, and workshops on innovation and business creation.', 'Yes, Kepler college accepts international students from neighboring countries and beyond. The institution provides support for adjusting to life in Rwanda.', 'English is the primary language of instruction, and students are expected to have a good command of English before enrolling.', 'Kepler college’s competency-based model includes real-world projects, case studies, and internships that help students apply their learning to practical scenarios.', 'Kepler college maintains a strong alumni network that offers mentorship, professional development, and job opportunities for both current students and graduates.', 'Yes, Kepler college collaborates with local businesses and organizations to provide internship opportunities and job placements for students and graduates.', 'Faculty at Kepler college are highly qualified professionals with significant experience in their respective fields, and they are selected for their commitment to student success and experiential learning.', 'Kepler college promotes diversity and inclusion by welcoming students from different socioeconomic backgrounds and offering programs that cater to various learning needs.', 'Kepler college stands out due to its competency-based education, international degree partnerships, emphasis on practical skills, and strong career services that prepare students for the workforce.', 'You can apply to Kepler college by visiting their website and completing the online application form. The process includes submitting academic records, passing an entrance exam, and attending an interview.', 'Business administration, healthcare management, and communications are among the most popular majors at Kepler college, due to their relevance in Rwanda’s growing economy.', 'Kepler college provides personalized coaching, regular assessments, and tailored support to ensure students meet academic goals and develop competencies needed for graduation.', 'Yes, through Kepler college’s global partnerships, students may have the opportunity to engage in exchange programs, internships, or short-term study abroad experiences.', 'Kepler college is a secular institution and does not have any religious affiliation, though it respects and accommodates students from all religious backgrounds.', 'Kepler college provides students with access to modern technology, including computers, online learning platforms, and digital resources to support their education.', 'Kepler college offers student counseling, wellness programs, and a flexible learning model that allows students to balance academic demands with personal and professional commitments.', 'Kepler college’s mission is to provide accessible, high-quality education that equips students with the skills needed to thrive in the global job market.', 'Most undergraduate programs at Kepler college take about three to four years to complete, depending on the student’s pace and program requirements.', 'Kepler college graduates often pursue careers in business, healthcare, non-profit management, and communications, while others become entrepreneurs or continue with postgraduate studies.', 'Kepler college uses a competency-based system where students are assessed based on their ability to demonstrate specific skills and knowledge, rather than through traditional grading.', 'Kepler college integrates leadership training into its curriculum through practical projects, leadership workshops, and opportunities for students to take on leadership roles in extracurricular activities.', 'Kepler college emphasizes social impact by encouraging students to engage in community service, sustainability projects, and initiatives that address local and global challenges.', 'Yes, Kepler college offers a blended learning model where students engage in both online courses and in-person coaching, allowing for flexible learning schedules.', 'Kepler college offers a range of extracurricular activities, including clubs, sports, debate teams, and leadership programs that help students develop socially and professionally.', 'Kepler is a high learning institution in Rwanda with different programs like project management, business analytics, and SNHU. Since 2012, Kepler has been reinventing higher education and creating pathways for vulnerable African populations.', 'There are three intakes: September for project management, January for business analytics, and March for SNHU.', 'The January intake starts from 16th September to 5th March 2024.', 'Kepler maintains a low student-to-faculty ratio to ensure personalized attention and support for every student.', 'Yes, Kepler offers scholarships and financial aid to students based on merit and need.', 'Kepler emphasizes innovation, collaboration, inclusivity, and excellence in education.', 'Kepler offers counseling services, mentorship, leadership training, and extracurricular activities to promote personal growth.', 'Kepler provides tutoring, coaching, and workshops for students who need academic assistance.', 'Yes, Kepler has a dedicated career center that offers career counseling, resume building, interview preparation, and job placement services.', 'Kepler uses blended learning with a combination of online resources, in-person coaching, and technology tools to enhance student learning.', 'Kepler provides housing options for students, including dormitories and assistance in finding off-campus accommodations.', 'Yes, Kepler has partnerships with international institutions that provide students with opportunities for global exposure and earning accredited degrees.', 'Kepler evaluates transfer credits on a case-by-case basis, ensuring they align with the curriculum and competencies required for graduation.', 'Kepler is committed to sustainability and encourages students to participate in community service, environmental projects, and initiatives that benefit the community.', 'Kepler focuses on building global competencies through internships, real-world projects, soft skills training, and connecting students with international opportunities.', 'Currently, Kepler focuses on undergraduate programs, but there are partnerships and pathways for students interested in pursuing postgraduate studies.', 'Students can participate in a variety of clubs, sports, cultural activities, leadership roles, and social impact projects.', 'Kepler encourages innovation by offering workshops, hackathons, and innovation labs that allow students to experiment with new ideas and technologies.', 'Common challenges include adjusting to competency-based education and managing time. Kepler provides strong coaching and support to help students overcome these challenges.', 'Kepler is a pioneer in competency-based education in Rwanda, offering a model that combines international standards with local relevance.', 'Kepler has partnerships with various industries, including tech, business, healthcare, and NGOs, providing students with practical internship opportunities.', 'Kepler regularly updates its curriculum based on industry trends, feedback from employers, and ongoing research into the skills needed in the job market.', 'Kepler has an active alumni network that engages with current students through mentoring programs, networking events, and career workshops.', 'While Kepler focuses on practical learning, students have opportunities to engage in research projects, especially in areas like education, social innovation, and business.', 'Kiziba and Kigali.'


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
