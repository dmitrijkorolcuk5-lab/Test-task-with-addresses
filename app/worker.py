import asyncio
from arq.connections import RedisSettings
from app.db.session import async_session
from app.models.address import Address
from sqlalchemy import update

async def validate_address_task(ctx, address_id: int):
    print(f"--- Start validation for ID: {address_id} ---")
    await asyncio.sleep(5)
    
    async with async_session() as session:
        await session.execute(
            update(Address).where(Address.id == address_id).values(is_valid=True)
        )
        await session.commit()
    print(f"✅ Address {address_id} validated successfully!")

class WorkerSettings:
    functions = [validate_address_task]
    redis_settings = RedisSettings(host='localhost', port=6380)