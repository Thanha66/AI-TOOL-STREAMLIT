# ui.py - Streamlit app for generating titles using Google Gemini with copy feature

import streamlit as st  # Streamlit library
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

# =========================
# 1. Configure Gemini API
# =========================
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================
# 2. Define structured response model
# =========================
class Titles(BaseModel):
    titles: List[str]

# =========================
# 3. Streamlit UI Elements
# =========================
st.title("💡 Blog/Video Title Generator")
st.write("Enter a topic, and get 5 catchy, SEO-friendly titles!")

# Text input for topic
topic = st.text_input("Topic", value="Digital marketing")

# Button to generate titles
if st.button("Generate Titles"):
    if not topic.strip():
        st.warning("Please enter a topic!")
    else:
        prompt = f"Generate 5 catchy and SEO-friendly blog/video titles about {topic}. Return them as a numbered list."

        try:
            # =========================
            # 4. Call Gemini API
            # =========================
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)

            # =========================
            # 5. Parse response
            # =========================
            lines = response.text.split("\n")
            titles_list = [line.lstrip("0123456789. ").strip() for line in lines if line.strip()]

            # Validate with Pydantic
            result = Titles(titles=titles_list[:5])

            # =========================
            # 6. Display results
            # =========================
            st.success("Here are your titles:")
            titles_text = ""
            for i, t in enumerate(result.titles, 1):
                st.write(f"{i}. {t}")
                titles_text += f"{i}. {t}\n"

            # =========================
            # 7. Copy to clipboard
            # =========================
            st.text_area("Copy all titles:", value=titles_text, height=150)

        except Exception as e:
            st.error(f"Something went wrong! Error details:\n{e}")
