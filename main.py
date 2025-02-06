import streamlit as st
from streamlit.components.v1 import html
import re
import google.generativeai as genai
import hashlib

# Configure the OpenAI API
key = "AIzaSyCiMCV_baOczaXAeQkhmMKH0IXin535RzI"
genai.configure(api_key=key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

def get_response(prompt):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config,
    )
    response = model.generate_content(prompt)
    return response.text

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to hash passwords
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Dictionary of username/password pairs (in production, use a secure database)
users = {
    "admin": make_hash("admin123"),
    "user": make_hash("user123")
}

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in users and users[username] == make_hash(password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def main_app():
    st.set_page_config(page_title="Architecture Diagram Generator", layout="wide")
    st.title('Architecture Diagram Generator')
    
    # Add logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    user_input = st.text_area('Enter your query:')
    prompt_for_generating_mermaid = f"""Create a precise Mermaid diagram (version 11.4.1) that visualizes the following user input:
    {user_input}
    Requirements:
    - Generate only valid Mermaid code without markdown markers
    - Follow proper syntax for arrows (use | instead of |>)
    - Maintain consistent node shapes ([Rectangle], (Round), {{Rhombus}}, etc.)
    - Use descriptive edge labels between nodes
    - Apply appropriate styling (colors, borders, etc.) for visual hierarchy
    - Ensure proper spacing and indentation
    - Support all Mermaid diagram types (flowchart, sequence, class, etc.)
    - Use clear, meaningful node IDs and labels
    - Include any necessary definitions or subgraphs"""

    if st.button("Generate Diagram"):
        mermaid_code = get_response(prompt_for_generating_mermaid)
        if '```mermaid' in mermaid_code:
            parts = mermaid_code.split('```mermaid')
            cleaned_code = parts[1]
        else:
            cleaned_code = mermaid_code

        mermaid_html = f"""
        <div class="mermaid">
            {cleaned_code}
        </div>
        <script>
            mermaid.initialize({{"startOnLoad": true}});
        </script>
        """
        
        html_content = f"""
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        {mermaid_html}
        """
        
        st.subheader("Rendered Diagram")
        if 'Syntax error' not in html_content:
            html(html_content, height=3000)
        else:
            st.write("error is in code")
    else:
        st.info("Click 'Generate Diagram' to see your Mermaid diagram here.")

    st.markdown(
        """
        ---
        Created with ❤️ using [Streamlit](https://streamlit.io) and [Mermaid.js](https://mermaid-js.github.io).
        """
    )
    st.markdown('Developed by Bishnu Haldar')

# Main logic
if not st.session_state.logged_in:
    login()
else:
    main_app()
