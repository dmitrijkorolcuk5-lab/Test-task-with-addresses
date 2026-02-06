import asyncio
import httpx
from arq.connections import RedisSettings
from sqlalchemy import select, update


from app.db.session import AsyncSessionLocal
from app.models.address import Address
from app.core.config import settings

async def validate_address_task(ctx, address_id: int):
    
    async with AsyncSessionLocal() as session:
        
        result = await session.execute(select(Address).where(Address.id == address_id))
        address = result.scalar_one_or_none()
        
        if not address:
            print(f"--- Task Failed: Address {address_id} not found ---")
            return
        
        
        api_key = settings.SHIPENGINE_API_KEY
        url = "https://api.shipengine.com/v1/addresses/validate"
        headers = {
            "API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        payload = [{
            "address_line1": address.address_line1,
            "city_locality": address.city_locality,
            "state_province": address.state_province,
            "postal_code": address.postal_code,
            "country_code": address.country_code
        }]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()[0]
                
               
                status = data.get("status")
                
                is_valid_result = (status == "verified")

                await session.execute(
                    update(Address)
                    .where(Address.id == address_id)
                    .values(is_valid=is_valid_result)
                )
                await session.commit()
                
                print(f"--- Result for ID {address_id}: {status} (is_valid={is_valid_result}) ---")

        except Exception as e:
            print(f" API Error: {e}")

class WorkerSettings:
    
    functions = [validate_address_task]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)