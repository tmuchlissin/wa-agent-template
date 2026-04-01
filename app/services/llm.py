from langchain_cerebras import ChatCerebras
from app.core.config import settings

LLM = ChatCerebras(
    model="llama3.1-8b",
    api_key=settings.CEREBRAS_API_KEY,
    temperature=0,
    max_tokens=4000
)
