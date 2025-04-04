import streamlit as st
import requests
import time  # For simulating delay during loading

# Backend API URL
BACKEND_URL = "http://localhost:8000/analyze"  # Ensure FastAPI is running

# Streamlit UI
st.title("Code Bug Detector & Fixing")  # Removed snake emoji

# Apply custom styles using Markdown
st.markdown(
    """
    <style>
        body {
            background-color: #f7f7f7;  /* Background color for the entire page */
        }
        .stTextArea {
            background-color: #e3f2fd;  /* Lighter blue color for the input box */
            color: #333;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Courier New', Courier, monospace;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
           font-size: 16px;
            border-radius: 5px;
            padding: 10px 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stError {
            color: red;
        }
        .stWarning {
            color: #ff9800;
        }
        .stSuccess {
            color: #4CAF50;
        }
        .stSubheader {
            color: #0056b3;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Code input box with style
code = st.text_area("Enter your Python code here:", height=200, key="code_input")

# Button click action
if st.button("Analyze Code"):
    if code.strip():
        with st.spinner("Analyzing your code... Please wait!"):
            time.sleep(2)  # Simulating delay for demonstration purposes

            # Send request to backend
            response = requests.post(BACKEND_URL, json={"code_snippet": code})

            if response.status_code == 200:
                result = response.json().get("analysis", "No analysis result found.")
                st.subheader("Code Analysis & Fix:")
                st.text_area("Output:", result, height=300)
            else:
                st.error("Error: Unable to connect to the backend!")
    else:
        st.warning("Please enter some code to analyze.")
