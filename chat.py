import streamlit as st
import pandas as pd

# Title of the app
st.title('Simple Pandas App with Streamlit')

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("Data Preview:")
    st.dataframe(df.head())
    
    # Show basic statistics
    st.write("Basic Statistics:")
    st.write(df.describe())

    # Show columns
    st.write("Columns:")
    st.write(df.columns)
else:
    st.write("Please upload a CSV file.")
