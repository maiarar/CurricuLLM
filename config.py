from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    LLM_API_KEY = os.getenv("LLM_API_KEY")