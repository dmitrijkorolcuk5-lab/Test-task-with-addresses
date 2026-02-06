import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class ShipEngineClient:
    def __init__(self):
        self.api_key = settings.SHIPENGINE_API_KEY
        self.base_url = "https://api.shipengine.com/v1"

    async def validate_address(self, address_data: dict) -> bool:
        async with httpx.AsyncClient() as client:
            headers = {
                "API-Key": self.api_key,
                "Content-Type": "application/json"
            }
            payload = [address_data]

            try:
                response = await client.post(
                    f"{self.base_url}/addresses/validate",
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                result = response.json()[0]
                return result.get("status") == "verified"
            except httpx.HTTPStatusError as e:
                logger.error(f"ShipEngine API returned an error: {e.response.status_code} - {e.response.text}")
                return False
            except httpx.RequestError as e:
                logger.error(f"Request to ShipEngine API failed: {e}")
                return False
            except (KeyError, IndexError) as e:
                logger.error(f"Failed to parse ShipEngine API response: {e} - Response: {response.text if 'response' in locals() else 'N/A'}")
                return False