import streamlit as st
import google.generativeai as genai  # Import Gemini API

# Set Gemini API Key (Replace 'your-api-key' with a valid one)
API_KEY = "AIzaSyC9RnsaVrgzL5RPrULefVkAu1TP-eC87Fc"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Set Streamlit page config (this must be at the very beginning)
st.set_page_config(page_title="Fin Bot", layout="wide")

# Get available models
def get_available_models():
    try:
        models = genai.list_models()
        # Filter for models that support generateContent and are not deprecated
        return [model.name for model in models if "generateContent" in model.supported_generation_methods and "vision" not in model.name.lower()]
    except Exception as e:
        st.error(f"Error fetching models: {e}")  # Display error in Streamlit
        return ["gemini-pro"]  # Default model if fetching fails

AVAILABLE_MODELS = get_available_models()

def chatbot_response(prompt, model_name):
    """Get response from Gemini API"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e} (Check your API key, quota, and billing details)")  # Display error in Streamlit
        return f"Error: {e} (Check your API quota and billing details)"

# Custom CSS styling for title and other elements
st.markdown("""
    <style>
        /* Custom styling for the heading */
        .main-title {
            color: #4CAF50;  /* Green color */
            font-family: 'Courier New', Courier, monospace;  /* Font style */
            font-size: 40px;
            font-weight: bold;
        }

        /* Custom styling for chatbot messages */
        .user-message {
            color: #1E90FF;  /* Blue color for user message */
            font-size: 16px;
            font-family: Arial, sans-serif;
        }

        .bot-message {
            color: #8A2BE2;  /* Purple color for bot response */
            font-size: 16px;
            font-family: 'Georgia', serif;
        }

        /* Sidebar Styling */
        .sidebar-header {
            font-family: 'Verdana', sans-serif;
            color: #333333;
            font-size: 18px;
            font-weight: bold;
        }

        /* Footer Styling */
        .footer-text {
            font-family: 'Arial', sans-serif;
            color: #555555;
            font-size: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title with custom class for styling
st.markdown('<p class="main-title">💰 Fin Bot 🤖</p>', unsafe_allow_html=True)

# Sidebar for chatbot settings
st.sidebar.header("Settings")
st.sidebar.markdown("Choose the model and set preferences.")  # Description of the settings

# Dropdown menu to select the model
if AVAILABLE_MODELS:
    model_choice = st.sidebar.selectbox("Select Model", AVAILABLE_MODELS)
else:
    model_choice = "gemini-pro"  # Fallback if model list is empty.

# Chat interface
st.write("### Chat with Fin Bot!")

# Initialize chat history
chat_history = st.session_state.get("chat_history", [])

# Input field for user query
user_input = st.text_input("Ask me anything about finance, investments, or digital assets:")

# Button to send the user input to the chatbot
if st.button("Send") and user_input:
    response = chatbot_response(user_input, model_choice)
    chat_history.append(("You", user_input))  # Store user input in chat history
    chat_history.append(("Fin Bot", response))  # Store bot response in chat history
    st.session_state.chat_history = chat_history  # Save chat history to session state

# Display chat history with custom styles
for sender, message in chat_history:
    if sender == "You":
        st.markdown(f'<p class="user-message"><b>{sender}:</b> {message}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="bot-message"><b>{sender}:</b> {message}</p>', unsafe_allow_html=True)

# Footer section in the sidebar with custom class for footer
st.sidebar.markdown("---")
st.sidebar.markdown('<p class="footer-text">Developed by Mehar Paryas | BSc CSM, Pursuing MBA FinTech</p>', unsafe_allow_html=True)
