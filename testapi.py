import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to fetch and parse content from a webpage
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

# Specific links you want to scrape
specific_links = [
    "https://keplercollege.ac.rw/about-us/",
    "https://keplercollege.ac.rw/leadership/",
    "https://keplercollege.ac.rw/faculty/",
    # Add more links here as needed
]

# Scrape content from the specific pages
all_text = ""
for link in specific_links:
    all_text += f"Content from {link}:\n"
    all_text += fetch_website_content(link) + "\n\n"

# Display the full content on the Streamlit page (or for debugging purposes)
st.write("Website Content Extracted from Specific Links:")
st.write(all_text)
