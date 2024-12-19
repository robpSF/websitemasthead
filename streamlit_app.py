import streamlit as st
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

st.title("Website Masthead Extractor and Visualizer")

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
        selectors = [
            "#masthead",
            ".masthead",
            "header",
            ".site-header"
        ]

        for selector in selectors:
            masthead = soup.select_one(selector)
            if masthead:
                break

        if masthead:
            st.subheader("Masthead HTML:")
            st.code(masthead.prettify(), language='html')

            # Render a visualization of the masthead in an embedded frame
            st.subheader("Masthead Visualization:")

            # We create a minimal HTML structure to display the masthead snippet.
            # External CSS may not be fully available, but we add basic styling for context.
            rendered_html = f"""
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Masthead Preview</title>
                    <style>
                        body {{
                            margin: 0;
                            padding: 0;
                            font-family: Arial, sans-serif;
                        }}
                        header, .masthead, #masthead, .site-header {{
                            border: 1px solid #ccc;
                            padding: 10px;
                            text-align: center;
                            font-size: 1.2em;
                        }}
                    </style>
                </head>
                <body>{masthead}</body>
            </html>
            """

            # Use Streamlit's components.html to render the snippet
            components.html(rendered_html, height=300, scrolling=True)

            # If there are images in the masthead, display them below
            images = masthead.find_all("img", src=True)
            if images:
                st.subheader("Masthead Images:")
                for img in images:
                    img_src = img['src']
                    # Convert relative URLs to absolute
                    if img_src.startswith("//"):
                        img_src = "https:" + img_src
                    elif img_src.startswith("/"):
                        img_src = url.rstrip('/') + img_src
                    st.image(img_src)
        else:
            st.write("No masthead element found with the given selectors.")
