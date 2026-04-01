import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.llm import LLM
from app.services.agent import init_agent
from app.services.whatsapp import WhatsAppClient
from app.prompts.custom import CUSTOM_PROMPT
from app.core.config import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting up application...")
    
    # client, tool_names = await init_mcp_client()
    # logger.info(f"Tools loaded: {tool_names}")

    agent = init_agent(LLM, CUSTOM_PROMPT)

    whatsapp_client = WhatsAppClient(
        access_token=settings.ACCESS_TOKEN,
        meta_api_url=settings.META_API_URL
    )

    app.state.agent = agent
    app.state.whatsapp_client = whatsapp_client
    app.state.processing_message_ids = set()

    yield

    # logger.info("🛑 Shutting down MCP client...")
    # await client.close()