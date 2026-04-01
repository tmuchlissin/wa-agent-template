
import uvicorn, logging
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from app.core.startup import lifespan
from app.api import root, webhook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True
)

logger = logging.getLogger("main")

app = FastAPI(title="WhatsApp Agent Bot", lifespan=lifespan)

app.include_router(root.router)
app.include_router(webhook.router)

if __name__ == "__main__":
    logger.info("🚀 Starting WhatsApp Agent Bot ...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )