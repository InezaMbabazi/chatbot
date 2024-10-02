import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# Replace with your Canvas API token and base URL
API_TOKEN = '1941~FXJZ2tYC2DTWQr923eFTaXy473rK73A4KrYkT3uVy7WeYV9fyJQ4khH4MAGEH3Tf'
BASE_URL = 'https://kepler.instructure.com/api/v1'

# Set headers for authentication
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Function to fetch all courses (same as before)
# ... [existing fetch_all_courses function here]

# Function to fetch assignment groups (same as before)
# ... [existing fetch_assignment_groups function here]

# Function to fetch assignments (same as before)
# ... [existing fetch_assignments function here]

# Function to fetch student submissions for an assignment (same as before)
# ... [existing fetch_grades function here]

# Function to fetch student names (same as before)
# ... [existing fetch_student_name function here]

# Function to calculate total grades and format data for transcripts
def format_gradebook(course_id):
    gradebook = []
    assignment_groups = fetch_assignment_groups(course_id)
    
    for group in assignment_groups:
        assignments = fetch_assignments(course_id, group['id'])
        for assignment in assignments:
            grades = fetch_grades(course_id, assignment['id'])
            for submission in grades:
                student_id = submission['user_id']
                student_name = fetch_student_name(student_id)
                grade = submission.get('score', 0)
                max_score = assignment.get('points_possible', 0)
                
                # Ensure grades are numeric
                grade = float(grade) if grade is not None else 0

                gradebook.append({
                    'Student ID': student_id,
                    'Student Name': student_name,
                    'Assignment Name': assignment['name'],
                    'Grade': grade,
                    'Max Score': max_score
                })
    
    df = pd.DataFrame(gradebook)

    # Group by student and calculate the total grade
    if not df.empty:
        df = df.groupby(['Student ID', 'Student Name']).agg({
            'Grade': 'sum'
        }).reset_index()
    
    return df

# Function to display a transcript for a specific student
def display_student_transcript(student_id, student_name):
    st.header(f"Transcript for {student_name} (ID: {student_id})")
    
    # Fetch all grades across courses
    all_grades = []
    courses = fetch_all_courses()
    for course in courses:
        course_id = course['id']
        course_name = course['name']
        df_gradebook = format_gradebook(course_id)

        # Filter grades for the selected student
        student_grades = df_gradebook[df_gradebook['Student ID'] == student_id]
        if not student_grades.empty:
            student_grades['Course Name'] = course_name
            all_grades.append(student_grades)

    # Combine all grades into one DataFrame
    if all_grades:
        transcript_df = pd.concat(all_grades)
        st.dataframe(transcript_df[['Course Name', 'Grade']])
        
        # Display total grade
        total_grade = transcript_df['Grade'].sum()
        st.subheader(f"Total Grade: {total_grade}")
    else:
        st.write("No grades found for this student.")

# Streamlit display function to show courses and their grades
def display_all_courses_grades():
    courses = fetch_all_courses()
    st.title("Course Grades")

    # Define the date threshold
    date_threshold = datetime.strptime("2024-05-01", "%Y-%m-%d")

    # Display all courses fetched
    for course in courses:
        course_id = course['id']
        course_name = course['name']
        start_at = course.get('start_at')

        if start_at:
            try:
                course_start_date = datetime.strptime(start_at, "%Y-%m-%dT%H:%M:%SZ")
                if course_start_date > date_threshold:
                    # Fetch and display the gradebook
                    df_gradebook = format_gradebook(course_id)
                    
                    if not df_gradebook.empty:
                        st.header(f"Course: {course_name} (ID: {course_id})")
                        st.dataframe(df_gradebook)
            except ValueError:
                st.error(f"Error parsing start date for course {course_name} (ID: {course_id}).")

# Streamlit app starts here
if __name__ == "__main__":
    # Create a sidebar menu for selecting students
    st.sidebar.title("Menu")
    students = set()  # Use a set to avoid duplicates

    # Fetch all grades to populate the student list
    courses = fetch_all_courses()
    for course in courses:
        course_id = course['id']
        df_gradebook = format_gradebook(course_id)
        students.update(df_gradebook['Student ID'].unique())

    # Display the transcript option in the sidebar
    selected_student_id = st.sidebar.selectbox("Select a Student", list(students))
    if selected_student_id:
        student_name = fetch_student_name(selected_student_id)
        display_student_transcript(selected_student_id, student_name)

    display_all_courses_grades()
