from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.address import Address

class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, address_data: dict) -> Address:
        new_address = Address(**address_data)
        self.session.add(new_address)
        await self.session.flush()
        return new_address
    
    async def get_by_id(self, address_id: int) -> Address | None:
        return await self.session.get(Address, address_id)
    
    async def get_all(self):
        result = await self.session.execute(select(Address))
        return result.scalars().all()