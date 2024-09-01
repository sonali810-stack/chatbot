import requests
import json
import streamlit as st

# Define your Google Gemini API key and endpoint
GEMINI_API_KEY = "AIzaSyA9pYRt95gwUm3UvoZTy30PQ0P65F8niYA"  # Replace with your actual API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Function to fetch information about plant diseases
def fetch_from_gemini(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        try:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "I'm sorry, but I couldn't retrieve the information you requested."
        except json.JSONDecodeError:
            return "I'm sorry, there was an error processing your request."
    else:
        return f"Error fetching information from Google Gemini: {response.status_code} - {response.text}"

# Function to handle the submission
def submit_data():
    if 'input_text' in st.session_state and st.session_state.input_text:
        user_input = st.session_state.input_text

        if user_input.strip().lower() == 'exit':
            st.write("Thank you for using the assistant. Stay healthy!")
            st.session_state.input_text = ""
            return

        # Add the user's query to the conversation
        st.session_state.conversation.append(f"<div class='user-message'><strong>You:</strong> {user_input}</div>")

        # Fetch plant disease information from Google Gemini
        st.session_state.conversation.append("<div class='assistant-message'><strong>Assistant:</strong> I'm fetching information on how to cure this disease...</div>")
        response = fetch_from_gemini(user_input)
        st.session_state.conversation.append(f"<div class='assistant-message'><strong>Assistant:</strong> {response}</div>")

        # Clear input field
        st.session_state.input_text = ""

# Streamlit app
def main():
    st.set_page_config(page_title="Plant Disease Chatbot", page_icon="🌱", layout="wide")

    # Sidebar for app title and instructions
    st.sidebar.title("Plant Disease Chatbot 🌱")
    st.sidebar.write("Enter the name of the plant disease below, and the chatbot will provide information on how to cure it and more.")

    # Initialize or retrieve the context from session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Call the submission handler before rendering the input box
    submit_data()

    # Apply custom CSS based on theme
    st.markdown(
        """
        <style>
        .user-message {
            color: green;
        }
        .assistant-message {
            color: darkred;
        }
        body {
            background-color: #f5f5f5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Chat container with scrollable history
    chat_container = st.container()

    # Display the conversation history
    with chat_container:
        for chat in st.session_state.conversation:
            st.markdown(chat, unsafe_allow_html=True)

    # Input box for the user query
    st.text_input("Type the name of the plant disease here:", value="", key="input_text", on_change=submit_data)

if __name__ == '__main__':
    main()
