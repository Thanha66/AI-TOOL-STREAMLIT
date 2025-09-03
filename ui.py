# ==============================================
# Streamlit UI for Gemini Blog/Video Title Generator
# ==============================================

# Import required libraries
import streamlit as st               # For building the user interface
import google.generativeai as genai  # Gemini API for AI text generation
from pydantic import BaseModel       # For validating structured data
from typing import List              # To define a list of titles


# --------------------------------------------------
# 1. Configure Gemini API
# --------------------------------------------------
# Normally, you should store your API key securely (in environment variables or a .env file).
# Here, we hard-code it for simplicity, but beginners should know this is NOT best practice.
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")  # <- Replace with your real key


# --------------------------------------------------
# 2. Define structured response model
# --------------------------------------------------
# Pydantic helps us validate the AI output so it always fits into a clean Python list.
class Titles(BaseModel):
    titles: List[str]


# --------------------------------------------------
# 3. Streamlit Page Setup
# --------------------------------------------------
# These commands make the page look more professional
st.set_page_config(
    page_title="AI Blog/Video Title Generator",  # Browser tab title
    page_icon="📝",                              # Small icon for the app
    layout="centered"                            # Keep everything nicely centered
)

# Add a title and description to the UI
st.title("📝 AI Blog/Video Title Generator")
st.write("Generate **catchy and SEO-friendly titles** for blogs or videos using Google Gemini.")


# --------------------------------------------------
# 4. User Input Section
# --------------------------------------------------
# Streamlit provides user input widgets (text boxes, sliders, buttons, etc.)
# We will use a text input box for the topic.
topic = st.text_input("Enter your topic:", value="Digital marketing")

# Add a button to trigger AI generation
generate_button = st.button("✨ Generate Titles")


# --------------------------------------------------
# 5. Run Gemini Model When Button is Clicked
# --------------------------------------------------
if generate_button:
    if topic.strip() == "":
        # If the input is empty, show a warning
        st.warning("⚠️ Please enter a topic before generating titles.")
    else:
        # Construct the AI prompt
        prompt = f"Generate 5 catchy and SEO-friendly blog/video titles about {topic}. Return them as a numbered list."

        # Choose the Gemini model (flash = faster, cheaper; pro = better reasoning)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Call the AI to generate content
        response = model.generate_content(prompt)

        # --------------------------------------------------
        # 6. Parse the AI Response into a List of Titles
        # --------------------------------------------------
        lines = response.text.split("\n")  # Split by line breaks
        titles = [line.lstrip("0123456789. ") for line in lines if line.strip()]

        # Validate with Pydantic (ensures we only keep 5 clean titles)
        result = Titles(titles=titles[:5])

        # --------------------------------------------------
        # 7. Display Results in Streamlit
        # --------------------------------------------------
        st.subheader("✅ Suggested Titles:")
        for i, title in enumerate(result.titles, start=1):
            st.write(f"{i}. {title}")  # Display each title nicely


# --------------------------------------------------
# End of Script
# --------------------------------------------------
# Tips for Beginners:
# - Try changing the default topic to see how AI responds.
# - Experiment with the prompt to generate different styles of titles.
# - Replace "gemini-1.5-flash" with "gemini-1.5-pro" if you want deeper reasoning (but it may be slower).
