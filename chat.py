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

# Function to fetch all courses
def fetch_all_courses():
    response = requests.get(f"{BASE_URL}/courses", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching courses.")
        return []

# Function to fetch assignment groups (same as before)
# ...

# Function to fetch assignments (same as before)
# ...

# Function to fetch student submissions for an assignment (same as before)
# ...

# Function to fetch student names (same as before)
# ...

# Function to calculate total grades and format data for transcripts
# ...

# Function to display a transcript for a specific student
# ...

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
    courses = fetch_all_courses()  # Ensure this function is defined above
    for course in courses:
        course_id = course['id']
        df_gradebook = format_gradebook(course_id)
        students.update(df_gradebook['Student ID'].unique())

    # Display the transcript option in the sidebar
    selected_student_id = st.sidebar.selectbox("Select a Student", list(students))
    if selected_student_id:
        student_name = fetch_student_name(selected_student_id)  # Ensure this function is defined
        display_student_transcript(selected_student_id, student_name)

    display_all_courses_grades()
