import logging, uvicorn

logger = logging.getLogger("run")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)

if __name__ == "__main__":
    logger.info("🚀 Starting WhatsApp Agent Bot from run.py ...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
