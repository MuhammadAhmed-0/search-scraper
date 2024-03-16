try:
    import bs4
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4==4.10.0'])

# Import necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define a function to retrieve Google search results
def get_google_results(query):
    # Google search URL
    url = f"https://www.google.com/search?q={query}"
    # Define headers to mimic a browser user-agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    # Send GET request to Google
    response = requests.get(url, headers=headers)
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    # Iterate through search results
    for i, g in enumerate(soup.find_all('div', class_='tF2Cxc')):
        # Extract link, title, and snippet (if available)
        link = g.find('a')['href']
        title = g.find('h3').text
        snippet = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else None
        # Append result to list
        results.append({'title': title, 'link': link, 'snippet': snippet})
        # Limit to top 10 results
        if i == 9:
            break
    return results

# Streamlit UI code
# Set page title and description
st.title("Google Search Results Scraper")
st.write("Enter your search query below:")

# User input for search query
query = st.text_input("Search Query")

# Execute search when button is clicked
if st.button("Search"):
    # Call function to get search results
    results = get_google_results(query)
    # Display results
    if len(results) > 0:
        st.write(f"Showing top {len(results)} results for '{query}':")
        for idx, result in enumerate(results, 1):
            # Display each result with title, link, and snippet (if available)
            st.subheader(f"Result {idx}:")
            st.write(f"Title: {result['title']}")
            st.write(f"Link: {result['link']}")
            if result['snippet']:
                st.write(f"Snippet: {result['snippet']}")
            st.write("\n")
    else:
        st.write("No results found.")
