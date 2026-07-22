from groq import Groq
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)