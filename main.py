import streamlit as st
from streamlit.components.v1 import html
from groq import Groq
from dotenv import load_dotenv
import re
load_dotenv()


def get_response(query):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": query
        }],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content  # Store for return
    return response

# Set page configuration
st.set_page_config(page_title="Architecture Digram Generator", layout="wide")

st.title('Architecture Digram Generator')

user_input=st.text_area('Enter your query:')
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
- Include any necessary definitions or subgraphs

Example of correct syntax:
graph LR
    A[User] -->|input| B(Process)
    B -->|transform| C{{Decision}}
    C -->|yes| D[Output]
    C -->|no| A
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px

Notes:
- Avoid common syntax errors like |> instead of |
- Use consistent indentation (4 spaces)
- Include styling where it adds clarity
- Ensure all nodes are connected properly
- Use meaningful directional indicators (TB, LR, RL, BT)
"""

# Button to render Mermaid diagram
if st.button("Generate Diagram"):
    mermaid_code=get_response(prompt_for_generating_mermaid)
    # cleaned_code = re.sub(r".*?", "", mermaid_code, flags=re.DOTALL).strip()
    # cleaned_code = mermaid_code.strip('`').replace('mermaid\n', '', 1).replace('```', '')
    if '```mermaid'  in mermaid_code:
        parts = mermaid_code.split('```mermaid')

        cleaned_code = parts[1]
    else:
        cleaned_code=mermaid_code
    # Embed Mermaid code in an HTML template
    # st.code(cleaned_code)
    mermaid_html = f"""
    <div class="mermaid">
        {cleaned_code}
    </div>
    <script>
        mermaid.initialize({{"startOnLoad": true}});
    </script>
    """

    # Load Mermaid.js
    html_content = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    {mermaid_html}
    """

    # Display the diagram
    st.subheader("Rendered Diagram")
    if 'Syntax error' not in html_content:
        html(html_content, height=3000)
    else:
        st.write("error is in code")
else:
    st.info("Click 'Render Diagram' to see your Mermaid diagram here.")

# Footer
st.markdown(
    """
    ---
    Created with ❤️ using [Streamlit](https://streamlit.io) and [Mermaid.js](https://mermaid-js.github.io).
    """
)

st.markdown('Developed by Bishnu Haldar')
