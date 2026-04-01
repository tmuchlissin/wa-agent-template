import logging
import httpx

logger = logging.getLogger(__name__)

class WhatsAppClient:
    """Client for sending messages via the WhatsApp Cloud API."""

    def __init__(
        self,
        access_token: str,
        meta_api_url: str,
    ):
        self.access_token = access_token
        self.api_url = meta_api_url
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def _post(self, payload: dict) -> dict:
        """Send a POST request to the WhatsApp API."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(self.api_url, headers=self.headers, json=payload)
            try:
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error("[WA-API] HTTP Error: %s | Body: %s", e, resp.text)
                raise
            data = resp.json()

            msg_id = data.get("messages", [{}])[0].get("id")
            if msg_id:
                logger.info("[WA-API] Success: message_id=%s", msg_id)

            return data

    async def send_message(
        self, to: str, text: str,
        contact_id=None, business_number=None,
    ):
        """Send a text message."""
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }
        try:
            return await self._post(payload)
        except Exception as e:
            logger.error("[WA-API] Failed to send text to %s: %s", to[-4:], e)
            raise
