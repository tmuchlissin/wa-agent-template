import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    # Meta 
    ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN')
    PHONE_NUMBER_ID: str = os.getenv('PHONE_NUMBER_ID')
    VERIFY_TOKEN: str = os.getenv('VERIFY_TOKEN')
    META_API_VERSION: str = os.getenv('META_API_VERSION')
    META_API_URL: str = f"https://graph.facebook.com/{META_API_VERSION}/{PHONE_NUMBER_ID}/messages"
    
    # API key
    CEREBRAS_API_KEY: str = os.getenv('CEREBRAS_API_KEY')
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY')
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY')

settings = Settings()
