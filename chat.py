import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# Replace with your Canvas API token and base URL
API_TOKEN = '1941~FXJZ2tYC2DTWQr923eFTaXy473rK73A4KrYkT3uVy7WeYV9fyJQ4khH4MAGEH3Tf'  # Replace with your actual token
BASE_URL = 'https://kepler.instructure.com/api/v1'

# Set headers for authentication
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Function to fetch all courses
def fetch_all_courses():
    courses = []
    url = f'{BASE_URL}/accounts/1/courses?per_page=100'
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            courses_page = response.json()
            courses.extend(courses_page)
            # Handle pagination if next page exists
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        else:
            st.error(f"Error fetching courses: {response.status_code}")
            break
    return courses

# Function to fetch assignment groups for a course
def fetch_assignment_groups(course_id):
    url = f'{BASE_URL}/courses/{course_id}/assignment_groups'
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

# Function to fetch assignments in each group
def fetch_assignments(course_id, group_id):
    url = f'{BASE_URL}/courses/{course_id}/assignment_groups/{group_id}/assignments'
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

# Function to fetch student submissions for an assignment
def fetch_grades(course_id, assignment_id):
    grades = []
    url = f'{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/submissions?per_page=100'

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            grades_page = response.json()
            grades.extend(grades_page)
            # Handle pagination
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        else:
            st.error(f"Error fetching grades: {response.status_code}")
            break

    return grades

# Function to fetch student names
def fetch_student_name(student_id):
    url = f'{BASE_URL}/users/{student_id}/profile'
    response = requests.get(url, headers=headers)
    return response.json().get('name', 'Unknown') if response.status_code == 200 else 'Unknown'

# Function to calculate total grades and format data
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

                # Ensure grades are numeric
                grade = float(grade) if grade is not None else 0

                gradebook.append({
                    'Student ID': student_id,
                    'Student Name': student_name,
                    'Grade': grade
                })
    
    df = pd.DataFrame(gradebook)

    if not df.empty:
        # Group by student and take total grades
        df = df.groupby(['Student ID', 'Student Name']).sum().reset_index()
    
    return df

# Function to display a transcript for a specific student
def display_student_transcript(student_id, student_name):
    total_grades = []
    courses = fetch_all_courses()
    
    for course in courses:
        course_id = course['id']
        df_gradebook = format_gradebook(course_id)
        student_grades = df_gradebook[df_gradebook['Student ID'] == student_id]

        if not student_grades.empty:
            total_grades.append({
                'Course': course['name'],
                'Total Grade': student_grades['Grade'].values[0]
            })

    if total_grades:
        st.header(f"Transcript for {student_name}")
        transcript_df = pd.DataFrame(total_grades)
        st.dataframe(transcript_df)
    else:
        st.write("No grades found for this student.")

# Streamlit app starts here
def main():
    st.title("Course Grades")

    # Define the date threshold
    date_threshold = datetime.strptime("2024-05-01", "%Y-%m-%d")

    # Create a sidebar menu for selecting students
    st.sidebar.title("Menu")
    students = set()  # Use a set to avoid duplicates

    # Fetch all grades to populate the student list
    courses = fetch_all_courses()
    for course in courses:
        course_id = course['id']
        start_at = course.get('start_at')

        if start_at:
            try:
                course_start_date = datetime.strptime(start_at, "%Y-%m-%dT%H:%M:%SZ")
                if course_start_date > date_threshold:
                    df_gradebook = format_gradebook(course_id)
                    students.update(df_gradebook['Student ID'].unique())
            except ValueError:
                st.error(f"Error parsing start date for course {course['name']} (ID: {course_id}).")

    # Display the transcript option in the sidebar
    selected_student_id = st.sidebar.selectbox("Select a Student", list(students))
    if selected_student_id:
        student_name = fetch_student_name(selected_student_id)
        display_student_transcript(selected_student_id, student_name)

    # Display grades for all courses that meet the criteria
    for course in courses:
        course_id = course['id']
        start_at = course.get('start_at')

        if start_at:
            try:
                course_start_date = datetime.strptime(start_at, "%Y-%m-%dT%H:%M:%SZ")
                if course_start_date > date_threshold:
                    df_gradebook = format_gradebook(course_id)
                    if not df_gradebook.empty:
                        st.header(f"Course: {course['name']} (ID: {course_id})")
                        st.dataframe(df_gradebook)
            except ValueError:
                st.error(f"Error parsing start date for course {course['name']} (ID: {course_id}).")

# Run the Streamlit app
if __name__ == "__main__":
    main()
