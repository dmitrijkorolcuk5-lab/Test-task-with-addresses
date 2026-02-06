import httpx
from app.core.config import settings

class ShipEngineClient:
    def __init__(self):
        self.api_key = settings.SHIPENGINE_API_KEY
        self.base_url = "https://api.shipengine.com/v1/addresses/validate"

    async def validate_address(self, address_data: dict) -> bool:
        headers = {
            "API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        # ShipEngine expects a list of addresses
        payload = [address_data]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return False
                
            # Check the first result
            result = data[0]
            return result.get("status") == "verified"
