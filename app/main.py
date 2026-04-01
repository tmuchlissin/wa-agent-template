from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from app.core.startup import lifespan
from app.api import root, webhook

app = FastAPI(title="WhatsApp Agent Bot", lifespan=lifespan)

app.include_router(root.router)
app.include_router(webhook.router)
