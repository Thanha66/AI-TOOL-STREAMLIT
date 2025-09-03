from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

# Load .env file
load_dotenv()

# 1. Use the key from .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Define structured response model
class Titles(BaseModel):
    titles: List[str]

# 3. User input
topic = "Digital marketing"

# 4. Prompt
prompt = f"Generate 5 catchy and SEO-friendly blog/video titles about {topic}. Return them as a numbered list."

# 5. Call Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# 6. Parse response into list of titles
lines = response.text.split("\n")
titles = [line.lstrip("0123456789. ") for line in lines if line.strip()]

# Validate with Pydantic
result = Titles(titles=titles[:5])

# 7. Print results
print("\n".join(result.titles))
