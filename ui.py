import streamlit as st
import google.generativeai as genai
import pandas as pd

# =========================
# 1. Configure Gemini API
# =========================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("🚨 GOOGLE_API_KEY not found! Please add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

# =========================
# 2. Define structured response model
# =========================
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# 3. Streamlit App UI
# =========================
st.title("🤖 Master AI")
st.write("Welcome! This AI tool generates creative titles for your ideas using Google's Gemini AI.")

# Input area
user_input = st.text_area("Enter your project description:", placeholder="E.g. An app that tracks your daily habits using AI...")

# Button
if st.button("✨ Generate Title"):
    if user_input.strip():
        with st.spinner("Generating a creative title..."):
            try:
                response = model.generate_content(f"Generate a catchy, creative title for this project idea: {user_input}")
                title = response.text.strip()
                st.success("✅ Title generated successfully!")
                st.subheader(f"💡 Suggested Title: {title}")
            except Exception as e:
                st.error(f"⚠️ Error generating title: {e}")
    else:
        st.warning("Please enter a description first!")

# =========================
# 4. Footer
# =========================
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Google Gemini API.")


       

         
