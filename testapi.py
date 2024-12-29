import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to fetch and parse content from a website
def fetch_website_content(url):
    try:
        # Send a request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from headings (h1, h2, h3, etc.) and paragraphs (p)
        headings = soup.find_all(['h1', 'h2', 'h3'])
        paragraphs = soup.find_all('p')
        
        # Join the text content from headings and paragraphs
        website_text = " ".join([heading.get_text() for heading in headings])
        website_text += " ".join([para.get_text() for para in paragraphs])

        return website_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return ""

# Load website content
website_url = "https://keplercollege.ac.rw/"
website_content = fetch_website_content(website_url)

# Display the content fetched from the website (for debugging)
st.write("Website Content Extracted:")
st.write(website_content)
