import httpx
from app.core.config import settings

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
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()[0]
                    return result.get("status") == "verified"
                return False
            except Exception:
                return False