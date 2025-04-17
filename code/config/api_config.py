import os
from dotenv import load_dotenv

load_dotenv()


class DeepseekConfig:
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    BASE_URL = "https://api.deepseek.com/v1"
    HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
