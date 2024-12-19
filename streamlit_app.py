import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Website Masthead Extractor")

# Prompt the user to input a URL
url = st.text_input("Enter the website URL (e.g., https://www.example.com):", "")

if url:
    # Fetch the webpage
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
    else:
        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Try common masthead/header selectors
        masthead = None
        # Attempt a few different selectors commonly used:
        selectors = [
            "#masthead",           # An element with id="masthead"
            ".masthead",           # An element with class="masthead"
            "header",              # A <header> element, if it exists
            ".site-header"         # Another common class name for headers
        ]

        for selector in selectors:
            masthead = soup.select_one(selector)
            if masthead:
                break

        if masthead:
            st.subheader("Masthead HTML:")
            st.code(masthead.prettify(), language='html')

            # If you'd like to display images from the masthead, for example:
            # Find all images in the masthead
            images = masthead.find_all("img", src=True)
            if images:
                st.subheader("Masthead Images:")
                for img in images:
                    img_src = img['src']
                    # If the image source is relative, convert to absolute
                    if img_src.startswith("//"):
                        img_src = "https:" + img_src
                    elif img_src.startswith("/"):
                        img_src = url.rstrip('/') + img_src
                    st.image(img_src)
        else:
            st.write("No masthead element found with the given selectors.")
