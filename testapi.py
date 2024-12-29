import requests
from bs4 import BeautifulSoup
import streamlit as st
import time

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

        return website_text, soup
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching website content: {str(e)}")
        return "", None

# Function to get all links from a webpage (internal links only)
def get_internal_links(soup, base_url):
    links = []
    for anchor in soup.find_all('a', href=True):
        link = anchor['href']
        if link.startswith('/') or base_url in link:
            # Resolve relative links to absolute links
            if link.startswith('/'):
                link = base_url + link
            links.append(link)
    return links

# Function to scrape the entire website
def scrape_entire_website(url):
    visited = set()  # Set to keep track of visited URLs
    all_text = ""

    # List of pages to visit
    pages_to_visit = [url]

    while pages_to_visit:
        current_url = pages_to_visit.pop(0)
        
        # Avoid revisiting pages
        if current_url in visited:
            continue
        visited.add(current_url)

        # Fetch content from the page
        page_content, soup = fetch_website_content(current_url)
        all_text += page_content + "\n\n"

        # Get links to other pages on the same site
        if soup:
            links = get_internal_links(soup, url)
            pages_to_visit.extend(links)

        # To avoid getting blocked, add a small delay between requests
        time.sleep(1)

    return all_text

# Start scraping from the homepage
website_url = "https://keplercollege.ac.rw/"
website_content = scrape_entire_website(website_url)

# Display the full content on the Streamlit page (or for debugging purposes)
st.write("Website Content Extracted:")
st.write(website_content)
