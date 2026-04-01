from langchain_cerebras import ChatCerebras
from app.core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
# LLM = ChatCerebras(
#     model="llama3.1-8b",
#     api_key=settings.CEREBRAS_API_KEY,
#     temperature=0,
#     max_tokens=4000
# )

# LLM = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=settings.GEMINI_API_KEY,
#     temperature=0,
#     max_output_tokens=2000,
# )

LLM = ChatAnthropic(
    model="claude-haiku-4-5",
    api_key=settings.ANTHROPIC_API_KEY,
    temperature=0,
    max_tokens=4000
)